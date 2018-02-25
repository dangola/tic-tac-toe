from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import loader
from .forms import NameForm
from .forms import SignupForm
from .forms import LoginForm
from .ai import ai_response
from .models import User


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
        if 'register-form' in request.POST:
            if form.is_valid():
                account = form.save(commit=False)
                account.verified = True
                account.save()
                send_mail(
                    'Subject Here',
                    'key word abracadabra',
                    'from@example.com',
                    [account.email],
                    fail_silently=False
                )
                return HttpResponse('account made')
            else:
                return HttpResponse('email already in use')
                # separate login and registration
        elif 'login-form' in request.POST:
            login(request)
    else:
        signupform = SignupForm()
        return render(request, 'ttt/register.html', {'signupform': signupform})

def login(request):
    # use built-in authenticator and user models
    if 'login-form' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'username': username,
            'password': password
        }
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.password == password:
                template = loader.get_template('ttt/play.html')
                response = HttpResponse(template.render(context, request))
                response.set_cookie(username+password)
                return response
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    elif 'register-form' in request.POST:
        adduser(request)
    else:
        loginform = LoginForm()
        return render(request, 'ttt/login.html', {'loginform': loginform})
