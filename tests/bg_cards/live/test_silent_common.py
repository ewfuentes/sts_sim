"""Live tests for Silent Common cards."""
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ---------------------------------------------------------------------------
# Poisoned Stab
# ---------------------------------------------------------------------------

def test_poisoned_stab_base(game):
    """Poisoned Stab deals 1 damage, applies 1 Poison, and exhausts."""
    hand = [sts_sim.Card.PoisonedStab]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_poisoned_stab_upgraded(game):
    """Upgraded Poisoned Stab applies 2 Poison."""
    hand = [(sts_sim.Card.PoisonedStab, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


def test_poisoned_stab_with_strength(game):
    """Poisoned Stab with 2 STR adds damage per HIT."""
    hand = [sts_sim.Card.PoisonedStab]
    powers = {"Strength": 2}
    set_scenario(game, hand=hand, energy=3, monster_hp=10, player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=10, player_powers=powers)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


# ---------------------------------------------------------------------------
# Dagger Throw
# ---------------------------------------------------------------------------

def test_dagger_throw_base(game):
    """Dagger Throw deals 2 HIT, draws 1, discards 1."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        sts_sim.Card.DaggerThrow, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, monster_hp=10)
    # Play Dagger Throw targeting enemy, choose card 0 to discard
    state = play_card_both(game, sim, hand_index=0, target_index=0, choices=[0])
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_dagger_throw_upgraded(game):
    """Upgraded Dagger Throw deals 3 HIT."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [(sts_sim.Card.DaggerThrow, True)]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0, choices=[0])
    assert_monsters_match(state, sim)


# ---------------------------------------------------------------------------
# Dagger Spray
# ---------------------------------------------------------------------------

def test_dagger_spray_base(game):
    """Dagger Spray hits all enemies twice."""
    hand = [sts_sim.Card.DaggerSpray]
    monsters = [{"hp": 10}, {"hp": 8}]
    set_scenario(game, hand=hand, energy=3, monsters=monsters)
    sim = make_sim(hand=hand, energy=3, monsters=monsters)
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_dagger_spray_upgraded(game):
    """Upgraded Dagger Spray hits all enemies three times."""
    hand = [(sts_sim.Card.DaggerSpray, True)]
    monsters = [{"hp": 10}, {"hp": 8}]
    set_scenario(game, hand=hand, energy=3, monsters=monsters)
    sim = make_sim(hand=hand, energy=3, monsters=monsters)
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)


def test_dagger_spray_with_strength(game):
    """Dagger Spray with 1 STR adds to each HIT on each enemy."""
    hand = [sts_sim.Card.DaggerSpray]
    powers = {"Strength": 1}
    monsters = [{"hp": 10}, {"hp": 10}]
    set_scenario(game, hand=hand, energy=3, monsters=monsters, player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monsters=monsters, player_powers=powers)
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)


# ---------------------------------------------------------------------------
# Sneaky Strike
# ---------------------------------------------------------------------------

def test_sneaky_strike_no_discard(game):
    """Sneaky Strike deals 3 damage without discard, no energy refund."""
    hand = [sts_sim.Card.SneakyStrike]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sneaky_strike_upgraded(game):
    """Upgraded Sneaky Strike deals 4 HIT."""
    hand = [(sts_sim.Card.SneakyStrike, True)]
    powers = {"Strength": 1}
    set_scenario(game, hand=hand, energy=3, monster_hp=20, player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=20, player_powers=powers)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Slice
# ---------------------------------------------------------------------------

def test_slice_base_no_shiv(game):
    """Slice deals 1 damage at zero cost without SHIV."""
    hand = [sts_sim.Card.Slice]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Backflip
# ---------------------------------------------------------------------------

def test_backflip_base(game):
    """Backflip grants 1 block and draws 2 cards."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        sts_sim.Card.Backflip, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3, player_block=0)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, player_block=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_backflip_upgraded(game):
    """Upgraded Backflip grants 2 block and draws 2 cards."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [(sts_sim.Card.Backflip, True)]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3, player_block=0)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, player_block=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Dodge and Roll
# ---------------------------------------------------------------------------

