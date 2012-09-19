#-*- coding: UTF-8 -*-
import hashlib
from random import randint
from datetime import date, timedelta
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from solonotebooks import settings
from solonotebooks.cotizador.forms import DateRangeForm
from models import *
from exceptions import *
from string import digits, lowercase

def clean_price_string(price_string):
    """
    Removes most common formatting of a string that represents a price
    leaving it only with its numbers.
    """

    blacklist = ['CLP$', '$', '.', ',', '&nbsp;', '\r', '\n', '\t']

    for item in blacklist:
        price_string = price_string.replace(item, '')

    return price_string

def stringCompare(comp1, comp2):
    comp1_words = comp1.lower().split()
    comp2_words = comp2.lower().split()
    counter = 0
    for word in comp2_words:
        for comp1_word in comp1_words:
            if word in comp1_word:
                counter += 1
                break
            
    return 100.0 * counter / len(comp2_words)

def load_advertisement(position):
    try:
        ads = Advertisement.objects.filter(position__name = position).filter(is_active = True)
        ad_index = randint(0, len(ads) - 1)
        ad = ads[ad_index]
        ad.impressions += 1
        ad.save()
    except:
        ad = None
        
    return ad
    
def send_email(user, subject, template, args = {}):
    args['server_name'] = settings.SERVER_NAME
    args['site_name'] = settings.SITE_NAME
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [ user.username + '<' + user.email + '>' ])
    
def send_facebook_registration_mail(user):
    subject = 'Registro en ' + settings.SITE_NAME
    t = get_template('mails/facebook_registration_mail.html')
    
    send_email(user, subject, t)
    
def send_signup_mail(user):
    if user.get_profile().confirmation_mails_sent >= 5:
        raise MailException('Superado el límite de correos de confirmación que se pueden enviar')
    else:
        send_confirmation_mail_from_template(user, 'mails/confirmation_mail.html')
        user.get_profile().confirmation_mails_sent += 1
        user.get_profile().save()
        
def send_change_mail(user):
    if user.get_profile().change_mails_sent >= 5:
        raise MailException('Superado el límite de solicitud de cambios de correo')
    else:
        send_confirmation_mail_from_template(user, 'mails/change_email.html')
        user.get_profile().change_mails_sent += 1
        user.get_profile().save()        
    
def send_confirmation_mail_from_template(user, template):
    subject = 'Confirmación correo electrónico de ' + settings.SITE_NAME
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()
    
    t = get_template(template)
    args = {'user_digest': user_digest}
    
    send_email(user, subject, t, args)
    
def send_password_regeneration_mail(user):
    subject = 'Regeneración de contraseña de ' + settings.SITE_NAME
    user_digest = hashlib.sha224(settings.SECRET_KEY + user.username + user.password).hexdigest()
    
    t = get_template('mails/password_regeneration_mail.html')
    args = {'user_digest': user_digest}
    send_email(user, subject, t, args)    
    
def send_new_password_mail(user, new_password):
    subject = 'Nueva contraseña de ' + settings.SITE_NAME
    
    t = get_template('mails/new_password_mail.html')
    args = {'new_password': new_password}
    
    send_email(user, subject, t, args)    
    
# Helper method to set the search_form for almost all of the views            
def initialize_search_form(request, ptype = ProductType.default()):
    from solonotebooks.cotizador.forms import *

    if not ptype:
        return None
    qd = request.GET.copy()
    search_form_class = eval(ptype.classname + 'SearchForm')
    
    extra_permissions = False
    if request.user.is_authenticated() and request.user.get_profile().allows_extra_ordering_options():
        extra_permissions = True
    search_form = search_form_class(qd, extra_permissions)
    
    search_form.validate()
    search_form.is_valid()
    
    return search_form
    
def set_subscription_mail_notifications(request, subscription_id, new_mail_notification_status):
    try:
        subscription = ProductSubscription.objects.get(pk = subscription_id)
        if subscription.user != request.user or not subscription.is_active:
            raise SubscriptionException('Error de seguridad')
        subscription.email_notifications = new_mail_notification_status
        subscription.save()
    except SubscriptionException, e:
        request.flash['error'] = str(e)
    except Exception, e:
        request.flash['error'] = 'Error desconocido'
        
def concat_dictionary(d):
    vals = ['%s=%s' % (k, v) for k, v in d.items()]
    if vals:
        return '?' + '&'.join(vals)
    else:
        return ''
        
def generate_timelapse_chart(data_streams, start_date, end_date, legends, filename, title):
    import cairo
    import pycha.line
    from copy import deepcopy
    
    data_streams = [dict(stream) for stream in data_streams]
    step_date = timedelta(days = 1)
    
    final_streams = []
    for stream in data_streams:
        sdate = start_date
        
        while sdate <= end_date:
            if sdate not in stream:
                stream[sdate] = 0
            sdate += step_date
        
        stream = stream.items()
        stream = sorted(stream, key = lambda pair: pair[0])
        final_streams.append(stream)
        
    data_streams = final_streams
    
    main_data_stream = data_streams[0]
    values = [v for k, v in main_data_stream]
    
    maxi = max(values)
    r = (main_data_stream[0][0].toordinal(), main_data_stream[-1][0].toordinal())
    
    chart_data_set = [(legends[idx], [(k.toordinal(), v) for k, v in l]) for idx, l in enumerate(data_streams)]
        
    dataSet = chart_data_set

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v = k.toordinal(), label = str(k.day) + '/' + str(k.month)) for k, v in main_data_stream],
                'range': r
            },
            'y': {
                'tickCount': 4,
                'range': (0, maxi * 1.2)
            }
        },
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444',
            'baseColor': '#FFFFFF',
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'blue',
            },
        },
        'legend': {
            #'hide': True,
        },
        'padding': {
            'left': 60,
            'bottom': 20,
            'right': 10,
        },
        'title': title
    }
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 850, 400)
    chart = pycha.line.LineChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + filename)
    
