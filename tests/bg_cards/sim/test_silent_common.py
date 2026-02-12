"""Simulator tests for Silent Common cards."""
import sts_sim
from tests.live.conftest import make_sim


# ---------------------------------------------------------------------------
# Poisoned Stab
# ---------------------------------------------------------------------------

def test_poisoned_stab_base():
    """Poisoned Stab deals 1 damage, applies 1 Poison, and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.PoisonedStab], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 9
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1
    assert sim.player.energy == 2
    # Card should be in exhaust pile, not discard
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.PoisonedStab in exhaust_cards
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.PoisonedStab not in discard_cards


def test_poisoned_stab_upgraded():
    """Upgraded Poisoned Stab applies 2 Poison."""
    sim = make_sim(
        hand=[(sts_sim.Card.PoisonedStab, True)], energy=3, monster_hp=10,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 9
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.PoisonedStab in exhaust_cards


def test_poisoned_stab_with_strength():
    """Poisoned Stab with 2 STR adds damage per HIT."""
    sim = make_sim(
        hand=[sts_sim.Card.PoisonedStab], energy=3, monster_hp=10,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7  # 1 HIT + 2 STR = 3 damage
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.PoisonedStab in exhaust_cards


# ---------------------------------------------------------------------------
# Dagger Throw
# ---------------------------------------------------------------------------

def test_dagger_throw_base():
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
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, monster_hp=10)
    # Play Dagger Throw targeting enemy, then choose card 0 to discard
    sim.play_card(0, 0, 0)
    assert sim.get_monsters()[0].hp == 8  # 2 HIT = 2 damage
    # Hand: was 4, played 1 = 3, drew 1 = 4, discarded 1 = 3
    assert len(sim.get_hand()) == 3
    assert sim.player.energy == 2


def test_dagger_throw_upgraded():
    """Upgraded Dagger Throw deals 3 HIT."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[(sts_sim.Card.DaggerThrow, True)],
        draw_pile=draw_pile, energy=3, monster_hp=10,
    )
    sim.play_card(0, 0, 0)
    assert sim.get_monsters()[0].hp == 7  # 3 HIT = 3 damage


