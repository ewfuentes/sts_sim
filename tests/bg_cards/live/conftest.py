"""Re-export fixtures from tests/live/conftest for bg_cards live tests."""
import pytest
from tests.live.conftest import client, in_combat, game, end_turn_both, _swap_encounter  # noqa: F401


@pytest.fixture(scope="class")
def single_monster_fight(client, in_combat):
    """Swap to a single-monster encounter once per test class."""
    _swap_encounter(client, "BoardGame:Jaw Worm (Easy)")


@pytest.fixture(scope="class")
def two_monster_fight(client, in_combat):
    """Swap to a two-monster encounter once per test class."""
    _swap_encounter(client, "BoardGame:2 Louse")


@pytest.fixture(scope="function")
def fresh_combat(client, in_combat):
    """Swap to Gremlin Nob for each multi-turn test."""
    _swap_encounter(client, "BoardGame:Gremlin Nob")
