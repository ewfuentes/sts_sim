"""Live tests for Defect Common cards.

Each test uses set_scenario to configure exact game state, then plays a card
in both the live game and simulator, asserting that state matches afterward.
"""
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches,
)


# ===================================================================
# Ball Lightning — Attack, Cost 1, 1 HIT + Channel 1 Lightning.
# Upgrade: 2 HIT + Channel 1 Lightning.
# ===================================================================


def test_ball_lightning_damage_and_channel(game):
    """Ball Lightning deals 1 damage and channels Lightning."""
    hand = [sts_sim.Card.BallLightning]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_ball_lightning_upgraded_deals_2(game):
    """Upgraded Ball Lightning deals 2 damage."""
    hand = [(sts_sim.Card.BallLightning, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_ball_lightning_full_orb_slots(game):
    """Ball Lightning with full orb slots evokes oldest orb."""
    hand = [sts_sim.Card.BallLightning]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Frost", "Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Frost", "Frost", "Frost"])

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Barrage — Attack, Cost 1, 1 HIT per Orb.
# Upgrade: 1 HIT per Orb +1.
# ===================================================================


def test_barrage_hits_per_orb(game):
    """Barrage deals hits equal to number of orbs."""
    hand = [sts_sim.Card.Barrage]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning", "Frost", "Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning", "Frost", "Dark"])

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_barrage_no_orbs(game):
    """Barrage with no orbs deals no damage."""
    hand = [sts_sim.Card.Barrage]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_barrage_upgraded_extra_hit(game):
    """Upgraded Barrage deals one extra hit."""
    hand = [(sts_sim.Card.Barrage, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning", "Frost"])

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_barrage_with_strength(game):
    """Barrage benefits from Strength on each hit."""
    hand = [sts_sim.Card.Barrage]
    powers = {"Strength": 2}

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning", "Frost"],
                         player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning", "Frost"],
                   player_powers=powers)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Beam Cell — Attack, Cost 0, die-dependent VULN.
# ===================================================================


def test_beam_cell_vuln_on_low_roll(game):
    """Beam Cell applies Vulnerable on low die roll.

    Note: set_scenario sets die=1 by default, which is in the [1][2][3]
    range that applies VULN.
    """
    hand = [sts_sim.Card.BeamCell]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_beam_cell_upgraded_always_vuln(game):
    """Upgraded Beam Cell always applies Vulnerable."""
    hand = [(sts_sim.Card.BeamCell, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Claw — Attack, Cost 0, 1 HIT + conditional bonus.
# ===================================================================


def test_claw_base_no_bonus(game):
    """Claw deals base 1 damage when discard top is not cost 0."""
    hand = [sts_sim.Card.Claw]
    discard = [sts_sim.Card.DefendBlue]  # cost 1

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_claw_bonus_from_cost_0_discard(game):
    """Claw deals 2 damage when discard top is cost 0."""
    hand = [sts_sim.Card.Claw]
    discard = [sts_sim.Card.Claw]  # cost 0

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_claw_upgraded_bonus(game):
    """Upgraded Claw deals 4 damage when discard top is cost 0."""
    hand = [(sts_sim.Card.Claw, True)]
    discard = [sts_sim.Card.BeamCell]  # cost 0

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_claw_bonus_stacks_with_strength(game):
    """Claw bonus stacks with Strength."""
    hand = [sts_sim.Card.Claw]
    discard = [sts_sim.Card.Claw]  # cost 0
    powers = {"Strength": 2}

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         discard_pile=discard, player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   discard_pile=discard, player_powers=powers)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Compile Driver — Attack, Cost 1, 1 HIT + draw per unique orb type.
# ===================================================================


def test_compile_driver_draws_per_unique_orb(game):
    """Compile Driver draws cards for each unique orb type."""
    hand = [sts_sim.Card.CompileDriver]
    draw = [
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue,
    ]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning", "Frost", "Lightning"],
                         draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning", "Frost", "Lightning"],
                   draw_pile=draw)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_compile_driver_no_orbs(game):
    """Compile Driver with no orbs draws nothing."""
    hand = [sts_sim.Card.CompileDriver]
    draw = [
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue,
    ]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   draw_pile=draw)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_compile_driver_upgraded(game):
    """Upgraded Compile Driver deals 2 damage."""
    hand = [(sts_sim.Card.CompileDriver, True)]
    draw = [
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
        sts_sim.Card.StrikeBlue,
    ]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Dark"], draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Dark"], draw_pile=draw)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# ===================================================================
# Go for the Eyes — Attack, Cost 0, die-dependent WEAK.
# ===================================================================


