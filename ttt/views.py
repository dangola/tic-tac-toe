from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.template import loader
import json
from .forms import NameForm
from .ai import ai_move


@require_http_methods(["POST"])
def play(request):
    data = json.loads(request.body)
    grid = data['grid']
    response = ai_move(grid)
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
