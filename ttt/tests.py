from django.core import mail
from django.test import TestCase, Client
from .models import User
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

    def test_unverified_user(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com')
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "flintstone"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)

    def test_wrong_password(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', verified=True)
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "password"}), content_type="application/json")
        expected_status = 'ERROR'
        self.assertEqual(response.json()['status'], expected_status)

    def test_verified_user(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', verified=True)
        user.save()
        c = Client()
        response = c.post('/ttt/login', json.dumps({"username": "fred", "password": "flintstone"}), content_type="application/json")
        expected_status = 'OK'
        self.assertEqual(response.json()['status'], expected_status)


class VerifyTest(TestCase):
    def test_verified(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', verified=False)
        user.save()
        c = Client()
        response = c.post('/ttt/verify', json.dumps({"email": "fredflintson@cartoon.network.com", "key": "abracadabra"}), content_type="application/json")
        expected_status = 'OK'
        self.assertEqual(response.json()['status'], expected_status)

    def test_already_verified(self):
        user = User(username='fred', password='flintstone', email='fredflintson@cartoon.network.com', verified=True)
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