def test_go_for_the_eyes_no_weak_on_low_roll(game):
    """Go for the Eyes does not apply Weak on low die roll.

    set_scenario sets die=1, which is in the [1][2][3] range (no WEAK).
    """
    hand = [sts_sim.Card.GoForTheEyes]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_go_for_the_eyes_upgraded_always_weak(game):
    """Upgraded Go for the Eyes always applies Weak."""
    hand = [(sts_sim.Card.GoForTheEyes, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Sweeping Beam — Attack, Cost 1, AOE 1 HIT + Draw 1.
# ===================================================================


def test_sweeping_beam_aoe_and_draw(game):
    """Sweeping Beam hits all enemies and draws a card."""
    hand = [sts_sim.Card.SweepingBeam]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   draw_pile=draw)

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_sweeping_beam_upgraded(game):
    """Upgraded Sweeping Beam deals 2 damage to all enemies."""
    hand = [(sts_sim.Card.SweepingBeam, True)]
    draw = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   draw_pile=draw)

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_sweeping_beam_with_strength(game):
    """Sweeping Beam with Strength hits all enemies for boosted damage."""
    hand = [sts_sim.Card.SweepingBeam]
    powers = {"Strength": 3}
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         player_powers=powers, draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers=powers, draw_pile=draw)

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Charge Battery — Skill, Cost 1, 2 BLK + conditional energy.
# ===================================================================


def test_charge_battery_block_no_energy(game):
    """Charge Battery grants 2 block without enough orbs."""
    hand = [sts_sim.Card.ChargeBattery]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         orbs=["Lightning", "Frost"])
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   orbs=["Lightning", "Frost"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_charge_battery_block_and_energy(game):
    """Charge Battery grants block and energy with 3 orbs."""
    hand = [sts_sim.Card.ChargeBattery]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         orbs=["Lightning", "Frost", "Dark"])
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   orbs=["Lightning", "Frost", "Dark"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_charge_battery_upgraded(game):
    """Upgraded Charge Battery grants 3 block."""
    hand = [(sts_sim.Card.ChargeBattery, True)]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         orbs=["Lightning"])
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   orbs=["Lightning"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# Chaos — Skill, Cost 1, Channel orb based on die.
# ===================================================================


def test_chaos_channels_lightning(game):
    """Chaos channels Lightning on die roll 1 (default die=1)."""
    hand = [sts_sim.Card.Chaos]

    setup = set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_chaos_upgraded_costs_0(game):
    """Upgraded Chaos costs 0."""
    hand = [(sts_sim.Card.Chaos, True)]

    setup = set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


# ===================================================================
# Coolheaded — Skill, Cost 1, Channel 1 Frost.
# ===================================================================


def test_coolheaded_channels_frost(game):
    """Coolheaded channels a Frost orb."""
    hand = [sts_sim.Card.Coolheaded]

    setup = set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_coolheaded_upgraded_draws(game):
    """Upgraded Coolheaded channels Frost and draws a card."""
    hand = [(sts_sim.Card.Coolheaded, True)]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, draw_pile=draw)
    sim = make_sim(hand=hand, energy=3, draw_pile=draw)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_coolheaded_full_orb_slots(game):
    """Coolheaded with full orb slots evokes oldest orb."""
    hand = [sts_sim.Card.Coolheaded]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning", "Lightning", "Lightning"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning", "Lightning", "Lightning"])

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Leap — Skill, Cost 1, 2 BLK to any player.
# ===================================================================


def test_leap_block_to_self(game):
    """Leap grants 2 block to self."""
    hand = [sts_sim.Card.Leap]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_leap_upgraded_block(game):
    """Upgraded Leap grants 3 block."""
    hand = [(sts_sim.Card.Leap, True)]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# Recursion — Skill, Cost 1, Evoke 1 Orb + Channel same type.
# ===================================================================


def test_recursion_evokes_and_rechannels_lightning(game):
    """Recursion evokes and re-channels a Lightning orb."""
    hand = [sts_sim.Card.Recursion]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning"])

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_recursion_evokes_frost(game):
    """Recursion evokes Frost and re-channels it."""
    hand = [sts_sim.Card.Recursion]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         player_block=0, orbs=["Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_block=0, orbs=["Frost"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


def test_recursion_upgraded_costs_0(game):
    """Upgraded Recursion costs 0."""
    hand = [(sts_sim.Card.Recursion, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Dark"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


def test_recursion_no_orbs(game):
    """Recursion with no orbs does nothing."""
    hand = [sts_sim.Card.Recursion]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Steam Barrier — Skill, Cost 0, 1 BLK + conditional bonus.
# ===================================================================


def test_steam_barrier_base_no_bonus(game):
    """Steam Barrier grants 1 block when discard top is not cost 0."""
    hand = [sts_sim.Card.SteamBarrier]
    discard = [sts_sim.Card.DefendBlue]  # cost 1

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_steam_barrier_bonus_from_cost_0(game):
    """Steam Barrier grants 2 block when discard top is cost 0."""
    hand = [sts_sim.Card.SteamBarrier]
    discard = [sts_sim.Card.Claw]  # cost 0

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_steam_barrier_upgraded_bonus(game):
    """Upgraded Steam Barrier grants 3 block when discard top is cost 0."""
    hand = [(sts_sim.Card.SteamBarrier, True)]
    discard = [sts_sim.Card.BeamCell]  # cost 0

    setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                         discard_pile=discard)
    sim = make_sim(hand=hand, energy=3, player_block=0,
                   discard_pile=discard)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_steam_barrier_empty_discard(game):
    """Steam Barrier with empty discard pile grants only base block."""
    hand = [sts_sim.Card.SteamBarrier]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
