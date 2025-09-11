# bad_code.py

import os  # unused import -> triggers Pylint warning


def add_numbers(a, b, c):  # too many arguments (triggers warning)
    return a + b + c


def unused_function():  # unused function -> warning
    pass


x = 1
y = 2
print(x + y)   # print statement is fine, but global variables trigger warnings
