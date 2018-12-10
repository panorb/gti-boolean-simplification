import os
import string
from tabulate import tabulate
from IPython.core.display import display, HTML

reserved_symbols = ['(', ')', '+', '*', '!']

showInputGeneration = os.getenv("SHOW_INPUT_GENERATION", False) == "True"

def simplify(equation):
    prez_solve(equation)
    return

def prez_solve(equation):
    
    base_vars = []

    cur_var = ""
    
    for i in range(len(equation)):
        c = equation[i]
        if (c not in reserved_symbols):
            cur_var += c
        if (c in reserved_symbols or i == len(equation) - 1) and len(cur_var) > 0:
            if cur_var not in base_vars:
                base_vars.append(cur_var)
            cur_var = ""
    
    # [["a", 0], ["b", 0], ["x_1", 1]]
    prez_display = []

    for i in range(pow(2, len(base_vars))):
        prez_values = [str(i)]
        values = []

        for j in range(len(base_vars) - 1, -1, -1):
            divisor = i // pow(2, j) # TODO: Besseren Variablennamen ausdenken
            value = divisor % 2 != 0
            values.append([base_vars[len(base_vars) - j - 1], value])
            if (value): prez_values.append("1")
            else: prez_values.append("0")
        
        print("======")
        print(values)
        prep_equ = prepare_compute(equation, values)
        #depth = analyze_for_depth(equation)
        result = compute(prep_equ)

        if (result): prez_values.append("1")
        else: prez_values.append("0")

        prez_display.append(prez_values)
    
    display_base_vars = base_vars.copy()
    display_base_vars.insert(0, "DEZ")
    display_base_vars.append("RES")
    if (showInputGeneration): print(tabulate(prez_display, headers=display_base_vars, tablefmt='orgtbl'))

def compute(equation):
    print("eq " + equation)
    depth = analyze_for_depth(equation)
    print(depth)
    start = depth[len(depth)-1][0]
    end = equation[start:len(equation)].find(')') + start
    if (end == -1):
        start = 0
        end = len(equation)
    
    # print("equation[start=" + str(start) + "] =" + equation[start])
    # print("equation[end=" + str(end) + "] =" + equation[end])

    if (len(equation) == 1):
        return char_to_bool(equation[0])

    equation = equation[0:start] + bool_to_char(partial_compute(equation, start, end, False)) + equation[end+1:len(equation)]
    return compute(equation)

def partial_compute(equation, start, end, invert):
    result = None
    combinator = 'c'
    
    for i in range(start + 1, end):
        if equation[i] == '0' or equation[i] == '1':
            result = combine(combinator, result, char_to_bool(equation[i]))
        elif equation[i] == '!':
            # TODO: Implement Negator
            continue
        elif equation[i] == '*':
            combinator = '*'
        elif equation[i] == '+':
            combinator = '+'
    
    return result

def char_to_bool(char):
    if (char == '1'):
        return True
    return False

def bool_to_char(bool):
    if (bool):
        return '1'
    return '0'

def combine(combinator, a, b):
    if (combinator == '+'): # OR
        print("... OR ...")
        print("." + bool_to_char(a) + ". OR ." + bool_to_char(b) + ". = " + bool_to_char(a or b))
        return a or b
    elif (combinator == '*'): # AND
        print("... AND ...")
        print("." + bool_to_char(a) + ". AND ." + bool_to_char(b) + ". = " + bool_to_char(a and b))
        return a and b
    elif (combinator =='c'):
        print("CONSTANT ...")
        print("CONSTANT ." + bool_to_char(b) + ".")
        return b
    print("Combine reached end, combinaor has no known value.")

def prepare_compute(equation, values):
    for pair in values:
        if (pair[1]): equation = equation.replace(pair[0], "1")
        else: equation = equation.replace(pair[0], "0")
    # print(equation)
    return "(" + equation + ")"

def analyze_for_depth(equation):
    current_depth = 0
    depth = [[0]]

    for i in range(len(equation)):
        c = equation[i]
        if (c == '('):
            current_depth += 1
            if (len(depth) <= current_depth):
                depth.append([i])
            else:
                depth[current_depth].append(i)
        elif (c == ')'):
            current_depth -= 1
            # if (len(depth) <= current_depth):
            #     depth[current_depth].append(i)
            # else:
            #     depth.insert(current_depth, [i])
    
    return depth

def prez_output_depth(equation):
    depth = analyze_for_depth(equation)
    
    for i in range(len(equation)):
        print(equation[i], end='', flush=True)
        for j in range(len(depth)):
            if i in depth[j]:
                print("    == Depth #" + str(j))


def value(values, key):
    for value in values:
        if values[0] == key: return value[1]
    
    print("Tried to access value of " + key)
    print("Values is " + values)
    raise ValueError()
