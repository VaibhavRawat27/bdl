def print_table(data):
    if not data:
        print("No data")
        return
    headers = list(data[0].keys())
    row_format = "| " + " | ".join(["{:>15}"]*len(headers)) + " |"
    print(row_format.format(*headers))
    print("-"*len(row_format.format(*headers)))
    for row in data:
        print(row_format.format(*[str(row[h]) for h in headers]))
