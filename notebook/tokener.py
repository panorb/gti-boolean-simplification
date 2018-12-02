class Token:
    def __init__(self, **kwds):
        if (kwds["type"] == "AND"):
            print("It's and AND.");

def create_tokens(line):
    for c in line:
        if (c == 'a'):
            print("Its the same, like magic.");