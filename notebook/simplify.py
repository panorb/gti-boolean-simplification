import os
import string
import copy
from tabulate import tabulate

reserved_symbols = ['(', ')', '+', '*', '!']

showInputGeneration = False
showInputTable = True
showDepthVisualisation = False
showMinTerms = True
showPhase1Table = True
showPhase2Table = True

def set_show(show):
    global showInputGeneration, showInputTable, showDepthVisualisation, showMinTerms, showPhase1Table, showPhase2Table
    showInputGeneration = "INPUT_GENERATION" in show
    showInputTable = "INOUT_TABLE" in show
    showDepthVisualisation = "DEPTH_VISUALISATION" in show
    showMinTerms = "MIN_TERMS" in show
    showPhase1Table = "PHASE_1" in show
    showPhase2Table = "PHASE_2" in show

def simplify(equation, show=[]):
    # set_show(show)
    var_names = isolate_var_names(equation)
    if showDepthVisualisation: output_depth(equation)

    min_terms = solve(equation, var_names)
    if showMinTerms: print("minTerms=" + str(min_terms))

    equation = find_simplest_equation(var_names, min_terms)
    solve(equation, var_names)
    return equation

def random_inputs(var_names):
    # TODO: Zufällige Inputs zuweisen
    return

def find_simplest_equation(var_names, min_terms):
    prime_implicants = phase_one(min_terms, [])
    print("Primimplikanten: " + str(prime_implicants))

    table = phase_two(min_terms, prime_implicants)
    print("Essentielle Primimplikanten: " + str(table))

    phase_three(table, [])
    # result = create_equation(var_names, table)
    # print("Ergebnis: " + result)
    return ""


def phase_one(terms, prime_implicants):
    ticked = []

    grouped_terms = group_terms(terms)
    new_terms = []
    match_count = 0

    # OOF, Setzt vorraus das Gruppen bei 0 beginnen
    for i in grouped_terms.keys():
        if i in grouped_terms and i+1 in grouped_terms:
            for term1 in grouped_terms[i]:
                for term2 in grouped_terms[i+1]:
                    match = match_pair(term1, term2)
                    if match != -1:
                        if term1 not in ticked: ticked.append(term1)
                        if term2 not in ticked:
                            ticked.append(term2)

                        new_terms.append(match)
                        match_count += 1
    
    prez_table = []
    for i in grouped_terms.keys():
        prez_table.append(["== {} ==".format(i), "="])
        for term in grouped_terms[i]:
            prez_table.append([term, "X" if term in ticked else " "])
    
    for term in terms:
        if (term not in ticked and term not in prime_implicants): prime_implicants.append(term)

    if (match_count == 0): return prime_implicants

    tabulate_table = tabulate(prez_table, tablefmt='orgtbl')
    print("")
    print("-" * tabulate_table.find("\n"))
    print(tabulate_table)
    print("-" * tabulate_table.find("\n"))
    return phase_one(new_terms, prime_implicants)

def phase_two(min_terms, prime_implicants):
    table = []

    for i in range(len(prime_implicants)):
        row = []
        for j in range(len(min_terms)):
            row.append("X" if is_matching(prime_implicants[i], min_terms[j]) else " ")
        table.append(row)

        row.insert(0, prime_implicants[i])

    header = min_terms.copy()
    header.insert(0, " ")
    table.insert(0, header)

    print(tabulate(table, headers="firstrow", tablefmt='orgtbl'))
    
    return table

def phase_three(o_table, reduced_prime_implicants):
    table = copy.deepcopy(o_table)

    for column in range(1, len(o_table[0])):
        x_count = 0
        x_pos = -1
        for row in range(1, len(o_table)):
            if (o_table[row][column] == "X"):
                x_pos = row
                x_count += 1
        
        if (x_count == 1):
            if o_table[x_pos][0] not in reduced_prime_implicants:
                reduced_prime_implicants.append(o_table[x_pos][0]) # Essential prime implicants
                for column in row_matched_columns(o_table, x_pos):
                    del_column(table, get_column_index_by_term(table, o_table[0][column]))
                del_row(table, get_row_index_by_implicant(table, o_table[x_pos][0]))
                continue

        column += 1
    
    print(tabulate(table, headers="firstrow", tablefmt='orgtbl'))
    print(reduced_prime_implicants)

def row_matched_columns(table, row):
    selected = []
    for i in range(1, len(table)):
        if table[row][i] == 'X': selected.append(i)
    return selected

def is_dominant(table, row_a, row_b):
    matched_minterms_a = row_matched_columns(table, row_a)
    matched_minterms_b = row_matched_columns(table, row_b)

    dominant = True
    for term in matched_minterms_b:
        if term not in matched_minterms_a: dominant = False

    return dominant

def get_column_index_by_term(table, term):
    for i in range(len(table[0])):
        if table[0][i] == term:
            return i
    return -1

def get_row_index_by_implicant(table, implicant):
    for i in range(len(table)):
        if table[i][0] == implicant:
            return i
    return -1

def del_column(table, column_index):
    for i in range(len(table)):
        del table[i][column_index]

def del_row(table, row_index):
    del table[row_index]

def create_equation(var_names, essential_prime_implicants):
    equation = ""
    for i in range(len(essential_prime_implicants)):
        for j in range(len(var_names)):
            if(essential_prime_implicants[i][j] == '1'):
                equation += var_names[j] + '*'
            elif(essential_prime_implicants[i][j] == '0'):
                equation += '!' + var_names[j] + '*'
        equation = equation[0:len(equation) - 1]
        equation += '+'
    equation = equation[0:len(equation) - 1]
    return equation

def matches(mask, terms):
    matches = []
    for term in terms:
        if (is_matching(mask, term)): matches.append(term)
    return matches

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
            prez_values.append(bool_to_char(value))
        
        if (showInputGeneration): print("======")
        if (showInputGeneration): print(var_names)
        if (showInputGeneration): print(values)

        prep_equ = prepare_compute(equation, var_names, values)
        result = compute(prep_equ)

        if (result):
            prez_values.append("1")
            minTerms.append(values) # Result 1 means this becomes minterm for the algorithm.
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
    print("combine() reached end, combinaor has no known value.")
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