"""Arma Reforger server without backend"""

import logging
import subprocess

from reforger_backendless.config import get_config

PROFILE_DIR = "/home/profile"
REFORGER_DIR = "/reforger"


class BackendlessServer:
    """A server configuration for Arma Reforger without backend"""

    def __init__(
        self, reforger_config_path: str, podman: bool = False, extra_args: str = ""
    ):
        """Initialize the server configuration"""
        logging.basicConfig(level=logging.INFO)

        self.reforger_config = get_config(reforger_config_path)
        self.podman = podman
        self.extra_args = extra_args

    def _start_command(self) -> list[str]:
        """Return the start command"""
        if self.podman:
            return [
                "podman",
                "run",
                "--network=host",
                "-v",
                "/opt/reforger/installation:/reforger",
                "-v",
                "/opt/reforger/profile:/home/profile",
                "--rm",
                "--name=reforger-backendless",
                "ghcr.io/zeusops/arma-reforger:latest",
                "/reforger/ArmaReforgerServer",
            ]

        return ["./ArmaReforgerServer"]

    def _get_args(self) -> list[str]:
        """Get the command line arguments"""
        return [
            "-bindIP",
            self.reforger_config.bindAddress,
            "-bindPort",
            str(self.reforger_config.bindPort),
            "-noSound",
            "-maxFPS",
            "60",
            "-logLevel",
            "normal",
            "-logStats",
            "60000",
            "-adminPassword",
            self.reforger_config.game.passwordAdmin,
            "-profile",
            PROFILE_DIR,
            "-addons",
            ",".join([mod.modId for mod in self.reforger_config.game.mods]),
            "-addonsDir",
            f"{REFORGER_DIR}/workshop/addons",
            "-server",
            "worlds/NoBackendScenarioLoader.ent",
            "-scenarioId",
            self.reforger_config.game.scenarioId,
        ]

    def start(self):
        """Start the server"""
        logging.info(
            "Starting server on %s:%s",
            self.reforger_config.bindAddress,
            self.reforger_config.bindPort,
        )
        command = self._start_command()
        command.extend(self._get_args())
        command.extend(self.extra_args.split())

        logging.info("Executing command: %s", command)

        subprocess.run(command)
