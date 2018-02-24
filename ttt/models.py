from django.db import models
from . import fields


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=256)
    verified = models.BooleanField()


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    grid = fields.ListField()
    winner = models.CharField(max_length=1)
