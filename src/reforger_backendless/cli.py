"""Command line entrypoint for reforger-backendless"""

import argparse
import sys


def parse_arguments(args: list[str]) -> argparse.Namespace:
    """Parse generic arguments, given as parameters

    This function can be used programatically to emulate CLI calls, either
    during tests or via other interfaces like API calls.


    Arguments:
      args: The arguments to parse, usually from `sys.argv` array.

    """
    parser = argparse.ArgumentParser(
        "reforger-backendless",
        description=(
            "A set of helper scripts to run an Arma Reforger server "
            "without the BI backend"
        ),
    )
    parser.add_argument("foo", help="Some parameter")
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the reforger_backendless cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    main(args.foo)


def main(foo):
    """Run the program's main command"""
    print(f"Foo is: {foo}")
