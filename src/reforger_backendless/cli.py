"""Command line entrypoint for reforger-backendless"""

import argparse
import logging
import os
import sys

from reforger_backendless.backendless_server import (
    PROFILE_DIR,
    REFORGER_DIR,
    BackendlessServer,
)


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
        "--dry-run",
        "-n",
        help="Print the command to run without executing it",
        action="store_true",
    )
    parser.add_argument(
        "--extra-args", "-e", help="Extra arguments to pass to the server", default=""
    )
    parser.add_argument(
        "--reforger-dir",
        help="Path to the reforger installation directory",
        default=REFORGER_DIR,
    )
    parser.add_argument(
        "--profile-dir",
        help="Path to the profile directory",
        default=PROFILE_DIR,
    )
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the reforger_backendless cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    main(
        args.config,
        args.podman,
        args.dry_run,
        args.extra_args,
        args.reforger_dir,
        args.profile_dir,
    )


def main(
    config_path: str,
    podman: bool,
    dry_run: bool,
    extra_args: str,
    reforger_dir: str,
    profile_dir: str,
):
    """Run the program's main command"""
    logging.basicConfig(level=logging.INFO)

    for directory, name in [(reforger_dir, "reforger"), (profile_dir, "profile")]:
        if not os.path.exists(directory):
            logging.error(f"Error: The {name} directory '{directory}' does not exist.")
            sys.exit(1)

    server = BackendlessServer(
        config_path, podman, dry_run, extra_args, reforger_dir, profile_dir
    )
    server.start()
