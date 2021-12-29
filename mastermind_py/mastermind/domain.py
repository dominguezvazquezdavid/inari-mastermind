import random
import uuid
from mastermind_py.mastermind.schemas import GameSchema, GuessSchema

from pydash import py_
from typing import Any, List, Tuple


class Colors:
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    BLACK = 'black'
    WHITE = 'white'
    PURPLE = 'purple'
    TURQUOISE = 'turquoise'


colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.ORANGE,
          Colors.WHITE, Colors.PURPLE, Colors.TURQUOISE]


class GameStatus:
    RUNNING = 'running'
    WON = 'won'
    LOST = 'lost'


def create_reference():
    """Generate a default stream name.

    The stream name will be completely random, based on the UUID generator
    passed onto hex format and cutr down to 8 characters. Remeber, UUID4's
    are 32 characters in length, so we cut it
    """
    divider = 3  # Divided by 3 generates 8 characters, by 2, 16 characters
    random_uuid = uuid.uuid4()
    stream_name = random_uuid.hex[:int(len(random_uuid.hex) / divider)]
    return stream_name

class Guess:
    def __init__(self, id: Any, code: str, black_pegs: int, white_pegs: int):
        self.id = id
        self.code = code
        self.black_pegs = black_pegs
        self.white_pegs = white_pegs

class Game:
    def __init__(self, id: Any, reference: str, num_slots: int, num_colors: int,
                 secret_code: List[str], max_guesses: int,
                 status: GameStatus, guesses: List[Guess]):
        self.id = id
        self.reference = reference
        self.num_slots = num_slots
        self.num_colors = num_colors
        self.secret_code = secret_code
        self.max_guesses = max_guesses
        self.status = status
        self.colors = py_.take(colors, num_colors)
        self.guesses = guesses
        
    def add_guess(self, code: List[str]) -> Tuple[Guess, GameStatus]:
        """
        Adds a new guess to the game, and updates the status of the game depending on
        the result.
        """
        if self.status != GameStatus.RUNNING:
            raise Exception('Cannot add a new guess, the game is already finished')
        else:            
            black_pegs, white_pegs = self._feedback(code)
            guess = Guess(None, code, black_pegs, white_pegs)
            if black_pegs == 4:
                self.status = GameStatus.WON
            else:
                if self.max_guesses <= len(self.guesses) + 1:
                    self.status = GameStatus.LOST
            return [guess, self.status]
        # TODO: Implement this. Call the _feedback function, and update the status of the game
        # depending on the result

    def _feedback(self, code: List[str]) -> Tuple[int, int]:
        """
        Compares the given code with the secret code of the game, and returns a tuple
        of the number of (black_pegs, white_pegs)
        """
        # TODO: Implement this
        black_pegs = 0
        white_pegs = 0
        # If secret_code is equal to guess, it is not needed to iterate.
        if self.secret_code == code:
            black_pegs = 4
        else:
            # First, We need to create a dict with color ocurrences in secret code
            color_ocurrences = {}
            for color in self.secret_code:
                if not [gr for gr in color_ocurrences if color in gr]:
                    color_ocurrences[color] = self.secret_code.count(color)

            # Then iterate checking code color and position
            ### Nested loop has a huge cost, but in this case both arrays are short, so it is not a problem
            for x in range(len(code)):
                guess = code[x]
                is_white_peg = False
                for y in range(len(self.secret_code)):
                    if guess == self.secret_code[y]:
                        if x == y:
                            black_pegs += 1
                            # if color ocurrence is 0 means that it encounter before and if is_white_peg means it encounter in this iteration,
                            # so we have to reduce white_pegs
                            if color_ocurrences[guess] == 0 or is_white_peg:
                                white_pegs -= 1
                            else:
                                color_ocurrences[guess] -= 1
                            break
                        else:
                            # if is_white_peg is True, means already encounter another one, so it have not to count it again
                            if color_ocurrences[guess] != 0 and not is_white_peg:
                                white_pegs += 1
                                color_ocurrences[guess] -= 1
                                is_white_peg = True

        return black_pegs, white_pegs 

    @staticmethod
    def new(num_slots: int, num_colors: int, max_guesses: int) -> "Game":
        reference = create_reference().upper()
        chosen_colors = py_.take(colors, num_colors)
        secret_code = random.choices(chosen_colors, k=num_slots)
        return Game(None, reference, num_slots, num_colors,
                    secret_code, max_guesses, GameStatus.RUNNING,
                    [])

    @staticmethod
    def fromSchema(gameSchema: GameSchema, guesses: List[GuessSchema]):
        """Transform from GameSchema to Game"""
        game_guesses = []
        if guesses is not None:
            for guess in guesses:
                game_guesses.append(Guess(guess.id, guess.code, guess.black_pegs, guess.white_pegs))
        return Game(gameSchema.id, gameSchema.reference, 
        gameSchema.num_slots, gameSchema.num_colors, gameSchema.secret_code, 
        gameSchema.max_guesses, gameSchema.status, game_guesses)

