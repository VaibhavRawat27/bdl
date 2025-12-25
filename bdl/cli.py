import typer
from bdl.main import run_script

app = typer.Typer(help="BDL - Business Data Language")

@app.command()
def run(file: str):
    """Run a .bdl script"""
    run_script(file)

@app.command()
def version():
    print("BDL 1.0.0 - Foundation")

if __name__ == "__main__":
    app()
