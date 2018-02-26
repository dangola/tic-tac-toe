from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import loader
from .forms import NameForm
from .forms import SignupForm
from .forms import LoginForm
from .ai import ai_response
from .models import User
from .models import Game
import json, copy


@csrf_exempt
@require_http_methods(["POST"])
def play(request):
    response = ai_response(request)

    # if id exists, update game
    # else, create new game

    # if has winner, remove from session

    if 'game_id' in request.session:
        game_id = request.session['game_id']
        game = Game.objects.get(id=game_id)
        game.grid = json.dumps(response['grid'])
        game.save()
    else:
        user = User.objects.get(username=request.session['username'])

        game = Game(user_id=user.id, grid=json.dumps(response['grid']))
        game.save()
        request.session['game_id'] = game.id

    if response['winner'] != ' ' or ' ' in response['grid']:
        game.winner = response['winner']

    return JsonResponse(response)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        template = loader.get_template('ttt/play.html')
        context = {
            'username': request.POST.get('name'),
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
                account = form.save()
                msg_html = loader.render_to_string('ttt/email_verification.html', {'url': '/ttt/verify', 'email': account.email, 'key': 'abracadabra'})
                send_mail(
                    'Subject Here',
                    msg_html,
                    'auto_generated@wer.cloud.compas.stonybrook.edu',
                    [account.email],
                    html_message=msg_html,
                    fail_silently=False
                )
                return HttpResponse('Account made')
            else:
                return HttpResponse('Email already in use')
    else:
        signupform = SignupForm()
        return render(request, 'ttt/register.html', {'signupform': signupform})


def login(request):
    # use built-in authenticator and user models
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.password == password:
                grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];
                response = render(request, 'ttt/play.html', {'username': username, 'grid': grid})
                response.set_cookie('username', username)
                request.session['username'] = username

                return response

    if 'username' in request.session:
        if 'game_id' in request.session and request.session['game_id'] != None:
            game = Game.objects.get(id=request.session['game_id'])
            grid = json.loads(game.grid)
        else:
            grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

        return render(request, 'ttt/play.html', {"username": request.session['username'], 'grid': grid})

    loginform = LoginForm()
    return render(request, 'ttt/login.html', {'loginform': loginform})


def logout(request):
    request.session.clear()
    loginform = LoginForm()
    return render(request, 'ttt/login.html', {'loginform': loginform})


@csrf_exempt
def verify(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = get_object_or_404(User, email=body['email'])
            key = body['key']

            if user.verified:
                message = 'Account already verified.'
            elif key == 'abracadabra':
                user.verified = True
                user.save()
                message = 'Your account has been verified.'
            else:
                message = 'Verification key is wrong.'

            html = loader.render_to_string('ttt/verify.html', {'message': message})
            return HttpResponse(html)
        except User.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'ttt/email_verification.html', {'url': '/ttt/verify', 'email': 'admin@example.com', 'key': 'abracadabra'})


def listgames(request):
    if 'username' in request.session:
        return


def getgame(request):
    return


def getscore(request):
    return