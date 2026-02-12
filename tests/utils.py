""" Utils for tests """

import string
from random import randint
from sys import maxsize as MAX_INT

MIN_INT = -MAX_INT - 1

BOUCLE_TEST = 100
TAILLE_STR = 100

def generate_random_string(length:int) -> str:
    """ Generate a random string of given length (the string only contains letters) """
    letters = string.ascii_letters
    return ''.join(letters[randint(0, len(letters) - 1)] for _ in range(length))
