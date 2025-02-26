"""Arma Reforger server configuration.

Generated using https://github.com/ikornaselur/dict-typer with manual modifications.
"""

from enum import Enum
from typing import Required

from pydantic import BaseModel
from typing_extensions import NotRequired, TypedDict

__all__ = ["ReforgerConfig"]


class A2s(TypedDict):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#a2s_2"""

    address: str
    port: NotRequired[int]


class RconPermission(Enum):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#permission"""

    admin = "admin"
    monitor = "monitor"


class Rcon(TypedDict, total=False):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#rcon_2"""

    address: Required[str]
    port: int
    password: Required[str]
    permission: Required[RconPermission]
    blacklist: list
    whitelist: list


class MissionHeader(TypedDict):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#missionHeader"""

    pass


class GameProperties(TypedDict, total=False):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#gameProperties_2"""

    serverMaxViewDistance: int
    serverMinGrassDistance: int
    networkViewDistance: int
    disableThirdPerson: bool
    fastValidation: bool
    battlEye: bool
    VONDisableUI: bool
    VONDisableDirectSpeechUI: bool
    missionHeader: MissionHeader


class Mods(TypedDict):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#mods"""

    modId: str
    name: str
    version: NotRequired[str]
    required: NotRequired[bool]


class Game(TypedDict):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#game_2"""

    name: str
    password: str
    passwordAdmin: str
    admins: list[str]
    scenarioId: str
    maxPlayers: NotRequired[int]
    visible: NotRequired[bool]
    crossPlatform: NotRequired[bool]
    supportedPlatforms: NotRequired[list[str]]
    gameProperties: GameProperties
    modsRequiredByDefault: NotRequired[bool]
    mods: list[Mods]


class JoinQueue(TypedDict):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#joinQueue"""

    maxSize: NotRequired[int]


class Operating(TypedDict, total=False):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#operating_2"""

    lobbyPlayerSynchronise: bool
    joinQueue: JoinQueue
    disableNavmeshStreaming: list[str]
    # and many more


class ReforgerConfig(BaseModel):
    """Arma Reforger server configuration root

    Ref: https://community.bistudio.com/wiki/Arma_Reforger:Server_Config
    """

    bindAddress: str = "0.0.0.0"
    bindPort: int = 2001
    publicAddress: str
    publicPort: int = 2001
    a2s: A2s
    rcon: Rcon | None = None
    game: Game
    operating: Operating = {}
