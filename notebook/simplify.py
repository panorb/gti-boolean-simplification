import os
import string
from tabulate import tabulate
from IPython.core.display import display, HTML

reserved_symbols = ['(', ')', '+', '*', '!']

showInputGeneration = os.getenv("SHOW_INPUT_GENERATION", "False") == "True"
showInputTable = os.getenv("SHOW_INPUT_TABLE", "False") == "True"
showDepthVisualisation = os.getenv("SHOW_DEPTH_VISUALISATION", "False") == "True"
showMinTerms = os.getenv("SHOW_MIN_TERMS", "False") == "True"
showPhase1Table = os.getenv("SHOW_PHASE_1_TABLE", "False") == "True"
showPhase2Table = os.getenv("SHOW_PHASE_2_TABLE", "False") == "True"

def simplify(equation):
    var_names = isolate_var_names(equation)
    if showDepthVisualisation: output_depth(equation)

    min_terms = solve(equation, var_names)
    if showMinTerms: print("minTerms=" + str(min_terms))
    
    prime_implicants = phase_one(min_terms, [])
    print("Primimplikanten: " + str(prime_implicants))

    essential_prime_implicants = phase_two(min_terms, prime_implicants)
    print("Essentielle Primimplikanten: " + str(essential_prime_implicants))

    result = create_equation(var_names, essential_prime_implicants)
    print("Ergebnis: " + result)
    return result

def phase_one(terms, prime_implicants):
    ticked = []

    grouped_terms = group_terms(terms)
    print("grouped_terms: " + str(grouped_terms))
    new_terms = []
    match_count = 0

    for i in range(len(grouped_terms)):
        if i in grouped_terms and i+1 in grouped_terms:
            for term1 in grouped_terms[i]:
                for term2 in grouped_terms[i+1]:
                    match = match_pair(term1, term2)
                    if match != -1:
                        if term1 not in ticked: ticked.append(term1)
                        if term2 not in ticked:
                            ticked.append(term2)
                            print("ticked[] <- " + term2)

                        new_terms.append(match)
                        match_count += 1
    
    for term in terms:
        if (term not in ticked and term not in prime_implicants): prime_implicants.append(term)

    if (match_count == 0): return prime_implicants

    return phase_one(new_terms, prime_implicants)

def phase_two(min_terms, prime_implicants):
    table = []
    prez_table = []

    for i in range(len(prime_implicants)):
        row = []
        for j in range(len(min_terms)):
            row.append("X" if is_matching(prime_implicants[i], min_terms[j]) else " ")
        table.append(row)

        prez_row = row.copy()
        prez_row.insert(0, prime_implicants[i])
        prez_table.append(prez_row)

    prez_headers = min_terms.copy()
    prez_headers.insert(0, " ")
    print(tabulate(prez_table, headers=prez_headers, tablefmt='orgtbl'))

    essential_prime_implicants = []
    for i in range(len(min_terms)):
        x_count = 0
        x_pos = -1
        for j in range(len(prime_implicants)):
            if (table[j][i] == "X"):
                x_pos = j
                x_count += 1
        
        if (x_count == 1 and prime_implicants[x_pos] not in essential_prime_implicants):
            essential_prime_implicants.append(prime_implicants[x_pos])
    
    essential_prime_implicants.sort()
    return essential_prime_implicants

def create_equation(var_names, essential_prime_implicants):
    equation = ""
    for i in range(len(essential_prime_implicants)):
        equation += '('
        for j in range(len(var_names)):
            if(essential_prime_implicants[i][j] == '1'):
                equation += var_names[j] + '*'
            elif(essential_prime_implicants[i][j] == '0'):
                equation += '!' + var_names[j] + '*'
        equation = equation[0:len(equation) - 1]
        equation += ')+'
    equation = equation[0:len(equation) - 1]
    return equation

def is_matching(mask, term):
    for i in range(len(mask)):
        if (mask[i] == '_'): continue
        elif (mask[i] == term[i]): continue
        return False
    return True

