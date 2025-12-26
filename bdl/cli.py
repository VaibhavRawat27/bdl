import sys
from bdl.parser import parse
from bdl.engine import *
from bdl.formatter import print_table
from bdl.context import context
from bdl.errors import BDLException
from bdl.version import BDL_VERSION

HELP_TEXT = """
BDL v1.0 — Data Language CLI
Commands:
  load "file.csv" as varname
  update field = expression
  filter where condition
  group by col agg_col [sum|avg|min|max]
  sort by column [asc|desc]
  show [n]
  save "file.csv"
  exit / quit
"""

def execute(line):
    try:
        t = parse(line)
        if not t: return

        cmd = t[0].lower()
        if cmd=="load":
            load_csv(t[1].strip('"'), t[3])
            print(f"Loaded {t[1]} as {t[3]}")
        elif cmd=="show":
            show(int(t[1]) if len(t)>1 else 10)
        elif cmd=="update":
            update_expr(" ".join(t[1:]))
        elif cmd=="filter":
            filter_where(" ".join(t[2:]))
        elif cmd=="sort":
            sort_by(t[2], t[3] if len(t)>3 else 'asc')
        elif cmd=="group":
            group_by(t[2], t[3], t[4] if len(t)>4 else 'sum')
        elif cmd=="save":
            save_csv(t[1].strip('"'))
            print("Saved.")
        elif cmd in ("exit","quit"):
            sys.exit(0)
        else:
            print("Unknown command:", cmd)

    except BDLException as e:
        print(f"BDL Error: {e}")
    except Exception as e:
        print(f"System Error: {e}")

def repl():
    print(f"BDL v{BDL_VERSION} — Interactive CLI")
    print("Type 'help' for commands, 'exit' to quit")
    while True:
        cmd = input("bdl> ").strip()
        if cmd.lower() in ("exit","quit"):
            break
        if cmd.lower() in ("help","?"):
            print(HELP_TEXT)
            continue
        execute(cmd)

def main():
    from bdl.runner import run_script
    run_script()


if __name__=="__main__":
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"BDL version {BDL_VERSION}")
        sys.exit(0)
    if len(sys.argv)==3 and sys.argv[1]=="run":
        run_script(sys.argv[2])
    else:
        repl()
