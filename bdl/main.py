from bdl.parser.parser import parse_script
from bdl.runtime.executor import Executor

def run_script(file_path: str):
    print(f"Running BDL script: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        script = f.read()

    commands = parse_script(script)

    print(f"Parsed {len(commands)} commands")

    executor = Executor()
    executor.execute(commands)