def test_dodge_and_roll_self(game):
    """Dodge and Roll assigns 2 BLK to self."""
    hand = [sts_sim.Card.DodgeAndRoll]
    set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)
    # Choice 0 = assign to self for each BLK
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Deflect
# ---------------------------------------------------------------------------

def test_deflect_base_no_shiv(game):
    """Deflect grants 1 block at zero cost without SHIV."""
    hand = [sts_sim.Card.Deflect]
    set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Cloak and Dagger
# ---------------------------------------------------------------------------

def test_cloak_and_dagger_base(game):
    """Cloak and Dagger gives 1 SHIV and 1 block."""
    hand = [sts_sim.Card.CloakAndDagger]
    set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_cloak_and_dagger_upgraded(game):
    """Upgraded Cloak and Dagger gives 2 SHIV and 1 block."""
    hand = [(sts_sim.Card.CloakAndDagger, True)]
    set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Blade Dance
# ---------------------------------------------------------------------------

def test_blade_dance_base(game):
    """Blade Dance gives 2 SHIV tokens."""
    hand = [sts_sim.Card.BladeDance]
    set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_blade_dance_upgraded(game):
    """Upgraded Blade Dance gives 3 SHIV tokens."""
    hand = [(sts_sim.Card.BladeDance, True)]
    set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_blade_dance_stacks(game):
    """Blade Dance SHIV stacks with existing SHIV."""
    hand = [sts_sim.Card.BladeDance]
    powers = {"Shiv": 1}
    set_scenario(game, hand=hand, energy=3, player_powers=powers)
    sim = make_sim(hand=hand, energy=3, player_powers=powers)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Prepared
# ---------------------------------------------------------------------------

def test_prepared_base(game):
    """Prepared draws 1 and discards 1 at zero cost."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        sts_sim.Card.Prepared, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)


def test_prepared_upgraded(game):
    """Upgraded Prepared draws 2 and discards 2."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        (sts_sim.Card.Prepared, True), sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    state = play_card_both(game, sim, hand_index=0, choices=[0, 0])
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Deadly Poison
# ---------------------------------------------------------------------------

def test_deadly_poison_base(game):
    """Deadly Poison applies 1 Poison to enemy."""
    hand = [sts_sim.Card.DeadlyPoison]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_deadly_poison_stacks(game):
    """Deadly Poison stacks with existing Poison."""
    hand = [sts_sim.Card.DeadlyPoison]
    monster_powers = {"Poison": 2}
    set_scenario(game, hand=hand, energy=3, monster_hp=10, monster_powers=monster_powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=10, monster_powers=monster_powers)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)


def test_deadly_poison_upgraded(game):
    """Upgraded Deadly Poison costs 0 energy."""
    hand = [(sts_sim.Card.DeadlyPoison, True)]
    set_scenario(game, hand=hand, energy=0, monster_hp=10)
    sim = make_sim(hand=hand, energy=0, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Acrobatics
# ---------------------------------------------------------------------------

def test_acrobatics_base(game):
    """Acrobatics draws 3 cards and discards 1."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        sts_sim.Card.Acrobatics, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)


def test_acrobatics_upgraded(game):
    """Upgraded Acrobatics draws 4 cards and discards 1."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        (sts_sim.Card.Acrobatics, True), sts_sim.Card.DefendGreen,
    ]
    set_scenario(game, hand=hand, draw_pile=draw_pile, energy=3)
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# Accuracy
# ---------------------------------------------------------------------------

def test_accuracy_upgraded_costs_zero(game):
    """Upgraded Accuracy costs 0 energy."""
    hand = [(sts_sim.Card.AccuracyCard, True)]
    set_scenario(game, hand=hand, energy=0)
    sim = make_sim(hand=hand, energy=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ---------------------------------------------------------------------------
# After Image
# ---------------------------------------------------------------------------

def test_after_image_upgraded_costs_zero(game):
    """Upgraded After Image costs 0 energy."""
    hand = [(sts_sim.Card.AfterImageCard, True)]
    set_scenario(game, hand=hand, energy=0)
    sim = make_sim(hand=hand, energy=0)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
