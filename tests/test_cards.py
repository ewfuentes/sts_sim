import sts_sim


def test_strike_properties():
    """Strike should have correct properties."""
    card = sts_sim.Card.StrikeRed
    assert card.py_cost == 1
    assert card.py_base_damage == 1
    assert card.py_base_block == 0
    assert card.py_has_target is True
    assert card.py_card_type == sts_sim.CardType.Attack
    assert card.py_name == "Strike"


def test_defend_properties():
    """Defend should have correct properties."""
    card = sts_sim.Card.DefendRed
    assert card.py_cost == 1
    assert card.py_base_damage == 0
    assert card.py_base_block == 1
    assert card.py_has_target is False
    assert card.py_card_type == sts_sim.CardType.Skill
    assert card.py_name == "Defend"


def test_bash_properties():
    """Bash should have correct properties."""
    card = sts_sim.Card.Bash
    assert card.py_cost == 2
    assert card.py_base_damage == 2
    assert card.py_base_block == 0
    assert card.py_base_magic == 1
    assert card.py_has_target is True
    assert card.py_card_type == sts_sim.CardType.Attack
    assert card.py_name == "Bash"


def test_starter_deck_composition():
    """Starter deck should have 5 Strikes, 4 Defends, 1 Bash."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    deck = cs.get_deck()
    assert len(deck) == 10

    strikes = sum(1 for c in deck if c.card == sts_sim.Card.StrikeRed)
    defends = sum(1 for c in deck if c.card == sts_sim.Card.DefendRed)
    bashes = sum(1 for c in deck if c.card == sts_sim.Card.Bash)

    assert strikes == 5
    assert defends == 4
    assert bashes == 1


def test_card_play_costs_energy():
    """Playing a card should reduce energy."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    assert cs.player.energy == 3

    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break

    assert cs.player.energy == 2


def test_cannot_play_without_energy():
    """Should not be able to play card without enough energy."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Play 3 cards to exhaust energy
    played = 0
    for _ in range(3):
        hand = cs.get_hand()
        for i, ci in enumerate(hand):
            if ci.card == sts_sim.Card.StrikeRed and cs.player.energy >= 1:
                cs.play_card(i, 0)
                played += 1
                break

    assert cs.player.energy == 0

    # Try to play another card — should fail
    hand = cs.get_hand()
    if hand:
        result = cs.play_card(0, 0)
        assert result is False


def test_defend_no_target_needed():
    """Defend should be playable without a target."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.DefendRed:
            result = cs.play_card(i)
            assert result is True
            break
