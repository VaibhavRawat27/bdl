from lark import Lark
from pathlib import Path

GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"

with open(GRAMMAR_PATH, encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(grammar, start="start")

def parse_script(script: str):
    tree = parser.parse(script)
    return tree.children
