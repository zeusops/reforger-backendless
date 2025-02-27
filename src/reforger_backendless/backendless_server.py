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
        dry_run: bool = False,
        host_network: bool = False,
        extra_args: str = "",
        reforger_dir: str = REFORGER_DIR,
        profile_dir: str = PROFILE_DIR,
    ):
        """Initialize the server configuration"""
        logging.basicConfig(level=logging.INFO)

        self.reforger_config = get_config(reforger_config_path)
        self.podman = podman
        self.dry_run = dry_run
        self.host_network = host_network
        self.extra_args = extra_args
        self.reforger_dir = reforger_dir
        self.profile_dir = profile_dir

        self.bind_port = self.reforger_config.bindPort

    def _start_command(self) -> list[str]:
        """Return the start command"""
        default_port = int(self.reforger_config.model_fields.get("bindPort").default)
        if self.host_network and (self.bind_port != default_port or not self.podman):
            error = (
                "Error: Must be running in Podman mode and the host network "
                f"must not be used when the bind port is not {default_port}."
            )
            logging.error(error)
            raise ValueError(error)

        if not self.podman:
            return ["./ArmaReforgerServer"]

        if self.host_network:
            network_command = ["--network=host"]
        else:
            default_a2s_port = int(
                self.reforger_config.a2s.model_fields.get("port").default
            )
            network_command = [
                "-p",
                f"{self.bind_port}:{default_port}/udp",
                "-p",
                f"{self.reforger_config.a2s.port}:{default_a2s_port}/udp",
            ]
            # Bind to the default port inside the container
            self.bind_port = default_port

            if self.reforger_config.rcon:
                default_rcon_port = int(
                    self.reforger_config.rcon.model_fields.get("port").default
                )
                network_command.extend(
                    [
                        "-p",
                        f"{self.reforger_config.rcon.port}:{default_rcon_port}/udp",
                    ]
                )

        command = [
            "podman",
            "run",
            *network_command,
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

    def _get_args(self) -> list[str]:
        """Get the command line arguments"""
        return [
            "-bindIP",
            self.reforger_config.bindAddress,
            "-bindPort",
            str(self.bind_port),
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

        logging.info("Command to execute: %s", command)

        if self.dry_run:
            logging.info("Dry run enabled, exiting without executing command")
            return

        subprocess.run(command)  # pragma: no cover
