def parse(line):
    # very simple parser: splits line by spaces, first word = command
    parts = line.strip().split()
    if not parts:
        return None
    return parts