def test_dagger_throw_discard_triggers_after_image():
    """Dagger Throw discard triggers After Image."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[sts_sim.Card.DaggerThrow, sts_sim.Card.StrikeGreen],
        draw_pile=draw_pile, energy=3, player_block=0, monster_hp=10,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, 0, 0)
    assert sim.get_monsters()[0].hp == 8  # 2 HIT = 2 damage
    assert sim.player.block == 1  # After Image triggers on discard


# ---------------------------------------------------------------------------
# Dagger Spray
# ---------------------------------------------------------------------------

def test_dagger_spray_base():
    """Dagger Spray hits all enemies twice."""
    sim = make_sim(
        hand=[sts_sim.Card.DaggerSpray], energy=3,
        monsters=[{"hp": 10}, {"hp": 8}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 8  # 10 - 2 HIT
    assert monsters[1].hp == 6  # 8 - 2 HIT
    assert sim.player.energy == 2


def test_dagger_spray_upgraded():
    """Upgraded Dagger Spray hits all enemies three times."""
    sim = make_sim(
        hand=[(sts_sim.Card.DaggerSpray, True)], energy=3,
        monsters=[{"hp": 10}, {"hp": 8}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 7  # 10 - 3 HIT
    assert monsters[1].hp == 5  # 8 - 3 HIT


def test_dagger_spray_with_strength():
    """Dagger Spray with 1 STR adds to each HIT on each enemy."""
    sim = make_sim(
        hand=[sts_sim.Card.DaggerSpray], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}],
        player_powers={"Strength": 1},
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    # 2 HIT at 2 damage each (1+1 STR) = 4 per enemy
    assert monsters[0].hp == 6
    assert monsters[1].hp == 6


# ---------------------------------------------------------------------------
# Sneaky Strike
# ---------------------------------------------------------------------------

def test_sneaky_strike_no_discard():
    """Sneaky Strike deals 3 damage without discard, no energy refund."""
    sim = make_sim(hand=[sts_sim.Card.SneakyStrike], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7  # 3 HIT = 3 damage
    assert sim.player.energy == 1  # costs 2


def test_sneaky_strike_with_discard():
    """Sneaky Strike refunds 2 energy when a card was discarded this turn."""
    sim = make_sim(
        hand=[sts_sim.Card.Survivor, sts_sim.Card.SneakyStrike,
              sts_sim.Card.StrikeGreen],
        energy=3, monster_hp=10,
    )
    # Play Survivor (cost 1, discard Strike at index 0 of remaining)
    sim.play_card(0, None, 0)
    # Energy: 3 - 1 (Survivor cost) = 2
    # Now play Sneaky Strike (now at index 0) targeting enemy
    sim.play_card(0, 0)
    # Sneaky Strike: costs 2, but refunds 2 because we discarded this turn
    assert sim.get_monsters()[0].hp == 7  # 3 HIT = 3 damage
    assert sim.player.energy == 2  # 2 - 2 (cost) + 2 (refund) = 2


def test_sneaky_strike_upgraded():
    """Upgraded Sneaky Strike deals 4 base + 1 STR = 5 damage."""
    sim = make_sim(
        hand=[(sts_sim.Card.SneakyStrike, True)], energy=3, monster_hp=20,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, 0)
    # Single-hit: 4 base + 1 STR = 5 damage
    assert sim.get_monsters()[0].hp == 15
    assert sim.player.energy == 1  # costs 2


# ---------------------------------------------------------------------------
# Slice
# ---------------------------------------------------------------------------

def test_slice_base_no_shiv():
    """Slice deals 1 damage at zero cost without SHIV."""
    sim = make_sim(hand=[sts_sim.Card.Slice], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 9
    assert sim.player.energy == 3  # costs 0


def test_slice_with_shiv():
    """Slice deals bonus damage when a shiv was used this turn."""
    sim = make_sim(
        hand=[sts_sim.Card.Slice], energy=3, monster_hp=10,
        player_powers={"Shiv": 1},
    )
    sim.use_shiv(0)  # 1 damage, hp=9, shivs_played=1
    sim.play_card(0, 0)  # 1 base + 1 shiv bonus = 2 damage, hp=7
    assert sim.get_monsters()[0].hp == 7


def test_slice_upgraded_with_shiv():
    """Upgraded Slice+ with shiv used and STR."""
    sim = make_sim(
        hand=[(sts_sim.Card.Slice, True)], energy=3, monster_hp=10,
        player_powers={"Shiv": 1, "Strength": 1},
    )
    sim.use_shiv(0)  # (1 + 1 STR) = 2 damage, hp=8
    sim.play_card(0, 0)  # (2 base + 1 shiv bonus + 1 STR) = 4 damage, hp=4
    assert sim.get_monsters()[0].hp == 4


# ---------------------------------------------------------------------------
# Backflip
# ---------------------------------------------------------------------------

def test_backflip_base():
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
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert len(sim.get_hand()) == 6  # 4 remaining + 2 drawn
    assert sim.player.energy == 2


def test_backflip_upgraded():
    """Upgraded Backflip grants 2 block and draws 2 cards."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[(sts_sim.Card.Backflip, True)],
        draw_pile=draw_pile, energy=3, player_block=0,
    )
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert len(sim.get_hand()) == 2  # 0 remaining + 2 drawn


def test_backflip_reshuffle():
    """Backflip with insufficient draw pile reshuffles discard."""
    draw_pile = [sts_sim.Card.StrikeGreen]
    discard_pile = [
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
        sts_sim.Card.DefendGreen,
    ]
    sim = make_sim(
        hand=[sts_sim.Card.Backflip],
        draw_pile=draw_pile, discard_pile=discard_pile,
        energy=3, player_block=0,
    )
    sim.play_card(0, None)
    assert sim.player.block == 1
    # Should have drawn 2 cards total (1 from draw, reshuffle, 1 more)
    assert len(sim.get_hand()) == 2


# ---------------------------------------------------------------------------
# Dodge and Roll
# ---------------------------------------------------------------------------

def test_dodge_and_roll_self():
    """Dodge and Roll assigns 2 BLK to self."""
    sim = make_sim(
        hand=[sts_sim.Card.DodgeAndRoll], energy=3, player_block=0,
    )
    # Choice 0 = assign to self for each BLK
    sim.play_card(0, None, 0)
    assert sim.player.block == 2
    assert sim.player.energy == 2


# ---------------------------------------------------------------------------
# Deflect
# ---------------------------------------------------------------------------

