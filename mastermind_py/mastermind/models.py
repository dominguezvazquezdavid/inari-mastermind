from typing_extensions import Required
from django.db import models
from typing import List
from django.contrib.postgres.fields import JSONField

class GameModel(models.Model):
    reference = models.CharField(max_length=256)
    num_slots = models.PositiveIntegerField()
    num_colors = models.PositiveIntegerField()
    max_guesses = models.PositiveIntegerField()
    secret_code = JSONField()
    status = models.CharField(max_length=256)
    colors = JSONField()
    registration_datetime = models.DateTimeField(auto_now_add=True)
    
class GuessModel(models.Model):
    code = models.CharField(max_length=256)
    black_pegs = models.PositiveIntegerField()
    white_pegs = models.PositiveIntegerField()
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE)