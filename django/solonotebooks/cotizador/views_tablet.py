from django.http import HttpResponse
from django.template import Template
from django.template import Context, loader
import simplejson
from solonotebooks.cotizador.forms.simple_notebook_search_form import SimpleNotebookSearchForm

def index(request):
    form = SimpleNotebookSearchForm(request.GET)
    form.is_valid()

    notebooks, shpes = form.find_best_notebooks()

    result = []

    for idx, notebook in enumerate(notebooks):
        if notebook.processor.speed_score < 1600:
            processor_score = 1
        elif notebook.processor.speed_score < 2400:
            processor_score = 2
        elif notebook.processor.speed_score < 3900:
            processor_score = 3
        else:
            processor_score = 4

        vc = notebook.video_card.order_by('-speed_score')[0]

        if vc.speed_score < 3200:
            graphics_score = 1
        elif vc.speed_score < 5000:
            graphics_score = 2
        elif vc.speed_score < 7500:
            graphics_score = 3
        else:
            graphics_score = 4

        screen_mobility_normalized_score = (notebook.screen.size.family.base_size - 10) / 6.0
        cpu_mobility_normalized_score = (notebook.processor.consumption - 1) / 4.0

        mobility_score = (screen_mobility_normalized_score + cpu_mobility_normalized_score) / 2.0

        # The less the more mobile it is
        if mobility_score > 0.75:
            mobility_score = 1
        elif mobility_score > 0.50:
            mobility_score = 2
        elif mobility_score > 0.25:
            mobility_score = 3
        else:
            mobility_score = 4

        t = loader.get_template('tablet/notebook_data.html')
        c = Context({
            'notebook': notebook,
        })

        subresult = dict()
        subresult['html_description'] = t.render(c)
        subresult['picture_url'] = notebook.picture.url
        subresult['application_score'] = processor_score
        subresult['games_score'] = graphics_score
        subresult['mobility_score'] = mobility_score
        subresult['price'] = shpes[idx].latest_price

        result.append(subresult)


    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