def test_deflect_base_no_shiv():
    """Deflect grants 1 block at zero cost without SHIV."""
    sim = make_sim(hand=[sts_sim.Card.Deflect], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.player.energy == 3  # costs 0


def test_deflect_with_shiv():
    """Deflect grants bonus block with SHIV."""
    sim = make_sim(
        hand=[sts_sim.Card.Deflect], energy=3, player_block=0,
        player_powers={"Shiv": 1},
    )
    sim.play_card(0, None)
    assert sim.player.block == 2  # 1 base + 1 SHIV bonus


def test_deflect_upgraded_with_shiv():
    """Upgraded Deflect with SHIV grants 3 block total."""
    sim = make_sim(
        hand=[(sts_sim.Card.Deflect, True)], energy=3, player_block=0,
        player_powers={"Shiv": 1},
    )
    sim.play_card(0, None)
    assert sim.player.block == 3  # 2 base + 1 SHIV bonus


# ---------------------------------------------------------------------------
# Cloak and Dagger
# ---------------------------------------------------------------------------

def test_cloak_and_dagger_base():
    """Cloak and Dagger gives 1 SHIV and 1 block."""
    sim = make_sim(
        hand=[sts_sim.Card.CloakAndDagger], energy=3, player_block=0,
    )
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 1
    assert sim.player.energy == 2


def test_cloak_and_dagger_upgraded():
    """Upgraded Cloak and Dagger gives 2 SHIV and 1 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.CloakAndDagger, True)], energy=3, player_block=0,
    )
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 2
    assert sim.player.energy == 2


def test_cloak_and_dagger_shiv_with_accuracy():
    """Cloak and Dagger SHIV interacts with Accuracy when used."""
    sim = make_sim(
        hand=[sts_sim.Card.CloakAndDagger, sts_sim.Card.Slice],
        energy=3, player_block=0, monster_hp=10,
        player_powers={"Accuracy": 1},
    )
    sim.play_card(0, None)  # Play Cloak and Dagger -> 1 SHIV, 1 block
    sim.use_shiv(0)  # (1 + 1 Accuracy) = 2 damage, hp=8
    sim.play_card(0, 0)  # Slice: 1 base + 1 shiv bonus = 2 damage, hp=6
    assert sim.get_monsters()[0].hp == 6


# ---------------------------------------------------------------------------
# Blade Dance
# ---------------------------------------------------------------------------

def test_blade_dance_base():
    """Blade Dance gives 2 SHIV tokens."""
    sim = make_sim(hand=[sts_sim.Card.BladeDance], energy=3)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 2
    assert sim.player.energy == 2


def test_blade_dance_upgraded():
    """Upgraded Blade Dance gives 3 SHIV tokens."""
    sim = make_sim(hand=[(sts_sim.Card.BladeDance, True)], energy=3)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 3
    assert sim.player.energy == 2


def test_blade_dance_stacks():
    """Blade Dance SHIV stacks with existing SHIV."""
    sim = make_sim(
        hand=[sts_sim.Card.BladeDance], energy=3,
        player_powers={"Shiv": 1},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 3  # 1 + 2


# ---------------------------------------------------------------------------
# Prepared
# ---------------------------------------------------------------------------

def test_prepared_base():
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
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    sim.play_card(0, None, 0)
    # Hand: 4 - 1 (played) + 1 (draw) - 1 (discard) = 3
    assert len(sim.get_hand()) == 3
    assert sim.player.energy == 3  # costs 0


def test_prepared_upgraded():
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
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    # Upgraded: draw 2, discard 2 — choice 0 for each discard
    sim.play_card(0, None, 0)
    # Hand: 4 - 1 (played) + 2 (draw) - 2 (discard) = 3
    assert len(sim.get_hand()) == 3
    assert sim.player.energy == 3


def test_prepared_discard_triggers_after_image():
    """Prepared discard triggers After Image."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[sts_sim.Card.Prepared, sts_sim.Card.StrikeGreen],
        draw_pile=draw_pile, energy=3, player_block=0,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, None, 0)
    assert sim.player.block == 1  # After Image triggers on discard


# ---------------------------------------------------------------------------
# Deadly Poison
# ---------------------------------------------------------------------------

