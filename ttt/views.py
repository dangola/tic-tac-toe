from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
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
        elif 'login-form' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username)
            if user.password == password:
                return redirect('index')
            else:
                return redirect('adduser')
    else:
        signupform = SignupForm()
        loginform = LoginForm()
        return render(request, 'ttt/login.html', {'signupform': signupform, 'loginform': loginform})    