import sts_sim


def test_die_rolls_in_range():
    """All die rolls should be 1-6."""
    die = sts_sim.TheDie(seed=0)
    for _ in range(100):
        roll = die.roll()
        assert 1 <= roll <= 6, f"Roll {roll} out of range"


def test_die_deterministic():
    """Same seed should produce same sequence."""
    die1 = sts_sim.TheDie(seed=123)
    die2 = sts_sim.TheDie(seed=123)
    for _ in range(20):
        assert die1.roll() == die2.roll()


def test_die_different_seeds():
    """Different seeds should (very likely) produce different sequences."""
    die1 = sts_sim.TheDie(seed=1)
    die2 = sts_sim.TheDie(seed=2)
    rolls1 = [die1.roll() for _ in range(20)]
    rolls2 = [die2.roll() for _ in range(20)]
    assert rolls1 != rolls2


def test_behavior_index_mapping():
    """Rolls 1-2 → 0, 3-4 → 1, 5-6 → 2."""
    assert sts_sim.TheDie.behavior_index(1) == 0
    assert sts_sim.TheDie.behavior_index(2) == 0
    assert sts_sim.TheDie.behavior_index(3) == 1
    assert sts_sim.TheDie.behavior_index(4) == 1
    assert sts_sim.TheDie.behavior_index(5) == 2
    assert sts_sim.TheDie.behavior_index(6) == 2
