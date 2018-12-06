import string
import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Token:
    def __init__(self, token_type, **kwds):
        self.token_type = token_type
        self.token_id = generate_id()

        if (self.token_type == "input"):
            self.var = kwds["var"]
        elif (self.token_type == "and" or self.token_type == "or"):
            self.inputs = kwds["inputs"]
        elif (self.token_type == "not"):
            self.input = kwds["input"]

def create_tokens(line):
    line = "(a+(b*c_1))+((c_1*c_2)+(c_2*a))"
    reserved_symbols = ['(', ')', '+', '*']

    base_vars = []
    cur_var = ""

    current_deepness = 0
    deepness = [[0]]

    print(line)
    # Find the variable names and note deepness levels
    for i in range(len(line)):
        c = line[i]
        print_color = color.END

        if (c == '('):
            current_deepness += 1
            if (len(deepness) >= current_deepness):
                deepness.append([i])
            else:
                deepness[current_deepness].append(i)
            print_color = color.BOLD + color.GREEN
        elif (c == ')'):
            current_deepness -= 1
            deepness[current_deepness].append(i)
            print_color = color.BOLD + color.RED

        if (c not in reserved_symbols):
            cur_var += c
        elif c in reserved_symbols and len(cur_var) > 0:
            if cur_var not in base_vars:
                token = Token("input", var=cur_var)
                base_vars.append(token)
            cur_var = ""
        print(print_color + c, end='', flush=True)
    
    print(color.END)
    



    for element in base_vars:
        print(element.token_type + " " + element.token_id)

def generate_id():
    return '#' + ''.join(random.choices(string.hexdigits, k=3))