"""Arma Reforger server configuration.

Generated using https://github.com/ikornaselur/dict-typer with manual modifications.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict

__all__ = ["ReforgerConfig"]


class A2s(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#a2s_2"""

    model_config = ConfigDict(extra="forbid")

    address: str
    port: int = 17777


class RconPermission(Enum):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#permission"""

    admin = "admin"
    monitor = "monitor"


class Rcon(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#rcon_2"""

    model_config = ConfigDict(extra="forbid")

    address: str
    port: int = 19999
    password: str
    permission: RconPermission
    blacklist: list = []
    whitelist: list = []


class MissionHeader(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#missionHeader"""

    model_config = ConfigDict(extra="allow")


class GameProperties(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#gameProperties_2"""

    model_config = ConfigDict(extra="forbid")

    serverMaxViewDistance: int = 1600
    serverMinGrassDistance: int = 0
    fastValidation: bool = True
    networkViewDistance: int = 1500
    battlEye: bool = True
    disableThirdPerson: bool = False
    VONDisableUI: bool = False
    VONDisableDirectSpeechUI: bool = False
    VONCanTransmitCrossFaction: bool = False
    missionHeader: MissionHeader


class Mods(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#mods"""

    model_config = ConfigDict(extra="forbid")

    modId: str
    name: str
    version: str = ""
    required: bool = True


class Game(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#game_2"""

    model_config = ConfigDict(extra="forbid")

    name: str
    password: str
    passwordAdmin: str
    admins: list[str]
    scenarioId: str
    maxPlayers: int = 64
    visible: bool = True
    crossPlatform: bool = False
    supportedPlatforms: list[str] = ["PLATFORM_PC"]
    gameProperties: GameProperties
    modsRequiredByDefault: bool = True
    mods: list[Mods] = []


class JoinQueue(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#joinQueue"""

    model_config = ConfigDict(extra="forbid")

    maxSize: int = 0


class Operating(BaseModel):
    """https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#operating_2"""

    model_config = ConfigDict(extra="allow")

    lobbyPlayerSynchronise: bool = True
    joinQueue: JoinQueue | None = None
    disableNavmeshStreaming: list[str] | bool = False
    # and many more


class ReforgerConfig(BaseModel):
    """Arma Reforger server configuration root

    Ref: https://community.bistudio.com/wiki/Arma_Reforger:Server_Config
    """

    model_config = ConfigDict(extra="forbid")

    bindAddress: str = "0.0.0.0"
    bindPort: int = 2001
    publicAddress: str
    publicPort: int = 2001
    a2s: A2s
    rcon: Rcon | None = None
    game: Game
    operating: Operating | None = None
