import os
import string
from tabulate import tabulate
from IPython.core.display import display, HTML

reserved_symbols = ['(', ')', '+', '*', '!']

# # Generate the inputs for the equation.
# def prez_generate_input_combinations(equation):
#     base_vars = []

#     cur_var = ""
    
#     reserved_symbols = ['(', ')', '+', '*']
    
#     for i in range(len(equation)):
#         c = equation[i]
#         if (c not in reserved_symbols):
#             cur_var += c
#         elif c in reserved_symbols and len(cur_var) > 0:
#             if cur_var not in base_vars:
#                 base_vars.append(cur_var)
#             cur_var = ""
    
#     # [["a", 0], ["b", 0], ["x_1", 1]]
#     prez_display = []

#     for i in range(pow(2, len(base_vars))):
#         prez_values = [str(i)]

#         for j in range(len(base_vars) - 1, -1, -1):
#             divisor = i // pow(2, j) # TODO: Besseren Variablennamen ausdenken
#             value = divisor % 2 != 0
#             if (value): prez_values.append("1")
#             else: prez_values.append("0")
        
#         prez_display.append(prez_values)
    
#     display_base_vars = base_vars.copy()
#     display_base_vars.insert(0, "DEZ")
#     print(tabulate(prez_display, headers=display_base_vars, tablefmt='orgtbl'))

def simplify(equation):
    prez_solve(equation)
    return

def prez_solve(equation):
    showInputGeneration = os.getenv("SHOW_INPUT_GENERATION", False)
    base_vars = []

    cur_var = ""
    
    reserved_symbols = ['(', ')', '+', '*']
    
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
            values.append([base_vars[j], value])
            if (value): prez_values.append("1")
            else: prez_values.append("0")
        
        print("======")
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
    end = equation[start:len(equation)].find(')') + start + 1
    if (end == -1):
        start = 0
        end = len(equation)
    
    print("equation[" + str(start) + ":" + str(end) + "] " + equation[start:end])

    if (len(equation) == 1):
        return char_to_bool(equation[0])

    equation = equation[0:start-1] + bool_to_char(partial_compute(equation, start, end, False)) + equation[end:len(equation)]
    return compute(equation)

def partial_compute(equation, start, end, invert):
    result = None
    combinator = None
    
    for i in range(start + 1, end - 1):
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

    # result = None
    # combinator = 'i'


    # for i in range(start, len(equation)):
    #     print("i: " + str(i))
    #     if equation[i] == '0' or equation[i] == '1':
    #         result = combine(combinator, result, to_bool(equation[i]))
    #     elif equation[i] == '(':
    #         result = combine(combinator, result, compute(equation, values, i+1))
    #     elif equation[i] == ')':
    #         return result
    #     elif equation[i] == '!':
    #         # TODO: Implement Negator
    #         continue
    #     elif equation[i] == '*':
    #         combinator = '*'
    #     elif equation[i] == '+':
    #         combinator = '+'
    
    # return result

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
        print("OR")
        print(str(a or b))
        return a or b
    elif (combinator == '*'): # AND
        print("AND")
        print(str(a and b))
        return a and b
    else:
        print("CONSTANT")
        print(str(b))
        return b

def prepare_compute(equation, values):
    for pair in values:
        if (pair[1]): equation = equation.replace(pair[0], "1")
        else: equation = equation.replace(pair[0], "0")
    # print(equation)
    return equation

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
            try:
                depth[current_depth].append(i)
            except IndexError:
                print("Error: ")
                print("current_depth " + str(current_depth))
                print("depth" + str(depth))
    
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