def test_deadly_poison_base():
    """Deadly Poison applies 1 Poison to enemy."""
    sim = make_sim(hand=[sts_sim.Card.DeadlyPoison], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1
    assert sim.player.energy == 2


def test_deadly_poison_stacks():
    """Deadly Poison stacks with existing Poison."""
    sim = make_sim(
        hand=[sts_sim.Card.DeadlyPoison], energy=3, monster_hp=10,
        monster_powers={"Poison": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 3


def test_deadly_poison_upgraded():
    """Upgraded Deadly Poison costs 0 energy."""
    sim = make_sim(
        hand=[(sts_sim.Card.DeadlyPoison, True)], energy=0, monster_hp=10,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1
    assert sim.player.energy == 0  # costs 0


# ---------------------------------------------------------------------------
# Acrobatics
# ---------------------------------------------------------------------------

def test_acrobatics_base():
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
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    sim.play_card(0, None, 0)
    # Hand: 3 - 1 (played) + 3 (draw) - 1 (discard) = 4
    assert len(sim.get_hand()) == 4
    assert sim.player.energy == 2


def test_acrobatics_upgraded():
    """Upgraded Acrobatics draws 4 cards and discards 1."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    hand = [
        (sts_sim.Card.Acrobatics, True), sts_sim.Card.DefendGreen,
    ]
    sim = make_sim(hand=hand, draw_pile=draw_pile, energy=3)
    sim.play_card(0, None, 0)
    # Hand: 2 - 1 (played) + 4 (draw) - 1 (discard) = 4
    assert len(sim.get_hand()) == 4


def test_acrobatics_discard_triggers_after_image():
    """Acrobatics discard triggers After Image."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[sts_sim.Card.Acrobatics, sts_sim.Card.DefendGreen,
              sts_sim.Card.DefendGreen],
        draw_pile=draw_pile, energy=3, player_block=0,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, None, 0)
    assert sim.player.block == 1  # After Image triggers on discard


# ---------------------------------------------------------------------------
# Accuracy
# ---------------------------------------------------------------------------

def test_accuracy_boosts_shiv():
    """Accuracy boosts shiv use damage."""
    sim = make_sim(
        hand=[sts_sim.Card.AccuracyCard, sts_sim.Card.Slice],
        energy=3, monster_hp=10,
        player_powers={"Shiv": 1},
    )
    sim.play_card(0, None)  # Play Accuracy -> Accuracy:1
    sim.use_shiv(0)  # (1 + 1 Accuracy) = 2 damage, hp=8
    sim.play_card(0, 0)  # Slice: 1 base + 1 shiv bonus = 2 damage, hp=6
    assert sim.get_monsters()[0].hp == 6


def test_accuracy_stacks():
    """Accuracy stacks with multiple plays, boosting shiv damage."""
    sim = make_sim(
        hand=[sts_sim.Card.AccuracyCard, sts_sim.Card.AccuracyCard,
              sts_sim.Card.Slice],
        energy=3, monster_hp=10,
        player_powers={"Shiv": 1},
    )
    sim.play_card(0, None)  # Play first Accuracy -> Accuracy:1
    sim.play_card(0, None)  # Play second Accuracy -> Accuracy:2
    sim.use_shiv(0)  # (1 + 2 Accuracy) = 3 damage, hp=7
    sim.play_card(0, 0)  # Slice: 1 base + 1 shiv bonus = 2 damage, hp=5
    assert sim.get_monsters()[0].hp == 5


def test_accuracy_upgraded_costs_zero():
    """Upgraded Accuracy costs 0 energy."""
    sim = make_sim(
        hand=[(sts_sim.Card.AccuracyCard, True)], energy=0,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 0
    assert sim.get_player_power(sts_sim.PowerType.Accuracy) == 1


# ---------------------------------------------------------------------------
# After Image
# ---------------------------------------------------------------------------

def test_after_image_triggers_on_survivor_discard():
    """After Image triggers on discard from Survivor."""
    sim = make_sim(
        hand=[sts_sim.Card.AfterImageCard, sts_sim.Card.Survivor,
              sts_sim.Card.StrikeGreen],
        energy=3, player_block=0,
    )
    sim.play_card(0, None)  # Play After Image (cost 1, energy -> 2)
    sim.play_card(0, None, 0)  # Play Survivor, discard Strike
    # Survivor: 2 BLK + After Image: 1 BLK = 3 total
    assert sim.player.block == 3


def test_after_image_once_per_discard_event():
    """After Image triggers once per discard event, not per card discarded."""
    draw_pile = [
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
        sts_sim.Card.StrikeGreen,
    ]
    sim = make_sim(
        hand=[sts_sim.Card.Acrobatics, sts_sim.Card.DefendGreen,
              sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen],
        draw_pile=draw_pile, energy=3, player_block=0,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, None, 0)  # Play Acrobatics, draw 3, discard 1
    # After Image triggers once for the discard event = 1 BLK
    assert sim.player.block == 1


def test_after_image_upgraded_costs_zero():
    """Upgraded After Image costs 0 energy."""
    sim = make_sim(
        hand=[(sts_sim.Card.AfterImageCard, True)], energy=0,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 0
    assert sim.get_player_power(sts_sim.PowerType.AfterImage) == 1


def test_after_image_does_not_trigger_on_exhaust():
    """After Image does not trigger on exhaust."""
    sim = make_sim(
        hand=[sts_sim.Card.PoisonedStab], energy=3, player_block=0,
        monster_hp=10,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, 0)
    # Poisoned Stab exhausts, not discards — After Image should NOT trigger
    assert sim.player.block == 0
