def generate_input_combinations(equation):
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
    for i in range(pow(2, len(base_vars))):
        values = []

        for j in range(len(base_vars) - 1, -1, -1):
            tmp = i // pow(2, j) # TODO: Besseren Variablennamen ausdenken
            value = tmp % 2 != 0
            values.append([base_vars[j], value])

        equate(equation, values)

def equate(equation, values):
    print(values)
