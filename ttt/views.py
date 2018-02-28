from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .ai import ai_response
from .models import User
from .models import Game
import json


@csrf_exempt
@api_view(['POST'])
def play(request):
    response = ai_response(request)

    if 'game_id' in request.session and request.session['game_id'] is not None:
        game = Game.objects.get(id=request.session['game_id'])
        game.grid = json.dumps(response['grid'])
        game.winner = json.dumps(response['winner'])
        game.save()
    else:
        user = User.objects.get(username=request.session['username'])
        game = Game(user=user, grid=json.dumps(response['grid']), winner=json.dumps(response['winner']))
        game.save()
        request.session['game_id'] = game.id

    if game.has_winner():
        del request.session['game_id']
    return JsonResponse(response)


@csrf_exempt
@api_view(['GET'])
def index(request):
    return render(request, 'ttt/index.html', {})


@csrf_exempt
@api_view(['POST'])
def adduser(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'ERROR'})
    else:
        user = User(username=username, password=password, email=email)
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
@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    try:
        user = User.objects.get(username=username)
        if user.password == password and user.verified is True:
            request.session['username'] = username
            return JsonResponse({'status': 'OK'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'ERROR'})
    return JsonResponse({'status': 'ERROR'})


@csrf_exempt
@api_view(['POST'])
def logout(request):
    request.session.clear()
    return JsonResponse({'status': 'OK'})


@csrf_exempt
@api_view(['POST'])
def verify(request):
    response = {}
    try:
        email = request.data['email']
        key = request.data['key']
        user = User.objects.get(email=email)

        if user.verified:
            response = {'status': 'OK'}
        elif key == 'abracadabra':
            user.verified = True
            user.save()
            response = {'status': 'OK'}
        else:
            response = {'status': 'ERROR'}

        return JsonResponse(response)
    except User.DoesNotExist:
        response = {'status': 'ERROR'}
        return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
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
@api_view(['POST'])
def getgame(request):
    try:
        game_id = request.data['id']
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
@api_view(['POST'])
def getscore(request):
    user = User.objects.get(username=request.session['username'])
    win, lose, tie = Game.get_score(user)
    response = {}
    response['status'] = 'OK'
    response['human'] = win
    response['wopr'] = lose
    response['tie'] = tie
    return JsonResponse(response)
