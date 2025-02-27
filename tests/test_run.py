"""Test (dry) running the server."""

import logging
from pathlib import Path

import pytest

from reforger_backendless.cli import cli


def test_run(caplog, datadir: Path):
    """Test (dry) running the server."""
    caplog.set_level(logging.INFO)
    cli(
        [
            "run",
            "--config",
            str(datadir / "config.json"),
            "--dry-run",
        ]
    )
    assert "./ArmaReforgerServer" in caplog.text, "Should log podman run command"


def test_run_podman(caplog, datadir: Path):
    """Test (dry) running the server with podman."""
    caplog.set_level(logging.INFO)
    cli(
        [
            "run",
            "--config",
            str(datadir / "config.json"),
            "--podman",
            "--dry-run",
        ]
    )
    assert "'podman', 'run'" in caplog.text, "Should log podman run command"


@pytest.mark.parametrize("directory", ["reforger", "profile"])
def test_nonexistent_directory(caplog, datadir: Path, directory):
    """Test (dry) running the server with a nonexistent directory."""
    caplog.set_level(logging.INFO)
    return_value = cli(
        [
            "run",
            "--config",
            str(datadir / "config.json"),
            "--podman",
            "--dry-run",
            f"--{directory}-dir",
            "/nonexistent",
        ]
    )
    assert f"The {directory} directory" in caplog.text, "Should log error message"
    assert return_value == 1, "Should return failure exit code"


def test_host_network(caplog, datadir: Path):
    """Test (dry) running the server with the host network."""
    caplog.set_level(logging.INFO)
    with pytest.raises(ValueError) as e:
        cli(
            [
                "run",
                "--config",
                str(datadir / "config_default_port.json"),
                "--host-network",
                "--dry-run",
            ]
        )
    assert "Must be running in Podman mode" in str(
        e
    ), "Should raise a ValueError with specific message"


def test_host_network_podman(caplog, datadir: Path):
    """Test (dry) running the server with the host network."""
    caplog.set_level(logging.INFO)
    cli(
        [
            "run",
            "--config",
            str(datadir / "config_default_port.json"),
            "--host-network",
            "--podman",
            "--dry-run",
        ]
    )
    assert "host_network=True" in caplog.text, "Should log host_network=True"


def test_host_network_mismatch(datadir: Path):
    """Test (dry) running the server with a mismatch in host network settings."""
    with pytest.raises(ValueError) as e:
        cli(
            [
                "run",
                "--config",
                str(datadir / "config.json"),
                "--host-network",
                "--dry-run",
            ]
        )
    assert "Must be running in Podman mode" in str(
        e
    ), "Should raise a ValueError with specific message"


def test_run_rcon(caplog, datadir: Path):
    """Test (dry) running the server with podman with rcon configuration."""
    caplog.set_level(logging.INFO)
    cli(
        [
            "run",
            "--config",
            str(datadir / "config_rcon.json"),
            "--podman",
            "--dry-run",
        ]
    )
    assert "19998:19999/udp" in caplog.text, "Should display RCON port in log"
