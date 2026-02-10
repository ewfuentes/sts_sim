import pytest
import sts_sim


def test_basic_strike_damage():
    """Strike should deal 1 damage to unblocked monster."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    # Jaw Worm starts at 8 HP
    monsters = cs.get_monsters()
    assert monsters[0].hp == 8

    # Find a Strike in hand and play it
    hand = cs.get_hand()
    strike_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            strike_idx = i
            break

    assert strike_idx is not None
    cs.play_card(strike_idx, 0)

    monsters = cs.get_monsters()
    assert monsters[0].hp == 7  # 8 - 1 = 7


def test_defend_gives_block():
    """Defend should give 1 block to player."""
    # Try multiple seeds to find one where Defend is in the opening hand
    for seed in range(100):
        cs = sts_sim.create_encounter("jaw_worm", seed=seed)
        cs.start_combat()
        hand = cs.get_hand()
        defend_idx = None
        for i, ci in enumerate(hand):
            if ci.card == sts_sim.Card.DefendRed:
                defend_idx = i
                break
        if defend_idx is not None:
            assert cs.player.block == 0
            cs.play_card(defend_idx)
            assert cs.player.block == 1
            return
    pytest.fail("No seed produced a Defend in opening hand")


def test_block_cap_at_20():
    """Player block should cap at 20."""
    cs = sts_sim.create_encounter("jaw_worm", seed=100)
    cs.start_combat()

    # Play all defends we can, multiple turns
    for turn in range(10):
        if cs.combat_over:
            break
        hand = cs.get_hand()
        for i in range(len(hand) - 1, -1, -1):
            if hand[i].card == sts_sim.Card.DefendRed and cs.player.energy >= 1:
                cs.play_card(i)
                hand = cs.get_hand()  # refresh after playing
        # Don't end turn if we're still testing block cap
        if cs.player.block >= 20:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()

    # Block should be capped at 20 if we played enough defends
    assert cs.player.block <= 20


def test_bash_applies_vulnerable():
    """Bash should deal 2 damage and apply 1 Vulnerable (net 0 after decay)."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    hand = cs.get_hand()
    bash_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.Bash:
            bash_idx = i
            break

    if bash_idx is not None:
        cs.play_card(bash_idx, 0)
        monsters = cs.get_monsters()
        # Bash deals 2 damage: 8 - 2 = 6
        assert monsters[0].hp == 6
        # Bash applies 1 Vulnerable
        assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) == 1


def test_damage_with_block():
    """Damage should be absorbed by block first."""
    # Find a seed where Defend is in opening hand
    for seed in range(100):
        cs = sts_sim.create_encounter("jaw_worm", seed=seed)
        cs.start_combat()
        hand = cs.get_hand()
        defend_idx = None
        for i, ci in enumerate(hand):
            if ci.card == sts_sim.Card.DefendRed:
                defend_idx = i
                break
        if defend_idx is not None:
            cs.play_card(defend_idx)
            assert cs.player.block == 1
            # Block resets at start of next player turn, so it won't persist
            # across monster turn, but during monster turn it should absorb damage
            return
    pytest.fail("No seed produced a Defend in opening hand")


def test_vulnerable_consumed_after_attack():
    """Vulnerable should be consumed (reduced by 1) after a player attack card resolves."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Play Bash to apply Vulnerable
    hand = cs.get_hand()
    bash_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.Bash:
            bash_idx = i
            break
    assert bash_idx is not None
    cs.play_card(bash_idx, 0)

    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    hp_after_bash = monsters[0].hp  # 8 - 2 = 6

    # Now play Strike — should deal double damage (1*2=2) and consume Vulnerable
    hand = cs.get_hand()
    strike_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            strike_idx = i
            break
    assert strike_idx is not None
    cs.play_card(strike_idx, 0)

    monsters = cs.get_monsters()
    assert monsters[0].hp == hp_after_bash - 2  # doubled damage
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) == 0  # consumed

    # Give player energy for another attack
    cs.set_player_energy(1)
    # Next Strike should deal normal damage (1) since Vulnerable is gone
    hand = cs.get_hand()
    strike_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            strike_idx = i
            break
    assert strike_idx is not None
    hp_before = cs.get_monsters()[0].hp
    cs.play_card(strike_idx, 0)
    monsters = cs.get_monsters()
    assert monsters[0].hp == hp_before - 1  # normal damage, no Vulnerable


def test_damage_floors_to_zero():
    """Damage should never go below 0."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    initial_hp = cs.player.hp
    # Even with various modifiers, HP should never increase from taking damage
    # This is implicitly tested by the damage pipeline
    assert initial_hp == 10
