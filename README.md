## Mastermind Inari exercise

**Mastermind** is a logic board game from the 70’s in which you have to correctly guess a random secret code in a determined number of guesses. 
This game can be played by two players, the *code-maker* and the *code-breaker*.

* The code-maker creates the secret combination, composed by a sequence of 4 colored pegs
- The code-breaker makes a series of guesses, each guess composed in the same way by 4 colores pegs. After each guess, the code-maker gives feedback to the code-breaker to see how close you got to the real secret code.

Each feedback is composed of two numbers, represented by **white pegs** and **black pegs**, and they tell you how your guess and the secret combination compare. Black pegs tell you how many pegs of your guess you have correct in color and position, and white pegs tell you how many pegs of your guess you have correct in color but not in the proper position.

A sample gameplay would be like this:

1. The code-maker has created the secret sequence [Red, Blue, Blue, Red]
2. The code-breaker has ten tries to guess the code. In his first attempt, he/she guesses [Red, Yellow, Green, Blue]
3. The code-maker compares the guess with his solution, and gives him 1 black peg and 1 white peg. 1 Black peg because he guessed correctly the first peg (The red one) in color and position, and 1 white peg because he guessed a Blue peg but in the incorrect position. The code maker never tells you which color or which position you correctly guessed (which is the real fun of the game after all :) )
4. The code-breaker makes another guess now, and tries [Yellow, Yellow, Green, Green]. He/she receives no pegs as feedback because he matched no color against the solution.

5. The gameplay continues until the code-breaker guesses the code correctly correctly or the code-breaker has reached the maximum number of tries allowed without reaching the solution.

To grasp an idea on how this game is played and how it works, you can check out this link and give it a shot:
http://www.webgamesonline.com/mastermind/


Here you have several examples to see how the algorithm to compute the feedback works:


| code | guess | black pegs | white pegs |
| --------|----------|-----------------|-----------------|
RGGB | RGGB  |      4     |      0       (You win!)
RRRR | BYOB  |      0     |      0
GBBR | GBRB  |      2     |      2
BBBR | RBGG  |      1     |      1
RBGG | BBBR  |      1     |      1       (Notice how inverting code and guess does not alter the result)
BBBR | BBRB  |      4     |      0
WBWB | BWBW  |      0     |      4
OOOW | OWWW  |      2     |      0

*Legend: (R)ed, (B)lue, (Y)ellow, (G)reen, (W)hite, (O)range*



You’ll receive a packaged project where you’ll find a small django application that exposes via REST an api to create and play mastermind games.

**We ask you to:**

1. Implement the method `feedback` and `add_guess`, found in the path `mastermind_py/mastermind/domain.py`, inside the `Game` class.
2. Implement a unit test that puts the `feedback` method under test, and checks that, for all the code and guess inputs described in the previous table, you get the expected results.
3. Implement a persistence layer. Right now, the API calls the storage layer, but the storage layer does nothing right now, so nothing you do with the API gets persisted. You can fill the methods of this persistence layer in the path `mastermind_py/mastermind/repo.py`. The typings of the methods should help as a guidance to the implementation.

Also, to retrospect with the code of the project, some questions:

1. What is your favorite package manager for python and why?
2. Do you like the architecture presented in this project? Would you have implemented it differently?
3. Do you know and understand UML? What would the class diagram of the domain exposed in the mastermind game be like for you?
4. What python tools are you aware of to handle things like code styling and consistency, formatting, typing…?
5. Could you tell the difference among a list, a set and a dictionary?
6. Is there anything you would like to comment about the project, this small exercise, etc?
