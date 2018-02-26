from django.db import models
from . import fields
import datetime


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=256, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    grid = models.TextField()
    winner = models.CharField(max_length=1, default=' ')

    def __str__(self):
        return self.grid

    def has_winner(self):
        return self.winner != ' ' or ' ' not in self.grid

    def get_score(username):
        user = User.objects.get(username=username)
        query_set = Game.objects.filter(user=user)

        win_count = 0
        lose_count = 0
        tie_count = 0
        for game in query_set:
            if game.winner == 'X':
                win_count += 1
            elif game.winner == 'O':
                lose_count += 1
            elif game.winner == ' ' and ' ' not in game.grid:
                tie_count += 1
        return win_count, lose_count, tie_count
