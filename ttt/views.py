from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .ai import ai_response
from .models import Game, Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
import traceback


def getSessionData(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            session = Session.objects.get(user=user)
            return session.game_id
        except:
            return None
    return None


def setSessionData(request, value):
    if request.user.is_authenticated:
        user = request.user
        try:
            session = Session.objects.get(user=user)
            session.game_id = value
            session.save()
        except Session.DoesNotExist:
            session = Session(user=user, game_id=value)
            session.save()


def deleteSessionData(request):
    if request.user.is_authenticated:
        user = request.user
        Session.objects.get(user=user).delete()


@csrf_exempt
@require_http_methods(["POST"])
def play(request):
    body = json.loads(request.body.decode('utf-8'))
    response = {}
    move = json.loads(body['move'])
    print(move)
    username = request.session['username']
    print(username)
    user = User.objects.get(username=username)

    game_id = getSessionData(request)
    if game_id is not None:
        print('Resuming old session from game_id')
        print(game_id)
        game = Game.objects.get(id=game_id)
        grid, game.winner = ai_response(game.get_grid(), move)
        game.set_grid(grid)
        game.save()

    else:
        print('Creating new game')
        game = Game(user=user)
        grid = game.get_grid()
        grid, game.winner = ai_response(grid, move)
        game.set_grid(grid)
        game.save()
        setSessionData(request, game.id)
        print(game.id)
        print(grid)

    response['grid'] = game.get_grid()
    response['winner'] = game.winner
    if game.has_winner():
        deleteSessionData(request)

    return JsonResponse(response)


def index(request):
    return render(request, 'ttt/index.html', {})


@require_http_methods(["POST"])
def adduser(request):
    body = json.loads(request.body.decode('utf-8'))
    username = body['username']
    password = body['password']
    email = body['email']

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'ERROR'})
    else:
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
        user.save()
        msg_html = loader.render_to_string('ttt/email_verification.html', {'url': '/ttt/verify', 'email': email, 'key': 'abracadabra'})
        send_mail(
            'Subject Here',
            msg_html,
            'auto_generated@wer.cloud.compas.stonybrook.edu',
            [email],
            html_message=msg_html,
            fail_silently=False
        )
        return JsonResponse({'status': 'OK'})


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    body = json.loads(request.body.decode('utf-8'))
    username = body['username']
    password = body['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        request.session['username'] = username
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'ERROR'})


@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    try:
        logout(request)
    except Exception:
        print(traceback.format_exc())
    return JsonResponse({'status': 'OK'})


@csrf_exempt
@require_http_methods(["POST"])
def verify_user(request):
    body = json.loads(request.body.decode('utf-8'))
    response = {}
    try:
        email = body['email']
        key = body['key']
        user = User.objects.get(email=email)

        if user.is_active:
            response = {'status': 'OK'}
        elif key == 'abracadabra':
            user.is_active = True
            user.save()
            response = {'status': 'OK'}
        else:
            response = {'status': 'ERROR'}

        return JsonResponse(response)
    except User.DoesNotExist:
        response = {'status': 'ERROR'}
        return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def listgames(request):
    response = {}
    response['status'] = 'OK'
    user = User.objects.get(username=request.session['username'])
    games = Game.objects.filter(user=user)
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
@require_http_methods(["POST"])
def getgame(request):
    body = json.loads(request.body.decode('utf-8'))
    try:
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
    except Game.DoesNotExist:
        response = {'status': 'ERROR'}
        return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def getscore(request):
    user = User.objects.get(username=request.session['username'])
    win, lose, tie = Game.get_score(user)
    response = {}
    response['status'] = 'OK'
    response['human'] = win
    response['wopr'] = lose
    response['tie'] = tie
    return JsonResponse(response)
