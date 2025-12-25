from lark import Lark

with open("bdl/parser/grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

def parse_script(script: str):
    tree = parser.parse(script)
    return tree.children
