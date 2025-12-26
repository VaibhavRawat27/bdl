# bdl/runner.py
def run_script(filename):
    from bdl.cli import execute  # import inside function to avoid circular import
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                execute(line)
