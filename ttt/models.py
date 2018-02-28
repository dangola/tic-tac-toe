from django.db import models
from django.contrib.auth.models import User
import json


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    grid = models.CharField(max_length=100, default=json.dumps([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']))
    winner = models.CharField(max_length=1, default=' ')

    def __str__(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = json.dumps(grid)

    def get_grid(self):
        return json.loads(self.grid)

    def has_winner(self):
        return self.winner != ' ' or ' ' not in self.grid

    def get_score(user):
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


class Session(models.Model):
    session_id = models.CharField(max_length=255, default='abracadabra')
    start_date = models.DateTimeField(auto_now_add=True)
    grid = models.CharField(max_length=100, default=json.dumps([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']))
    winner = models.CharField(max_length=1, default=' ')
    started = models.BooleanField(default=False)
    username = models.CharField(max_length=200)

    def set_grid(self, grid):
        self.grid = json.dumps(grid)

    def get_grid(self):
        return json.loads(self.grid)

    def has_winner(self):
        board = json.loads(self.grid)
        return self.winner != ' ' or ' ' not in board

    def reset(self):
        self.grid = json.dumps([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
        self.winner = ' '
        self.started = False
        self.save()
