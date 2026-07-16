import argparse

from .pipeline import build, compare, fetch, run_all


def main(argv=None):
    parser = argparse.ArgumentParser(description="Refresh the Legionella effector catalogue")
    parser.add_argument("command", choices=("fetch", "compare", "build", "all"))
    args = parser.parse_args(argv)
    {"fetch": fetch, "compare": compare, "build": build, "all": run_all}[args.command]()
    return 0

