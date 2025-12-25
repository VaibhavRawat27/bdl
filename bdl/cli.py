import os
import typer
from lark.exceptions import UnexpectedCharacters, UnexpectedToken
from bdl.main import run_script
from bdl.errors import BDLParseError

os.environ["RICH_DISABLE"] = "1"

app = typer.Typer(
    help="BDL - Business Data Language",
    add_completion=False
)


def print_unexpected_char(e: UnexpectedCharacters, source: str):
    print(
        f"UnexpectedCharacters: No terminal matches '{e.char}' "
        f"in the current parser context"
    )
    print(f"at line {e.line}, column {e.column}\n")
    print(e.get_context(source))
    print("\nExpected one of:")
    for t in sorted(e.allowed):
        print(f"  {t}")


def print_unexpected_token(e: UnexpectedToken, source: str):
    print("UnexpectedToken")
    print(f"at line {e.line}, column {e.column}\n")
    print(e.get_context(source))
    print("\nExpected one of:")
    for t in sorted(e.expected):
        print(f"  {t}")


@app.command()
def run(file: str):
    try:
        run_script(file)
    except BDLParseError as e:
        if isinstance(e.error, UnexpectedCharacters):
            print_unexpected_char(e.error, e.source)
        elif isinstance(e.error, UnexpectedToken):
            print_unexpected_token(e.error, e.source)
        raise typer.Exit(code=1)


@app.command()
def version():
    print("BDL 1.0.0 - Foundation")


if __name__ == "__main__":
    app()
