import pytest

from pydantic import ValidationError

from dominions5_server.config import Game, VictoryOptions


@pytest.fixture
def default_game() -> Game:
    return Game.from_yaml_file("tests/resources/default.yaml")


def test_yaml_is_parsed(default_game):
    game = default_game

    # set values
    assert game.name == "Test_game"
    assert game.era == "MA"
    assert game.port == 9194

    # default values
    assert game.victory.cataclysm == 75
    assert game.hof_size == 20


def test_thrones(default_game):
    assert default_game.victory.l1_thrones == 5
    assert default_game.victory.l2_thrones == 10
    assert default_game.victory.l3_thrones == 0
    assert default_game.victory.ascension_points == 8

    assert (
        default_game.victory.to_args()
        == "--thrones 5 10 0 --requiredap 8 --cataclysm 75"
    )


def test_conquer_victory():
    victory = VictoryOptions(conquer_all=True, cataclysm=3)

    assert victory.to_args() == "--conqall --cataclysm 3"


def test_both_victories_not_accepted():
    with pytest.raises(ValidationError):
        VictoryOptions(conquer_all=True, ascension_points=3, l1_thrones=3)
