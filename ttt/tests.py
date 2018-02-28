from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Game
from .ai import ai_response
import json


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


class LoginTest(TestCase):
    def test_login(self):
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "flintstone"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)

    def test_unis_active_user(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', is_active=False)
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "flintstone"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)

    def test_wrong_password(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', is_active=True)
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "password"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)

    def test_is_active_user(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', is_active=True)
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "flintstone"}), content_type="application/json")
        expected_status = 'OK'
        self.assertEqual(response.json()['status'], expected_status)


class VerifyTest(TestCase):
    def test_is_active(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', is_active=False)
        user.save()
        c = Client()
        response = c.post('/ttt/verify', json.dumps({"email": "fredflintson@cartoon.network.com", "key": "abracadabra"}), content_type="application/json")
        expected_status = 'OK'
        self.assertEqual(response.json()['status'], expected_status)

    def test_already_is_active(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', is_active=True)
        user.save()
        c = Client()
        response = c.post('/ttt/verify', json.dumps({"email": "fredflintson@cartoon.network.com", "key": "abracadabra"}), content_type="application/json")
        expected_status = 'OK'
        self.assertEqual(response.json()['status'], expected_status)

    def test_user_does_not_exist(self):
        c = Client()
        response = c.post('/ttt/verify', json.dumps({"email": "fredflintson@cartoon.network.com", "key": "abracadabra"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)


class GameModelTest(TestCase):
    def setUp(self):
        username = 'eric'
        password = 'ericson'
        email = 'simpleEric@example.com'
        User.objects.create_user(username=username, password=password, email=email, is_active=True)

    def test_create_game(self):
        grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        user = User.objects.get(username='eric')
        game = Game(user=user)
        game.set_grid(grid)
        game.winner = ' '
        game.save()
        result = game.get_grid()
        for i in range(len(result)):
            self.assertEqual(result[i], ' ')

    def test_create_defaults(self):
        user = User.objects.get(username='eric')
        game = Game(user=user)
        game.save()
        self.assertEqual(game.winner, ' ')
        self.assertIsNotNone(game.start_date)
        grid = game.get_grid()
        for elem in grid:
            self.assertEqual(elem, ' ')


class PlayTest(TestCase):
    def setUp(self):
        username = 'eric'
        password = 'ericson'
        email = 'simpleEric@example.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=True)
        game = Game(user=user)
        game.save()

    def test_ai_response(self):
        user = User.objects.get(username='eric')
        game = Game.objects.get(user=user)
        move = 2
        grid, winner = ai_response(game.get_grid(), move)
        expected_grid = ['O', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        expected_winner = ' '
        self.assertEqual(grid, expected_grid)
        self.assertEqual(winner, expected_winner)

    def test_player_win(self):
        grid = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        move = 5
        grid, winner = ai_response(grid, move)
        expected_grid = ['O', 'O', ' ', 'X', 'X', 'X', ' ', ' ', ' ']
        expected_winner = 'X'
        self.assertEqual(grid, expected_grid)
        self.assertEqual(winner, expected_winner)

    def test_ai_win(self):
        grid = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        move = 8
        grid, winner = ai_response(grid, move)
        expected_grid = ['O', 'O', 'O', 'X', 'X', ' ', ' ', ' ', 'X']
        expected_winner = 'O'
        self.assertEqual(grid, expected_grid)
        self.assertEqual(winner, expected_winner)

    def test_draw(self):
        grid = ['O', 'O', 'X', 'X', 'X', 'O', 'O', ' ', ' ']
        move = 7
        grid, winner = ai_response(grid, move)
        expected_grid = ['O', 'O', 'X', 'X', 'X', 'O', 'O', 'X', 'O']
        expected_winner = ' '
        self.assertEqual(grid, expected_grid)
        self.assertEqual(winner, expected_winner)
