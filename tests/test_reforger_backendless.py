"""Basic tests of reforger_backendless CLI"""

import pytest

from reforger_backendless.cli import cli

API_AUTH_TOK = "not-a-real-pass123deadb0b"


@pytest.mark.parametrize("args", [[], None])
def test_cli_shows_usage(capsys, args):
    """Checks we can invoke the CLI entrypoint (no shelling out) via --help"""
    try:
        cli(args)
    except SystemExit:  # Args parsing failure throws SystemExit
        pass  # Ignore it to run tests properly
    _out, err = capsys.readouterr()
    assert "usage" in err, "Missing required args should show usage in stderr"
