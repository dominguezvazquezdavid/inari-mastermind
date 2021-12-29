from typing import Any, Dict, List
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from mastermind_py.mastermind.domain import Game
from mastermind_py.mastermind.repo import Games

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    ## Utils
    @staticmethod
    def __createGame(num_slots: int, num_colors: int, max_guesses: int, reference: str,
                    status: str, colors: List[str], secret_code: List[str]) -> Game:
        game = Game(
            id = None,
            num_slots = num_slots,
            num_colors = num_colors,
            max_guesses = max_guesses,
            reference = reference,
            status = status,
            secret_code = secret_code,
            guesses = []
        )
        game.colors = colors

        game = Games().save(game)
        return game
    
    def __assertGuess(self, response: Any, expected_white_peg: int, expected_black_peg: int):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["guesses"][0]["white_pegs"], expected_white_peg)
        self.assertEqual(response.json()["guesses"][0]["black_pegs"], expected_black_peg)

    def test_get_games(self):
        """Check if retrieve all games correctly"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "red", "green", "yellow"])

        response = self.client.get('/api/games/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"][0]), 8)

    def test_get_game(self):
        """Check if retrieve a game correctly"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "red", "green", "yellow"])

        response = self.client.get(f'/api/games/{game.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 8)

    def test_create_game(self):
        """Check if a game is created correctly"""
        response = self.client.post('/api/games/', '{ "num_slots": 4, "num_colors": 4, "max_guesses": 2 }', content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()), 8)
    
    def test_create_guess(self):
        """Check if guess create correctly"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()["guesses"]), 1)
    
    def test_retrieve_guesses(self):
        """Check if guesses are retrieved correctly"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')
        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()["guesses"]), 2)

    def test_none_white_peg(self):
        """Check if return none white peg"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["red", "blue", "yellow", "blue"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')

        self.__assertGuess(response, 0, 0)

    def test_one_white_peg(self):
        """Check if return one white peg"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "blue", "yellow", "blue"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 0)

    def test_two_white_peg(self):
        """Check if return two white peg"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 2, 0)

    def test_three_white_peg(self):
        """Check if return three white peg"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "blue"] }', content_type='application/json')
        
        self.__assertGuess(response, 3, 0)

    def test_four_white_peg(self):
        """Check if return four white peg"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "red", "green", "blue"] }', content_type='application/json')

        self.__assertGuess(response, 4, 0)

    def test_one_black_peg(self):
        """Check if return one black peg"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["green", "orange", "orange", "orange"] }', content_type='application/json')

        self.__assertGuess(response, 0, 1)

    def test_two_black_peg(self):
        """Check if return two black peg"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["green", "blue", "orange", "orange"] }', content_type='application/json')

        self.__assertGuess(response, 0, 2)

    def test_three_black_peg(self):
        """Check if return three black peg"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["green", "blue", "yellow", "orange"] }', content_type='application/json')

        self.__assertGuess(response, 0, 3)

    def test_won_game(self):
        """Check if returned status is won when reach four black peg"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["green", "blue", "yellow", "red"] }', content_type='application/json')

        self.__assertGuess(response, 0, 4)
        self.assertEqual(response.json()["status"], "won")

    def test_lost_game(self):
        """Check if returned status is lost when reach max_guesses"""
        game = self.__createGame(4, 5, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange"], ["green", "blue", "yellow", "red"])

        self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')
        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "orange", "orange", "orange"] }', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["status"], "lost")

    def test_one_black_peg_same_color_guess(self):
        """Check if return only one black peg with same color guess"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "red", "green", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "yellow", "yellow"] }', content_type='application/json')

        self.__assertGuess(response, 0, 1)

    def test_two_black_peg_same_color_guess(self):
        """Check if return two black peg with same color guess"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "yellow", "green", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "yellow", "yellow"] }', content_type='application/json')

        self.__assertGuess(response, 0, 2)

    def test_three_black_peg_same_color_guess(self):
        """Check if return three black peg with same color guess"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["yellow", "yellow", "green", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "yellow", "yellow"] }', content_type='application/json')

        self.__assertGuess(response, 0, 3)        

    def test_one_white_peg_same_color(self):
        """Check if return one white peg with same color"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "blue", "blue", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 0)

    def test_two_white_peg_same_color(self):
        """Check if return two white peg with same color"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "blue", "yellow", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 2, 0)

    def test_one_white_peg_one_black_peg_same_color(self):
        """Check if return one white peg one black peg with same color"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "yellow", "yellow", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 1)

    def test_one_white_peg_two_black_peg_same_color(self):
        """Check if return one white peg two black peg with same color"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "yellow", "yellow", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "yellow", "yellow", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 2)

    def test_one_white_peg_same_color(self):
        """Check if return one white peg when secret code if formed by the same color"""
        game = self.__createGame(4, 4, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow"], ["red", "yellow", "yellow", "yellow"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["yellow", "green", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 0)

#Feedback Unit Test

    def test_One(self):
        """RGGB | RGGB  |      4     |      0"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["red", "green", "green", "blue"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["red", "green", "green", "blue"] }', content_type='application/json')

        self.__assertGuess(response, 0, 4)

    def test_Two(self):
        """RRRR | BYOB  |      0     |      0"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["red", "red", "red", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["blue", "yellow", "orange", "blue"] }', content_type='application/json')

        self.__assertGuess(response, 0, 0)

    def test_Three(self):
        """GBBR | GBRB  |      2     |      2"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["green", "blue", "blue", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["green", "blue", "red", "blue"] }', content_type='application/json')

        self.__assertGuess(response, 2, 2)

    def test_Four(self):
        """BBBR | RBGG  |      1     |      1"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["blue", "blue", "blue", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["red", "blue", "green", "green"] }', content_type='application/json')

        self.__assertGuess(response, 1, 1)

    def test_Five(self):
        """RBGG | BBBR  |      1     |      1"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["red", "blue", "green", "green"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["blue", "blue", "blue", "red"] }', content_type='application/json')

        self.__assertGuess(response, 1, 1)

    def test_Six(self):
        """BBBR | BBRB  |      4     |      0"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["blue", "blue", "blue", "red"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["blue", "blue", "red", "blue"] }', content_type='application/json')

        self.assertNotEqual(response.json()["guesses"][0]["white_pegs"], 0)  
        self.assertNotEqual(response.json()["guesses"][0]["black_pegs"], 4)
        self.__assertGuess(response, 2, 2)

    def test_Seven(self):
        """WBWB | BWBW  |      0     |      4"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["white", "blue", "white", "blue"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["blue", "white", "blue", "white"] }', content_type='application/json')

        self.__assertGuess(response, 4, 0)

    def test_Eight(self):
        """OOOW | OWWW  |      2     |      0"""
        game = self.__createGame(4, 6, 2, "3DB2C149E8", "running", ["red", "blue", "green", "yellow", "orange", "white"], ["orange", "orange", "orange", "white"])

        response = self.client.post(f'/api/games/{game.id}/guesses/', '{ "code": ["orange", "white", "white", "white"] }', content_type='application/json')

        self.__assertGuess(response, 0, 2)