def group_terms(minTerms):
    grouped = {}

    for i in range(len(minTerms)):
        term = minTerms[i]
        one_count = 0

        for j in range(len(minTerms[0])):
            if (minTerms[i][j] == "1"): one_count += 1
        
        if one_count in grouped:
            grouped[one_count].append(term)
        else:
            grouped[one_count] = [term]
    
    return grouped

def match_pair(term1, term2):
    changes = 0
    compared = ""

    for i in range(len(term1)):
        if (term1[i] == term2[i]):
            compared += term1[i]
        else:
            changes += 1
            compared += "_"
    
    if (changes == 1): return compared
    return -1

def isolate_var_names(equation):
    var_names = []

    cur_var = ""

    for i in range(len(equation)):
        c = equation[i]
        if (c not in reserved_symbols):
            cur_var += c
        if (c in reserved_symbols or i == len(equation) - 1) and len(cur_var) > 0:
            if cur_var not in var_names:
                var_names.append(cur_var)
            cur_var = ""

    var_names.sort()
    return var_names

def solve(equation, var_names):
    # [["a", 0], ["b", 0], ["x_1", 1]]
    prez_display = []
    minTerms = []

    for i in range(pow(2, len(var_names))):
        prez_values = [str(i)]
        values = ""

        for j in range(len(var_names) - 1, -1, -1):
            divisor = i // pow(2, j) # TODO: Besseren Variablennamen ausdenken
            value = divisor % 2 != 0
            values += bool_to_char(value)
            if (value): prez_values.append("1")
            else: prez_values.append("0")
        
        if (showInputGeneration): print("======")
        if (showInputGeneration): print(var_names)
        if (showInputGeneration): print(values)

        prep_equ = prepare_compute(equation, var_names, values)
        #depth = analyze_for_depth(equation)
        result = compute(prep_equ)

        if (result):
            prez_values.append("1")
            minTerms.append(values)
        else:
            prez_values.append("0")

        prez_display.append(prez_values)
    
    display_base_vars = var_names.copy()
    display_base_vars.insert(0, "DEZ")
    display_base_vars.append("RES")
    if (showInputTable): print(tabulate(prez_display, headers=display_base_vars, tablefmt='orgtbl'))
    return minTerms

def compute(equation):
    if (showInputGeneration): print("eq " + equation)
    depth = analyze_for_depth(equation)
    if (showInputGeneration): 
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

    computed = partial_compute(equation, start, end, False)
    if (start - 1 >= 0 and equation[start - 1] == '!'):
        computed = not computed
    
    equation = equation[0:start] + bool_to_char(computed) + equation[end+1:len(equation)]
    return compute(equation)

def partial_compute(equation, start, end, invert):
    result = None
    combinator = 'c'
    
    for i in range(start + 1, end):
        if equation[i] == '0' or equation[i] == '1':
            result = combine(combinator, result, char_to_bool(equation[i]))
        elif equation[i] == '*':
            combinator = '*'
        elif equation[i] == '+':
            combinator = '+'
    
    return result

def char_to_bool(char):
    if (char == '1'):
        return True
    return False

def bool_to_char(bol):
    if (bol):
        return '1'
    return '0'

def combine(combinator, a, b):
    if (combinator == '+'): # OR
        if (showInputGeneration): 
            print("... OR ...")
            print("." + bool_to_char(a) + ". OR ." + bool_to_char(b) + ". = " + bool_to_char(a or b))
        return a or b
    elif (combinator == '*'): # AND
        if (showInputGeneration): 
            print("... AND ...")
            print("." + bool_to_char(a) + ". AND ." + bool_to_char(b) + ". = " + bool_to_char(a and b))
        return a and b
    elif (combinator =='c'):
        if (showInputGeneration): 
            print("CONSTANT ...")
            print("CONSTANT ." + bool_to_char(b) + ".")
        return b
    print("Combine reached end, combinaor has no known value.")
    raise ValueError()

def prepare_compute(equation, var_names, values):
    for i in range(len(var_names)):
        equation = equation.replace("!" + var_names[i], bool_to_char(not char_to_bool(values[i])))
        equation = equation.replace(var_names[i], values[i])
    
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

def output_depth(equation):
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
