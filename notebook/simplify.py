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
    base_vars = []

    cur_var = ""
    
    reserved_symbols = ['(', ')', '+', '*']
    
    for i in range(len(equation)):
        c = equation[i]
        if (c not in reserved_symbols):
            cur_var += c
        elif c in reserved_symbols and len(cur_var) > 0:
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
        
        depth = analyze_for_depth(equation)
        result = compute(equation, values, depth)
        if (result): prez_values.append("1")
        else: prez_values.append("0")

        prez_display.append(prez_values)
    
    display_base_vars = base_vars.copy()
    display_base_vars.insert(0, "DEZ")
    display_base_vars.append("RES")
    print(tabulate(prez_display, headers=display_base_vars, tablefmt='orgtbl'))

def compute(equation, values, depth):
    return False

def analyze_for_depth(equation):
    current_depth = 0
    depth = []

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
            depth[current_depth].append(i)
    
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
