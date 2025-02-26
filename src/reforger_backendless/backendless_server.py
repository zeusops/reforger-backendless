"""Arma Reforger server without backend"""

import logging
import subprocess

from reforger_backendless.config import get_config

REFORGER_DIR = "/opt/reforger/installation"
PROFILE_DIR = "/opt/reforger/profile"
CONTAINER_PROFILE_DIR = "/home/profile"
CONTAINER_REFORGER_DIR = "/reforger"


class BackendlessServer:
    """A server configuration for Arma Reforger without backend"""

    def __init__(
        self,
        reforger_config_path: str,
        podman: bool = False,
        extra_args: str = "",
        reforger_dir: str = REFORGER_DIR,
        profile_dir: str = PROFILE_DIR,
    ):
        """Initialize the server configuration"""
        logging.basicConfig(level=logging.INFO)

        self.reforger_config = get_config(reforger_config_path)
        self.podman = podman
        self.extra_args = extra_args
        self.reforger_dir = reforger_dir
        self.profile_dir = profile_dir

    def _start_command(self) -> list[str]:
        """Return the start command"""
        if self.podman:
            command = [
                "podman",
                "run",
                "--network=host",
                "-v",
                f"{self.reforger_dir}:{CONTAINER_REFORGER_DIR}",
                "-v",
                f"{self.profile_dir}:{CONTAINER_PROFILE_DIR}",
                "--rm",
                "--name=reforger-backendless",
                "ghcr.io/zeusops/arma-reforger:latest",
                f"{CONTAINER_REFORGER_DIR}/ArmaReforgerServer",
            ]
            self.reforger_dir = CONTAINER_REFORGER_DIR
            self.profile_dir = CONTAINER_PROFILE_DIR
            return command

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
            self.profile_dir,
            "-addons",
            ",".join([mod.modId for mod in self.reforger_config.game.mods]),
            "-addonsDir",
            f"{self.reforger_dir}/workshop/addons",
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
