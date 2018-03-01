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
import datetime


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
    move = body['move']
    user = request.user
    try:
        session_id = request.COOKIES.get('sessionid')
        if Session.objects.filter(session_id=session_id).exists():
            session = Session.objects.get(session_id=session_id)
        else:
            session = Session(session_id=session_id)

        if move is None:
            response['grid'] = session.get_grid()
            response['winner'] = session.winner
            return JsonResponse(response)

        if session.started is False:
            session.started = True
            session.start_date = datetime.datetime.now()

        grid = session.get_grid()
        grid, session.winner = ai_response(grid, move)
        session.set_grid(grid)
        session.save()

        response['grid'] = session.get_grid()
        response['winner'] = session.winner
        if session.has_winner():
            game = Game(user=user, start_date=session.start_date, winner=session.winner)
            game.set_grid(session.get_grid())
            game.save()
            session.reset()
        return JsonResponse(response)
    except:
        tb = traceback.format_exc()
        return HttpResponse(tb)


def index(request):
    return render(request, 'ttt/index.html', {})


@csrf_exempt
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
        response = JsonResponse({'status': 'OK'})
        response.set_cookie('username', username)
        return response
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
    try:
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        games = Game.objects.filter(user=user)
        games_data = []
        for item in games:
            game = {
                'id': item.id,
                'start_date': item.start_date
            }
            games_data.append(game)
        response['games'] = games_data
        response['status'] = 'OK'
        return JsonResponse(response)
    except:
        response = {'status': 'ERROR'}
        return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def getgame(request):
    body = json.loads(request.body.decode('utf-8'))
    try:
        username = request.COOKIES.get('username')
        game_id = body['id']
        game = Game.objects.get(id=game_id)
        user = User.objects.get(username=username)
        if user.id == game.user_id:
            response = {}
            response['status'] = 'OK'
            response['grid'] = game.grid
            response['winner'] = game.winner
        else:
            raise User.DoesNotMatch
        return JsonResponse(response)
    except:
        response = {'status': 'ERROR'}
        return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def getscore(request):
    try:
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        win, lose, tie = Game.get_score(user)
        response = {}
        response['status'] = 'OK'
        response['human'] = win
        response['wopr'] = lose
        response['tie'] = tie
        return JsonResponse(response)
    except:
        response = {'status': 'ERROR'}
        return JsonResponse(response)
