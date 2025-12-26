from bdl.cli import execute

def run_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                execute(line)
