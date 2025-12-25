from lark import Lark
from pathlib import Path
from lark.exceptions import UnexpectedCharacters, UnexpectedToken
from bdl.errors import BDLParseError

import os

# Use this to find the file correctly in both dev and exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

grammar_file = resource_path("bdl/parser/grammar.lark")

with open(grammar_file, "r", encoding="utf-8") as f:
    grammar = f.read()


def parse_script(script: str):
    try:
        tree = parser.parse(script)
        return tree.children
    except (UnexpectedCharacters, UnexpectedToken) as e:
        raise BDLParseError(e, script)


parser = Lark(grammar, start="start")