def generate_pie_chart(data, filename, title):
    import cairo
    import pycha.pie
    from copy import deepcopy
    
    if not data:
        return False
        
    dataSet = [(entry[0], [[0, entry[1]]]) for entry in data]

    options = {
        'axis': {
            'x': {
                #'ticks': [dict(v = k.toordinal(), label = str(k.day) + '/' + str(k.month)) for k, v in main_data_stream],
                #'range': r
            },
            'y': {
                'tickCount': 4,
                #'range': (0, maxi * 1.2)
            }
        },
        'background': {
            'color': '#eeeeff',
            'lineColor': '#444444',
            'baseColor': '#FFFFFF',
        },
        'colorScheme': {
            'name': 'rainbow', 
            'args': 
                {'initialColor': 'red'}
        },
        'legend': {
            #'hide': True,
        },
        'padding': {
            #'left': 60,
            #'bottom': 20,
            #'right': 10,
        },
        'title': title
    }
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 890, 500)
    chart = pycha.pie.PieChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(settings.MEDIA_ROOT + '/charts/' + filename)
    
    return True
    
def urlify(unistring):
    unistring = latin1_to_ascii(unistring)
    unistring = unistring.lower()
    valid_symbols = lowercase + digits
    final_string = ''
    for c in unistring:
        if c in valid_symbols:
            final_string += c
        else:
            final_string += ' '
    final_string = '-'.join([w for w in final_string.split(' ') if w])
    return final_string
    
    
def latin1_to_ascii(unicrap):
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
        0xd7:'*', 0xf7:'/'
        }

    r = ''
    for i in unicrap:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += i
    return r

def fill_timelapse(entries,
                   start_date,
                   end_date,
                   series_name_function,
                   value_function=None,
                   date_function=None,
                   null_value=0):
    """
    Function used to format data for line charts (with one or more series)

    Entries is the input data, an iterable object sorted first by series and
    second by date.

    The function returns a dictionary series_name => series_data, where series
    data is a list of (date, value) tuples sorted by date.

    start_date and end_date define the limits of the function. For each series
    all its dates between start and date will have a value. If the input
    entries don't provide it then the "null_value" will be used.

    label_function is a function that, given an element of entries, returns the
    name of the series it must belong to.

    value_function is a function that, given an element of entries, returns the
    value to be used in the resulting structure. If not given the function will
    try and access the 'data' element of the antry as if it were a dictionary.

    date_function is a function that, given an element of entries, returns the
    date to be used in the resulting structure to index the entry. If not given
    the function will try and access the 'date' element of the antry as if it
    were a dictionary.
    """

    if not value_function:
        value_function = lambda x: x['data']

    if not date_function:
        date_function = lambda x: x['date']

    one_day = timedelta(days=1)
    next_function = lambda x: x + one_day

    return generic_fill_lapse(
        entries=entries,
        start_key=start_date,
        end_key=end_date,
        next_function=next_function,
        series_name_function=series_name_function,
        key_function=date_function,
        value_function=value_function,
        null_value=null_value
    )


def generic_fill_lapse(entries,
                       start_key,
                       end_key,
                       next_function,
                       series_name_function,
                       key_function,
                       value_function,
                       null_value=None):

    result = {}
    current_series_name = None

    # next_expected_key will have a real value inside the loop, but we need
    # to have it in scope
    next_expected_key = None

    series_names = []

    for entry in entries:
        entry_key = key_function(entry)
        entry_series_name = series_name_function(entry)

        if current_series_name != entry_series_name:
            next_expected_key = start_key

            current_series_name = entry_series_name
            series_names.append(current_series_name)
            result[current_series_name] = []

        while next_expected_key < entry_key:
            result[entry_series_name].append([next_expected_key, null_value])
            next_expected_key = next_function(next_expected_key)

        entry_value = value_function(entry)

        result[entry_series_name].append([entry_key, entry_value])

        next_expected_key = next_function(next_expected_key)

    # Pad the end
    for serie_name in series_names:
        next_key = next_function(result[serie_name][-1][0])

        while next_key <= end_key:
            result[serie_name].append([next_key, null_value])
            next_key = next_function(next_key)

    return result


epoch = date(1970, 1, 1)


def milliseconds_since_epoch(date):
    td = date - epoch
    return long(td.seconds + (td.days * 24 * 3600) * 1000)


# Utility methods for highcharts

def get_and_clean_form(data, FormClass=DateRangeForm):
    form = FormClass(data)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    else:
        start_date, end_date = FormClass.default_dates()

    return form, start_date, end_date

def line_chart_data(start_date, end_date, data_calculation_method):
    series = []

    serie_history = data_calculation_method(start_date, end_date)

    for series_name, date_value_tuple in serie_history.items():
        result = [(milliseconds_since_epoch(d), p)
                  for d, p in date_value_tuple]

        series.append({
            'name': series_name,
            'data': result
        })

    return series