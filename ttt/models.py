from django.db import models
from . import fields


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=256, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    grid = fields.ListField()
    winner = models.CharField(max_length=1)

    def __str__(self):
        return self.grid

    def has_winner(self):
        return self.winner != ' '
