# bdl/cli.py
import sys
from bdl.parser import parse
from bdl.engine import *
from bdl.formatter import print_table
from bdl.context import context
from bdl.errors import BDLException
from bdl.version import BDL_VERSION

HELP_TEXT = """
BDL — Data Language (v{version})

USAGE:
  bdl run <file.bdl>      Run a BDL script
  bdl --version | -v      Show version
  bdl --help    | -h      Show this help
  bdl help                Show this help

CORE COMMANDS:
  load "file.csv" as t
  use t
  columns
  show [n]
  filter where <condition>
  search <column> for <value>
  update <expr>
  delete where <condition>
  sort by <column> asc|desc
  select col1,col2
  group by <column> sum|avg|min|max <column>
  join <table> on <col> = <col>
  save "file.csv"

EXIT:
  exit | quit
""".format(version=BDL_VERSION)

def execute(line):
    try:
        t = parse(line)
        if not t:
            return

        cmd = t[0].lower()
        if cmd == "load":
            load_csv(t[1].strip('"'), t[3])
            print(f"Loaded {t[1]} as {t[3]}")
        elif cmd == "use":
            context.active = t[1]
        elif cmd == "columns":
            print(columns())
        elif cmd == "show":
            print_table(show(int(t[1]) if len(t)>1 else 10))
        elif cmd == "filter":
            filter_where(" ".join(t[2:]))
        elif cmd == "search":
            search(t[1], t[3])
        elif cmd == "update":
            update_expr(" ".join(t[1:]))
        elif cmd == "delete":
            delete_where(" ".join(t[2:]))
        elif cmd == "sort":
            sort_by(t[2], t[3] if len(t)>3 else 'asc')
        elif cmd == "select":
            select_cols(t[1].split(","))
        elif cmd == "group":
            group_by(t[2], t[3], t[4] if len(t)>4 else 'sum')
        elif cmd == "join":
            join_table(t[1], t[3], t[5])
        elif cmd == "save":
            save_csv(t[1].strip('"'))
            print("Saved.")
        elif cmd in ("help","?"):
            print(HELP_TEXT)
        elif cmd in ("exit","quit"):
            sys.exit(0)
        else:
            print("Unknown command. Type 'help'.")
    except BDLException as e:
        print(f"BDL Error: {e}")
    except Exception as e:
        print(f"System Error: {e}")

def repl():
    print(f"BDL v{BDL_VERSION} — Data Language")
    print("Type 'help' for commands, 'exit' to quit.\n")
    while True:
        cmd = input("bdl> ").strip()
        if cmd.lower() in ("exit","quit"):
            break
        execute(cmd)

if __name__=="__main__":
    # Version / Help flags
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"BDL version {BDL_VERSION}")
        sys.exit(0)
    if "--help" in sys.argv or "-h" in sys.argv or "help" in sys.argv:
        print(HELP_TEXT)
        sys.exit(0)

    # Script mode
    if len(sys.argv) == 3 and sys.argv[1]=="run":
        from bdl.runner import run_script
        run_script(sys.argv[2])
    # Interactive mode
    else:
        repl()
