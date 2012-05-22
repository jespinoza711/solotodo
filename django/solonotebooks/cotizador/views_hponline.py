from django.shortcuts import render_to_response
from solonotebooks.cotizador.forms.hponline_search_form import HponlineSearchForm

def index(request):
    notebook = None
    shpe = None

    if 'submit' in request.GET:
        form = HponlineSearchForm(request.GET)
        if form.is_valid():
            notebook, shpe = form.find_best_notebook()
        else:
            form = HponlineSearchForm()
    else:
        form = HponlineSearchForm()

    processor_tuple = []
    graphics_tuple = []
    mobility_tuple = []

    if notebook:
        if notebook.processor.speed_score < 1600:
            processor_tuple = [25, 'danger']
        elif notebook.processor.speed_score < 2400:
            processor_tuple = [50, 'warning']
        elif notebook.processor.speed_score < 3900:
            processor_tuple = [75, 'success']
        else:
            processor_tuple = [100, 'primary']

        vc = notebook.video_card.order_by('-speed_score')[0]

        if vc.speed_score < 3200:
            graphics_tuple = [25, 'danger']
        elif vc.speed_score < 5000:
            graphics_tuple = [50, 'warning']
        elif vc.speed_score < 7500:
            graphics_tuple = [75, 'success']
        else:
            graphics_tuple = [100, 'primary']

        screen_mobility_normalized_score = (notebook.screen.size.family.base_size - 10) / 6.0
        cpu_mobility_normalized_score = (notebook.processor.consumption - 1) / 4.0

        mobility_score = (screen_mobility_normalized_score + cpu_mobility_normalized_score) / 2.0

        # The less the more mobile it is
        if mobility_score > 0.75:
            mobility_tuple = [25, 'danger']
        elif mobility_score > 0.50:
            mobility_tuple = [50, 'warning']
        elif mobility_score > 0.25:
            mobility_tuple = [75, 'success']
        else:
            mobility_tuple = [100, 'primary']

        print screen_mobility_normalized_score
        print cpu_mobility_normalized_score

    return render_to_response('hponline/index.html', {
        'form': form,
        'notebook': notebook,
        'shpe': shpe,
        'processor_tuple': processor_tuple,
        'graphics_tuple': graphics_tuple,
        'mobility_tuple': mobility_tuple
    })