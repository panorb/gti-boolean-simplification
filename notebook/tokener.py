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

    print(line)
    # Find the variable names and note deepness levels
    # TODO: Nochmal überprüfen, der -1 index muss irgendwie herauslasbar sein.
    # 

    prepare_equation(line)

    # args = []

    # for i in range(len(deepness) - 1, 0, -1):
    #     for j in deepness[i]:
    #         # TODO: Create the element
    #         while True:
    #             k = j
    #             if (line[k] not in reserved_symbols):
                    
    #             if (line[k] == '+' || line[k] == '*'):

def prepare_equation(line):
    base_vars = []
    cur_var = ""
    cur_var_start = 0
    
    reserved_symbols = ['(', ')', '+', '*']
    current_deepness = 0
    deepness = []

    for i in range(len(line)):
        c = line[i]
        print_color = color.END

        if (c == '('):
            current_deepness += 1
            if (len(deepness) <= current_deepness):
                deepness.append([i])
            else:
                deepness[current_deepness].append(i)
            print_color = color.BOLD + color.GREEN
        elif (c == ')'):
            current_deepness -= 1
            deepness[current_deepness].append(i)
            print_color = color.BOLD + color.RED

        if (c not in reserved_symbols):
            if (len(cur_var) == 0):
                cur_var_start = i
            cur_var += c
        elif c in reserved_symbols and len(cur_var) > 0:
            if cur_var not in base_vars:
                token = Token("input", var=cur_var)
                base_vars.append(token)
                line = line[0:cur_var_start] + token.token_id + line[i - 1:len(line)]
                return prepare_equation(line)
            cur_var = ""
        print(print_color + c, end='', flush=True)
    print(color.END)
    print(deepness)

def generate_id():
    return '#' + ''.join(random.choices(string.hexdigits, k=3))