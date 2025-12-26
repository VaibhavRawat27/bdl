# bdl/parser.py
def parse(line):
    # naive parser: split by spaces
    tokens = line.strip().split()
    return tokens if tokens else None
