import pandas as pd
from rich.console import Console
from rich.table import Table
from bdl.runtime.context import Context

console = Console()

class Executor:
    def __init__(self):
        self.ctx = Context()

    def execute(self, commands):
        for cmd in commands:
            self._execute_command(cmd)

    def _execute_command(self, cmd):
    # unwrap statement node
        if cmd.data == "statement":
            cmd = cmd.children[0]

        if cmd.data == "load":
            self._load(cmd)
        elif cmd.data == "preview":
            self._preview(cmd)
        elif cmd.data == "show":
            self._show(cmd)


    def _load(self, cmd):
        name = cmd.children[0].value
        file_path = cmd.children[1].value.strip('"')

        df = pd.read_csv(file_path)
        self.ctx.tables[name] = df

        console.print(f"[green]Loaded {len(df)} rows into '{name}'[/green]")

    def _preview(self, cmd):
        name = cmd.children[0].value
        limit = int(cmd.children[1].value) if len(cmd.children) > 1 else 5

        df = self.ctx.tables[name].head(limit)
        self._print_table(df)

    def _show(self, cmd):
        name = cmd.children[0].value
        df = self.ctx.tables[name]
        self._print_table(df)

    def _print_table(self, df):
        table = Table(show_header=True)

        for col in df.columns:
            table.add_column(col)

        for _, row in df.iterrows():
            table.add_row(*[str(x) for x in row])

        console.print(table)
