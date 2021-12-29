from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from mastermind_py.mastermind.domain import Game, Guess
from mastermind_py.mastermind.repo import Games, Guesses
from mastermind_py.mastermind.schemas import GameSchema, GuessSchema


class MastermindViewset(viewsets.ViewSet):
    def list(self, request):
        games = Games().all()
        
        data, _ = GameSchema(many=True).dump(games)
        return Response(data={'results': data})

    def create(self, request):
        data, errors = GameSchema().load(request.data)
        if errors:
            raise ValidationError(errors)

        game = Game.new(data['num_slots'], data['num_colors'], data['max_guesses'])
        game = Games().save(game)        
        result, _ = GameSchema().dump(game)

        return Response(status=status.HTTP_201_CREATED, data=result)

    def retrieve(self, request, id):
        game = Games().get(id)
        data, _ = GameSchema().dump(game)
        return Response(data=data)


class GuessesViewset(viewsets.ViewSet):
    def create(self, request, id):
        data, errors = GuessSchema().load(request.data)
        if errors:
            raise ValidationError(errors)

        game = Games().get(id)
        guesses = Guesses().getByGame(game)
        game = Game.fromSchema(game, guesses)
        guess, gameStatus = game.add_guess(data['code'])
        game.status = gameStatus
        game = Games().save(game)
        Guesses().save(guess, game)

        guesses = Guesses().getByGame(game)
        guesses = GuessSchema(many=True).dump(guesses)
        result, _ = GameSchema().dump(game)
        result["guesses"] = guesses.data

        return Response(status=status.HTTP_201_CREATED, data=result)
