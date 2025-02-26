"""Command line entrypoint for reforger-backendless"""

import argparse
import sys

from reforger_backendless.backendless_server import BackendlessServer


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
    parser.add_argument(
        "--config",
        "-c",
        help="Path to the configuration file",
        default="config.json",
    )
    parser.add_argument(
        "--podman",
        "-p",
        help="Use podman to run the server",
        action="store_true",
    )
    parser.add_argument(
        "--extra-args", "-e", help="Extra arguments to pass to the server", default=""
    )
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the reforger_backendless cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    main(args.config, args.podman, args.extra_args)


def main(config_path: str, podman: bool, extra_args: str):
    """Run the program's main command"""
    server = BackendlessServer(config_path, podman, extra_args)
    server.start()
