import pytest
import sts_sim


@pytest.fixture
def die():
    """A deterministic die with seed 42."""
    return sts_sim.TheDie(seed=42)


@pytest.fixture
def player():
    """A fresh Ironclad player."""
    return sts_sim.Player()


@pytest.fixture
def jaw_worm_combat():
    """A combat state against Jaw Worm with seed 42."""
    return sts_sim.create_encounter("jaw_worm", seed=42)


@pytest.fixture
def cultist_combat():
    """A combat state against Cultist with seed 42."""
    return sts_sim.create_encounter("cultist", seed=42)


@pytest.fixture
def louse_combat():
    """A combat state against 2x Louse with seed 42."""
    return sts_sim.create_encounter("louse", seed=42)
