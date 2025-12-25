import pandas as pd
from rich.console import Console
from rich.table import Table
from bdl.runtime.context import Context

console = Console()

class Executor:
    def __init__(self):
        self.ctx = Context()
        self.grouped = None
        self.last_table = None   # 🔥 IMPORTANT

    def execute(self, commands):
        for cmd in commands:
            if cmd.data == "statement":
                cmd = cmd.children[0]
            self._execute(cmd)

    def _execute(self, cmd):
        name = cmd.data if isinstance(cmd.data, str) else cmd.data.value

        if name == "load":
            self.load(cmd)
        elif name == "preview":
            self.preview(cmd)
        elif name == "show":
            self.show(cmd)
        elif name == "filter":
            self.filter(cmd)
        elif name == "search":
            self.search(cmd)
        elif name == "add_column":
            self.add_column(cmd)
        elif name == "sort":
            self.sort(cmd)
        elif name == "group":
            self.group(cmd)
        elif name == "summarize":
            self.summarize(cmd)

    # -------- COMMANDS -------- #

    def load(self, cmd):
        table = cmd.children[0].value
        path = cmd.children[1].value.strip('"')
        df = pd.read_csv(path)
        self.ctx.tables[table] = df
        self.last_table = table
        console.print(f"[green]Loaded {len(df)} rows into {table}[/green]")

    def preview(self, cmd):
        table = cmd.children[0].value
        self.last_table = table
        limit = int(cmd.children[1].value) if len(cmd.children) > 1 else 5
        self.print_df(self.ctx.tables[table].head(limit))

    def show(self, cmd):
        table = cmd.children[0].value
        self.last_table = table
        self.print_df(self.ctx.tables[table])

    def filter(self, cmd):
        table = cmd.children[0].value
        condition = cmd.children[1]

        col, op, val_node = condition.children
        token = val_node.children[0]

        value = token.value.strip('"') if token.type == "STRING" else int(token.value)

        # 🔥 OPERATOR TRANSLATION (IMPORTANT)
        pandas_op = "==" if op.value == "=" else op.value

        df = self.ctx.tables[table]
        query = f"`{col.value}` {pandas_op} @value"
        self.ctx.tables[table] = df.query(query)

        self.last_table = table


    def search(self, cmd):
        table = cmd.children[0].value
        text = cmd.children[1].value.strip('"')

        df = self.ctx.tables[table]
        mask = df.apply(
            lambda r: r.astype(str).str.contains(text, case=False).any(),
            axis=1
        )

        self.ctx.tables[table] = df[mask]
        self.last_table = table

    def add_column(self, cmd):
        if not self.last_table:
            raise RuntimeError("No table available for add column")

        new_col = cmd.children[0].value
        left, op, right = cmd.children[1].children
        df = self.ctx.tables[self.last_table]

        if op.value == "+":
            df[new_col] = df[left.value] + df[right.value]
        elif op.value == "-":
            df[new_col] = df[left.value] - df[right.value]
        elif op.value == "*":
            df[new_col] = df[left.value] * df[right.value]
        elif op.value == "/":
            df[new_col] = df[left.value] / df[right.value]

    def sort(self, cmd):
        table, col, order = cmd.children
        df = self.ctx.tables[table.value]
        self.ctx.tables[table.value] = df.sort_values(
            col.value, ascending=(order.value == "asc")
        )
        self.last_table = table.value

    def group(self, cmd):
        table, col = cmd.children
        self.grouped = self.ctx.tables[table.value].groupby(col.value)
        self.last_table = table.value

    def summarize(self, cmd):
        _, agg, col = cmd.children

        if agg.value == "total":
            result = self.grouped[col.value].sum()
        elif agg.value == "average":
            result = self.grouped[col.value].mean()
        elif agg.value == "min":
            result = self.grouped[col.value].min()
        elif agg.value == "max":
            result = self.grouped[col.value].max()
        elif agg.value == "count":
            result = self.grouped[col.value].count()

        console.print(result.reset_index())

    # -------- OUTPUT -------- #

    def print_df(self, df):
        table = Table(show_header=True)
        for c in df.columns:
            table.add_column(str(c))
        for _, r in df.iterrows():
            table.add_row(*[str(x) for x in r])
        console.print(table)
