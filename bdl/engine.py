import sys
from bdl.parser import parse
from bdl.engine import *
from bdl.formatter import print_table
from bdl.context import context
from bdl.errors import BDLException
from bdl.version import BDL_VERSION




# =========================
# HELP TEXT
# =========================
HELP_TEXT = """
BDL — Data Language (v{version})

USAGE:
  bdl                     Start interactive shell
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


# =========================
# EXECUTOR
# =========================
def execute(line):
    try:
        t = parse(line)
        if not t:
            return

        if t[0] == "load":
            load_csv(t[1], t[3])
            print(f"Loaded {t[1]} as {t[3]}")

        elif t[0] == "use":
            context.active = t[1]

        elif t[0] == "columns":
            print(columns())

        elif t[0] == "show":
            print_table(show(int(t[1]) if len(t) > 1 else 10))

        elif t[0] == "filter":
            filter_where(" ".join(t[2:]))

        elif t[0] == "search":
            search(t[1], t[3])

        elif t[0] == "update":
            update_expr(" ".join(t[1:]))

        elif t[0] == "delete":
            delete_where(" ".join(t[2:]))

        elif t[0] == "sort":
            sort_by(t[2], t[3])

        elif t[0] == "select":
            select_cols(t[1].split(","))

        elif t[0] == "group":
            group_by(t[2], t[3], t[4])

        elif t[0] == "join":
            join_table(t[1], t[3], t[5])

        elif t[0] == "save":
            save_csv(t[1])
            print("Saved.")

        elif t[0] == "help":
            print(HELP_TEXT)

        else:
            print("Unknown command. Type 'help'.")

    except BDLException as e:
        print(f"BDL Error: {e}")
    except Exception as e:
        print(f"System Error: {e}")


# =========================
# REPL
# =========================
def repl():
    print(f"BDL v{BDL_VERSION} — Data Language")
    print("Type 'help' for commands, 'exit' to quit.\n")

    while True:
        cmd = input("bdl> ").strip()

        if cmd in ("exit", "quit"):
            break

        execute(cmd)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":

    # ---- VERSION FLAG ----
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"BDL version {BDL_VERSION}")
        sys.exit(0)

    # ---- HELP FLAG ----
    if "--help" in sys.argv or "-h" in sys.argv or "help" in sys.argv:
        print(HELP_TEXT)
        sys.exit(0)

    # ---- SCRIPT MODE ----
    if len(sys.argv) == 3 and sys.argv[1] == "run":
        from runner import run_script
        run_script(sys.argv[2])

    # ---- INTERACTIVE MODE ----
    else:
        repl()
