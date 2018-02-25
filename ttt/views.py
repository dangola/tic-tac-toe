from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import loader
from .forms import NameForm
from .forms import SignupForm
from .forms import LoginForm
from .ai import ai_response


@csrf_exempt
@require_http_methods(["POST"])
def play(request):
    response = ai_response(request)
    return JsonResponse(response)


@csrf_exempt
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

def adduser(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.verified = True
            account.save()
            return HttpResponse('account made')
    else:
        signupform = SignupForm()
        loginform = LoginForm()
        return render(request, 'ttt/login.html', {'signupform': signupform, 'loginform': loginform})