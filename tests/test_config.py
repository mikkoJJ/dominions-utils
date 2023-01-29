import pytest

from dominions5_server.config import Game

@pytest.fixture
def default_game():
    return  Game.from_yaml_file("tests/resources/default.yaml")


def test_yaml_is_parsed(default_game):
    game = default_game

    # set values
    assert game.name == "Test_game"
    assert game.era == "MA"
    assert game.port == 9194

    # default values
    assert game.cataclysm == 75
    assert game.hof_size == 20
