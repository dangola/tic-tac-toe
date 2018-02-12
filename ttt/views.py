from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

@csrf_exempt
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse()
           # return render(request, 'ttt/play.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'ttt/index.html', {'form': form})

def get_move(request):
    if request.method == 'POST':
        response_data['winner'] = 'X';
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def index(request):
    return render(request, 'ttt/index.html')
def ttt(request):
    return render(request, 'ttt/ttt.html')