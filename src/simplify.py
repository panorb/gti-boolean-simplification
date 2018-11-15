from logging import *
from sympy import *
import pygame

def main():
    basicConfig(format='%(message)s', level=INFO);
    x = symbols('x')
    expr = sin(sqrt(x**2 + 20)) + 1
    info("Generating image of base equation...")
    preview(expr, viewer='file', filename='output.png', dvioptions=["-T", "tight", "-z", "0", "-bg", "transparent", "--truecolor", "-D 800"])

if __name__ == '__main__':
    main()