from logging import *
from sympy import *
import os
import sys

# Mute logging to surpress output of pygame
origStdout = sys.stdout
f = open(os.devnull, 'w')
sys.stdout = f

# Import pygame
import pygame

# Unmute logging
sys.stdout = origStdout
f.close()

def main():
    basicConfig(format='‹%(levelname)s» %(message)s', level=DEBUG)

    if (len(sys.argv) < 2):
        error("Missing arguments.")
        return

    analyze_base_equation(sys.argv[1])
    #generate_base_equation_image()
    #init_pygame()
    
def generate_base_equation_image():
    x = symbols('x')
    expr = sin(sqrt(x**2 + 20)) + 1
    info("Generating image of base equation...")
    preview(expr, viewer='file', filename='output.png', dvioptions=["-T", "tight", "-z", "0", "-bg", "transparent", "--truecolor", "-D 120"])

tokens = []

# Einfaches Scannen nach Variablennamen
def analyze_base_equation(equation):
    in_token = False
    cur_token = ""
    i = 0
    for c in equation:
        debug("(" +str(i)+ ") Aktueller Charakter: " + c)
        if (c == '(' or c == ')' or c == '!' or c == '+' or c == '*'):
            if (len(cur_token)):
                tokens.append(cur_token)
            cur_token = ""
            in_token = False
        else:
            if (not in_token):
                cur_token = c
                in_token = True
            else:
                cur_token = cur_token + c
        debug("(" +str(i)+ ") curToken: " + cur_token)
        debug("=====================")
        i += 1

    for token in tokens:
        debug(token)
    
# Pygame is used to display the results in a window.
def init_pygame():
    pygame.init()

    size = width, height = 800, 400
    white = 255, 255, 255
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Result")

    base_equation = pygame.image.load("output.png")
    base_equation_rect = base_equation.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(white)
        screen.blit(base_equation, base_equation_rect)
        pygame.display.flip()

if __name__ == '__main__':
    main()

class Token:
    def __init__(this, name, **kwargs):
        self.name = name
        info(name)