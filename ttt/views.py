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
import json


@csrf_exempt
@require_http_methods(["POST"])
def play(request):
    response = ai_response(request)

    # if id exists, update game
    # else, create new game

    # if has winner, remove from session

    if 'game_id' in request.session and request.session['game_id'] != None:
        game_id = request.session['game_id']
        game = Game.objects.get(id=game_id)
        game.grid = json.dumps(response['grid'])
        game.save()
    else:
        user = User.objects.get(username=request.session['username'])
        game = Game(user_id=user.id, grid=json.dumps(response['grid']))
        game.save()
        request.session['game_id'] = game.id

    if response['winner'] != ' ' or ' ' not in response['grid']:
        game.winner = response['winner']
        game.save()
        del request.session['game_id']

    print(request.user.id)

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

        if 'username' in request.COOKIES and request.COOKIES['username']:
            if request.COOKIES['username'] == username:
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    grid = lastplayed(user)
                    request.session['username'] = username
                    response = render(request, 'ttt/play.html', {'username': request.COOKIES['username'], 'grid': grid})
                    return response

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.password == password:
                if user.verified == True:
                    grid = lastplayed(user)
                    response = render(request, 'ttt/play.html', {'username': username, 'grid': grid})
                    response.set_cookie('username', user.username)
                    request.session['username'] = username
                    return response
                else:
                    return HttpResponse('user not verified')

    if 'username' in request.session and request.session['username']:
        if User.objects.filter(username=request.session['username']).exists():
            user = User.objects.get(username=request.session['username'])
            grid = lastplayed(user)
        return render(request, 'ttt/play.html', {'username': user.username, 'grid': grid})

    loginform = LoginForm()
    return render(request, 'ttt/login.html', {'loginform': loginform})


def lastplayed(user):
    return Game.objects.filter(user_id=user.id).order_by('-id')[0]


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
    response = {}
    response['status'] = 'OK'
    user = User.objects.get(username=request.session['username'])
    games = Game.objects.filter(user_id=user.id)
    games_data = []
    for item in games:
        game = {
            'id': item.id,
            'start_date': item.start_date
        }
        games_data.append(game)
    response['games'] = games_data
    return JsonResponse(response)


@csrf_exempt
def getgame(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            game_id = body['id']
            game = Game.objects.get(id=game_id)
            if request.session['username']:
                user = User.objects.get(username=request.session['username'])
                if user.id == game.user_id:
                    response = {}
                    response['status'] = 'OK'
                    response['grid'] = game.grid
                    response['winner'] = game.winner
            else:
                raise User.DoesNotMatch
            return JsonResponse(response)
        except (Game.DoesNotExist, User.DoesNotMatch):
            response = { 'status': 'ERROR' } 
            return JsonResponse(response)
    return HttpResponseNotFound('<h1>Page not found</h1>')


@csrf_exempt
def getscore(request):
    user = User.objects.get(username=request.session['username'])
    win, lose, tie = Game.get_score(user)
    response = {}
    response['status'] = 'OK'
    response['human'] = win
    response['wopr'] = lose
    response['tie'] = tie
    return JsonResponse(response)
