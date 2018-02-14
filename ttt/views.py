from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.template import loader
import json
from .forms import NameForm
from .ai import ai_move


def get_name(request):
    # if this is a POST request we need to process the form data
    print request.body
    if request.method == 'POST':
        template = loader.get_template('ttt/play.html')
        context = {
            'name': request.POST.get('name')
        }
        return HttpResponse(template.render(context, request))
        # return HttpResponseRedirect(reverse('play'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'ttt/index.html', {'form': form})


@require_http_methods(["POST"])
def play(request):
    # template = loader.get_template('ttt/play.html')
    print 'Request: ' + request.body
    data = json.loads(request.body)
    grid = data['grid']
    response = ai_move(grid)
    print response
    context = {
        'grid': response['grid']
    }
    return JsonResponse(response)


def index(request):
    if request.method == 'POST':
        template = loader.get_template('ttt/play.html')
        context = {
            'name': request.POST.get('name'),
        }
        return HttpResponse(template.render(context, request))
    else:
        form = NameForm()
        return render(request, 'ttt/index.html', {'form': form})


def ttt(request):
    return render(request, 'ttt/ttt.html')
