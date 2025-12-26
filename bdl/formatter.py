def print_table(data):
    if not data:
        print("[Empty table]")
        return

    headers = list(data[0].keys())
    col_widths = {h: max(len(str(h)), *(len(str(row[h])) for row in data)) for h in headers}

    header_line = " | ".join(f"{h:{col_widths[h]}}" for h in headers)
    separator_line = "-+-".join("-" * col_widths[h] for h in headers)
    print(header_line)
    print(separator_line)
    for row in data:
        row_line = " | ".join(f"{str(row[h]):{col_widths[h]}}" for h in headers)
        print(row_line)
