import json
from mastermind_py.mastermind.domain import Game, Guess
from mastermind_py.mastermind.models import GameModel, GuessModel
from typing import List


class Games:
    def all(self) -> List[Game]:
        """
        Returns all the stored games in the system
        """
        return GameModel.objects.all()

    def save(self, game: Game) -> Game:
        """
        Saves the game into a database
        """
        if len(GameModel.objects.filter(id = game.id)):
            game_model = GameModel.objects.filter(id = game.id)[0]
            game_model.status = game.status
        else:
            game_model = GameModel(reference = game.reference, num_slots = game.num_slots, num_colors = game.num_colors, colors= game.colors, 
                    secret_code = game.secret_code, max_guesses = game.max_guesses, status = game.status)

        game_model.save()

        return GameModel.objects.filter(id = game_model.id)[0]

    def get(self, id: int) -> Game:
        """
        Returns a single game by ID
        """

        game = GameModel.objects.filter(id = id)
        return game[0] if len(game) > 0 else {}
        
class Guesses:
    def all(self) -> List[Guess]:
        """
        Returns all the stored guesses in the system
        """
        return GuessModel.objects.all()

    def save(self, guess: Guess, game: GameModel) -> Guess:
        """
        Saves the guess into a database
        """
        if len(GuessModel.objects.filter(id = guess.id)):
            raise Exception("You can not update a guess")
        else:
            guess = GuessModel(code = guess.code, black_pegs = guess.black_pegs, white_pegs = guess.white_pegs, game = game)

        guess.save()

        return GuessModel.objects.filter(id = guess.id)[0]

    def get(self, id: int) -> Guess:
        """
        Returns a single guess by ID
        """

        guess = GuessModel.objects.filter(id = id)
        return guess[0] if len(guess) > 0 else {}
        
    def getByGame(self, game: GameModel) -> List[Guess]:
        """
        Returns a a list of Guess by game
        """

        guesses = GuessModel.objects.filter(game = game)
        return guesses if len(guesses) > 0 else []