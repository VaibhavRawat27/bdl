# bdl/engine.py
from bdl.context import context
from bdl.formatter import print_table
import csv

# Load CSV file
def load_csv(file_path, varname):
    print(f"[load_csv] Loading '{file_path}' as '{varname}'")
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            context.tables[varname] = [row for row in reader]
        context.active = varname
        print_table(context.tables[varname])
    except FileNotFoundError:
        print(f"[Error] File '{file_path}' not found.")
        context.tables[varname] = []

# Update expression (basic: profit = price - cost)
def update_expr(expr):
    print(f"[update_expr] {expr}")
    table = context.tables.get(context.active, [])
    if not table:
        return

    # Only supports 'profit = price - cost' format for now
    parts = expr.replace(" ", "").split("=")
    if len(parts) == 2:
        col, operation = parts
        if operation == "price-cost":
            for row in table:
                try:
                    row[col] = float(row.get("price",0)) - float(row.get("cost",0))
                except ValueError:
                    row[col] = 0
    print_table(table)

# Filter rows (basic equality only)
def filter_where(condition):
    print(f"[filter_where] {condition}")
    table = context.tables.get(context.active, [])
    if not table:
        return

    # Only supports 'col == "value"'
    if "==" in condition:
        col, val = condition.split("==")
        col = col.strip()
        val = val.strip().strip('"')
        table = [r for r in table if r.get(col) == val]
        context.tables[context.active] = table
    print_table(table)

# Group by (sum aggregation)
def group_by(col, agg_col, agg_func='sum'):
    print(f"[group_by] {col}, {agg_col}, {agg_func}")
    table = context.tables.get(context.active, [])
    grouped = {}
    for r in table:
        key = r[col]
        grouped.setdefault(key, []).append(r)

    new_table = []
    for k, rows in grouped.items():
        val = 0
        if agg_func == 'sum':
            for row in rows:
                try:
                    val += float(row.get(agg_col,0))
                except ValueError:
                    val += 0
        new_table.append({col: k, agg_col: val})
    context.tables[context.active] = new_table
    print_table(new_table)

# Sort by column
def sort_by(col, order='asc'):
    print(f"[sort_by] {col} {order}")
    table = context.tables.get(context.active, [])
    reverse = order.lower() == "desc"
    try:
        table.sort(key=lambda x: float(x.get(col,0)), reverse=reverse)
    except ValueError:
        table.sort(key=lambda x: x.get(col,''), reverse=reverse)
    print_table(table)

# Show first n rows
def show(n=10):
    table = context.tables.get(context.active, [])
    print_table(table[:n])
    return table[:n]

# Save CSV
def save_csv(file_path):
    print(f"[save_csv] Saving CSV to {file_path}")
    table = context.tables.get(context.active, [])
    if not table:
        print("[Empty table]")
        return
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        writer.writeheader()
        writer.writerows(table)
    print_table(table)

# Columns
def columns():
    table = context.tables.get(context.active, [])
    return list(table[0].keys()) if table else []
