from enum import Enum
from typing import Any
import src.questions as question_module
NUMBER_OF_ROUNDS = 5

"""
Authored by CH4RM (ch4rm)
Python Offical CodeJam '24
FINAL BUILD PUSHED 07/27/2024 10:50 PM EST
** THIS CODE IS UNMAINTAINED**
"""

class Verdict(Enum):
    FALSE = 0
    MOSTLY_FALSE = 1
    UNPROVEN = 2
    MOSTLY_TRUE = 3
    TRUE = 4


class Question:
    def __init__(self, question: str, description: str, answer: str, explanation: str):
        """
        Initialize the components of a question.
        """
        self._question = question
        self._description = description
        self._answer = Verdict[answer]
        self._explanation = explanation

    def get_question(self) -> str:
        """
        Getter for the question variable.
        """
        return self._question

    def get_description(self) -> str:
        """
        Getter for the description variable.
        """
        return self._description

    def get_answer(self) -> int:
        """
        Getter for the answer variable.
        """
        return self._answer.value

    def get_explanation(self) -> str:
        """
        Getter for the explanation variable.
        """
        return self._explanation


class Game:
    def __init__(self, user: str):
        self._current_question = None
        self._user = user
        self._score = 0
        self._final_score = -1
        self._difference = None
        self._rounds_remaining = NUMBER_OF_ROUNDS

    def get_question(self) -> Question:
        """
        Getter for the current_question variable.
        """
        return self._current_question

    def get_score(self) -> int:
        """
        Getter for the score variable.
        """
        return self._score

    def get_difference(self) -> int:
        """
        Getter for the difference variable.
        """
        return self._difference

    def get_rounds_remaining(self) -> int:
        """
        Getter for the rounds_remaining variable.
        """
        return self._rounds_remaining

    def _load_new_question(self):
        """
        Load a new question from the question module.
        """
        question, description, answer, explanation = question_module.get()
        self._current_question = Question(question, description, answer, explanation)

    def _calculate_difference(self, user_guess: str) -> int:
        """
        Calculate the difference between the user's guess and the correct answer.
        """
        user_guess = Verdict[user_guess]
        self._difference = abs(self._current_question.get_answer() - user_guess.value)

    def _calculate_score(self, difference: int):
        """
        Calculate the score based on the difference between the user's guess and the correct answer.
        """
        if difference == 0:
            self._score += 10000
        else:
            self._score += 10000 - ((difference + 1) * 2000)

    def attempt_answer(self, user_guess: str):
        """
        Check the user's answer and return the result.
        """
        result_output = ""

        self._calculate_difference(user_guess)
        self._calculate_score(self._difference)

    def start_new_round(self) -> bool:
        """
        Start a new round of the game.
        Returns True if new Round. Returns False if Game Over.
        """
        if self._rounds_remaining <= 0:
            self._end_game()
            return False

        else:
            self._rounds_remaining -= 1
            self._load_new_question()
            return True

    def get_final_score(self):
        """Returns final score. -1 if game has not ended."""
        return self._final_score
    def _end_game(self):
        """
        End the game and record the final score.
        """
        self._final_score = self._score

