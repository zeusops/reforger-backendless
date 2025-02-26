"""Test the ReforgerConfig model."""

import json
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from reforger_backendless.config import ReforgerConfig


def test_reforger_config(datadir: Path):
    """Test the ReforgerConfig model."""
    config = json.load(open(datadir / "config.json"))
    reforger_config = ReforgerConfig(**config)
    assert (
        reforger_config.game["scenarioId"]
        == "{BC0DB173B6FF24EA}Missions/OperationTrebuchet.conf"
    )
    assert reforger_config.game["mods"][0]["name"] == "No Backend Scenario Loader"

    ta = TypeAdapter(ReforgerConfig)
    try:
        ta.validate_python(config)
    except ValidationError as e:
        assert False, e

    with open(datadir / "config.json", "r") as f:
        data = f.read()
    obj = ta.validate_json(data)
    print(type(obj))
    assert (
        obj.game["scenarioId"] == "{BC0DB173B6FF24EA}Missions/OperationTrebuchet.conf"
    )
    assert obj.game["mods"][0]["name"] == "No Backend Scenario Loader"
