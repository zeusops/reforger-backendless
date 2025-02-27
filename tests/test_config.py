"""Test the ReforgerConfig model."""

from pathlib import Path

from reforger_backendless.config import get_config


def test_reforger_config(datadir: Path):
    """Test the ReforgerConfig model."""
    reforger_config = get_config(str(datadir / "config.json"))
    assert (
        reforger_config.game.scenarioId
        == "{BC0DB173B6FF24EA}Missions/OperationTrebuchet.conf"
    )
    assert reforger_config.game.mods[0].name == "No Backend Scenario Loader"
