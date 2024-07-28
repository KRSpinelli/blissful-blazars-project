import random
import os
from typing import Tuple

"""
Authored by e-Kretén (feketehun0r)
Python Offical CodeJam '24
FINAL BUILD PUSHED 07/27/2024 10:50 PM EST
** THIS CODE IS UNMAINTAINED**
"""



with open(os.path.join(__file__, "..", "questions.txt")) as f:
    questions = f.read().split("\n\n")


def get() -> Tuple[str, str, str, str]:
    question = random.choice(questions)
    if "|" in question:
        question = question.split("|")
        question[2] = str(question[2]).replace(" ","")
        print(f"|{question[2]}|")
        return question
