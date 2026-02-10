"""Tier 20: Watcher base (unupgraded) card tests.

Tests verify that Watcher card mechanics — stances, scry, miracles, mantra,
multi-hit attacks, and exhaust — match between the live BG mod game and the
Rust simulator.

Because make_sim() in conftest hardcodes Character.Ironclad, this file uses
a local make_watcher_sim() that creates a CombatState with Character.Watcher
so stance mechanics work correctly.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
    CARD_TO_BG,
)


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=30, monster_block=0, monster_powers=None,
                     monsters=None):
    """Create a simulator CombatState with Character.Watcher.

    Mirrors make_sim() from conftest but uses the Watcher character so that
    stance mechanics (Wrath, Calm, Divinity) work correctly.
    """
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 30), "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Jaw Worm", monster_hp, "jaw_worm", "A", False)
        if monster_block > 0:
            monster.add_block(monster_block)
        if monster_powers:
            for power_name, amount in monster_powers.items():
                pt = getattr(sts_sim.PowerType, power_name)
                monster.apply_power(pt, amount)
        monster_list = [monster]

    sim = sts_sim.CombatState.new_with_character(
        monster_list, seed=0, character=sts_sim.Character.Watcher,
    )
    sim.set_player_energy(energy)
    sim.set_player_hp(player_hp)
    sim.set_player_block(player_block)

    if player_relics is not None:
        sim.clear_relics()
        for relic in player_relics:
            sim.add_relic(relic)

    if player_powers:
        for power_name, amount in player_powers.items():
            pt = getattr(sts_sim.PowerType, power_name)
            sim.apply_player_power(pt, amount)

    for card_spec in draw_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    return sim


def _card_spec_card(card_spec):
    if isinstance(card_spec, tuple):
        return card_spec[0]
    return card_spec


def _card_spec_upgraded(card_spec):
    if isinstance(card_spec, tuple):
        return card_spec[1]
    return False


# ===================================================================
# STARTERS
# ===================================================================


# ── StrikePurple: cost 1, damage 1, targeted ─────────────────────────

def test_strike_purple(game):
    """StrikePurple deals base damage to target monster."""
    hand = [sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikePurple,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── DefendPurple: cost 1, block 1 ───────────────────────────────────

def test_defend_purple(game):
    """DefendPurple grants block to the player."""
    hand = [sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendPurple)

    assert_player_matches(state, sim)


# ── Eruption: cost 2, damage 2, enters Wrath ────────────────────────

def test_eruption(game):
    """Eruption deals damage and enters Wrath stance."""
    hand = [sts_sim.Card.Eruption]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Eruption,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Vigilance: cost 2, block 2, enters Calm ─────────────────────────

def test_vigilance(game):
    """Vigilance grants block and enters Calm stance."""
    hand = [sts_sim.Card.Vigilance]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance)

    assert_player_matches(state, sim)


# ===================================================================
# COMMON ATTACKS
# ===================================================================


# ── FlurryOfBlows: cost 0, damage 1, targeted ───────────────────────

def test_flurry_of_blows(game):
    """FlurryOfBlows deals damage for 0 energy."""
    hand = [sts_sim.Card.FlurryOfBlows]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FlurryOfBlows,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── EmptyFist: cost 1, damage 2, exits stance ───────────────────────

def test_empty_fist(game):
    """EmptyFist deals damage and exits current stance."""
    hand = [sts_sim.Card.EmptyFist]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyFist,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Consecrate: cost 0, damage 1, AoE (no target) ───────────────────

def test_consecrate(game):
    """Consecrate deals AoE damage for 0 energy."""
    hand = [sts_sim.Card.Consecrate]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Consecrate)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── CutThroughFate: cost 1, damage 1, scry 2, targeted ──────────────

def test_cut_through_fate(game):
    """CutThroughFate deals damage and scrys."""
    hand = [sts_sim.Card.CutThroughFate]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CutThroughFate,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── JustLucky: cost 0, damage 1, block 1, scry 1, targeted ──────────

def test_just_lucky(game):
    """JustLucky deals damage, gains block, and scrys."""
    hand = [sts_sim.Card.JustLucky]
    draw = [sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.JustLucky,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# COMMON SKILLS
# ===================================================================


# ── EmptyBody: cost 1, block 2, exits stance ────────────────────────

def test_empty_body(game):
    """EmptyBody gains block and exits current stance."""
    hand = [sts_sim.Card.EmptyBody]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyBody)

    assert_player_matches(state, sim)


# ── Protect: cost 2, block 3 ────────────────────────────────────────

def test_protect(game):
    """Protect gains block."""
    hand = [sts_sim.Card.Protect]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Protect)

    assert_player_matches(state, sim)


# ── Halt: cost 0, block 1, extra block in Wrath ─────────────────────

def test_halt(game):
    """Halt gains block for 0 energy."""
    hand = [sts_sim.Card.Halt]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Halt)

    assert_player_matches(state, sim)


# ── ThirdEye: cost 1, block 2, scry 3 ───────────────────────────────

def test_third_eye(game):
    """ThirdEye gains block and scrys."""
    hand = [sts_sim.Card.ThirdEye]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ThirdEye)

    assert_player_matches(state, sim)


# ── Tranquility: cost 1, exhaust, enters Calm ───────────────────────

def test_tranquility(game):
    """Tranquility enters Calm and exhausts itself."""
    hand = [sts_sim.Card.Tranquility]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Tranquility)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Crescendo: cost 0, exhaust, enters Wrath ────────────────────────

def test_crescendo(game):
    """Crescendo enters Wrath and exhausts itself for 0 energy."""
    hand = [sts_sim.Card.Crescendo]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Collect: cost 1, exhaust, generates miracles ────────────────────

def test_collect(game):
    """Collect generates Miracle cards and exhausts."""
    hand = [sts_sim.Card.Collect]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Collect)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# UNCOMMON ATTACKS
# ===================================================================


# ── CrushJoints: cost 1, damage 1, apply weak 1, targeted ───────────

def test_crush_joints(game):
    """CrushJoints deals damage and applies Weak."""
    hand = [sts_sim.Card.CrushJoints]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CrushJoints,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── FearNoEvil: cost 1, damage 2, enters Calm if attacking, targeted ──

def test_fear_no_evil(game):
    """FearNoEvil deals damage and conditionally enters Calm."""
    hand = [sts_sim.Card.FearNoEvil]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FearNoEvil,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── ForeignInfluence: cost 2, damage 3, targeted ────────────────────

def test_foreign_influence(game):
    """ForeignInfluence deals damage."""
    hand = [sts_sim.Card.ForeignInfluence]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForeignInfluence,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── SashWhip: cost 1, damage 2, apply vulnerable 1, targeted ────────

def test_sash_whip(game):
    """SashWhip deals damage and applies Vulnerable."""
    hand = [sts_sim.Card.SashWhip]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SashWhip,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Tantrum: cost 1, damage 2, multi-hit, enters Wrath, targeted ────

def test_tantrum(game):
    """Tantrum deals multi-hit damage and enters Wrath."""
    hand = [sts_sim.Card.Tantrum]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Tantrum,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── CarveReality: cost 2, damage 3, targeted (adds Smite to hand) ───

def test_carve_reality(game):
    """CarveReality deals damage and adds a Smite to hand."""
    hand = [sts_sim.Card.CarveReality]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CarveReality,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── SandsOfTime: cost 2, damage 3, targeted ─────────────────────────

def test_sands_of_time(game):
    """SandsOfTime deals damage."""
    hand = [sts_sim.Card.SandsOfTime]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SandsOfTime,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── WindmillStrike: cost 2, damage 2, targeted ──────────────────────

def test_windmill_strike(game):
    """WindmillStrike deals base damage (first play, not retained)."""
    hand = [sts_sim.Card.WindmillStrike]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WindmillStrike,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Wallop: cost 2, damage 2, block = unblocked damage, targeted ────

def test_wallop(game):
    """Wallop deals damage and gains block equal to unblocked damage."""
    hand = [sts_sim.Card.Wallop]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Wallop,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Weave: cost 0, damage 1, targeted ───────────────────────────────

def test_weave(game):
    """Weave deals damage for 0 energy."""
    hand = [sts_sim.Card.Weave]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Weave,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── SignatureMove: cost 2, damage 6, targeted (only attack in hand) ──

def test_signature_move(game):
    """SignatureMove deals heavy damage when it is the only attack in hand."""
    hand = [sts_sim.Card.SignatureMove]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SignatureMove,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── FlyingSleeves: cost 1, damage 1 x2, targeted ────────────────────

def test_flying_sleeves(game):
    """FlyingSleeves deals multi-hit damage."""
    hand = [sts_sim.Card.FlyingSleeves]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FlyingSleeves,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Conclude: cost 1, damage 1, AoE, ends turn ──────────────────────

def test_conclude(game):
    """Conclude deals AoE damage and ends the turn.

    Play it as the only card so the end-turn is clean.
    """
    hand = [sts_sim.Card.Conclude]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Conclude)

    assert_monsters_match(state, sim)


# ── ReachHeaven: cost 1, damage 2, targeted ──────────────────────────

def test_reach_heaven(game):
    """ReachHeaven deals damage and shuffles Through Violence into draw."""
    hand = [sts_sim.Card.ReachHeaven]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ReachHeaven,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# UNCOMMON SKILLS
# ===================================================================


# ── EmptyMind: cost 1, draw 2, exits stance ─────────────────────────

def test_empty_mind(game):
    """EmptyMind draws cards and exits stance."""
    hand = [sts_sim.Card.EmptyMind]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyMind)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── MeditateCard: cost 1, ends turn, enters Calm ────────────────────

def test_meditate(game):
    """MeditateCard ends the turn and enters Calm.

    Play it alone so end-turn is clean.
    """
    hand = [sts_sim.Card.MeditateCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MeditateCard)

    # MeditateCard ends the turn; just verify player matches
    assert_player_matches(state, sim)


# ── InnerPeace: cost 1, draw 3 if Calm ──────────────────────────────

def test_inner_peace(game):
    """InnerPeace draws cards (3 if in Calm, else enters Calm)."""
    hand = [sts_sim.Card.InnerPeace]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.InnerPeace)

    assert_player_matches(state, sim)


# ── Indignation: cost 1, enter Wrath or apply Vuln ──────────────────

def test_indignation(game):
    """Indignation enters Wrath (from neutral) or applies Vuln (if in Wrath)."""
    hand = [sts_sim.Card.Indignation]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Indignation)

    assert_player_matches(state, sim)


# ── Swivel: cost 2, block 2 ─────────────────────────────────────────

def test_swivel(game):
    """Swivel gains block."""
    hand = [sts_sim.Card.Swivel]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Swivel)

    assert_player_matches(state, sim)


# ── Perseverance: cost 1, block 1 ───────────────────────────────────

def test_perseverance(game):
    """Perseverance gains block (base, not retained)."""
    hand = [sts_sim.Card.Perseverance]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Perseverance)

    assert_player_matches(state, sim)


# ── Pray: cost 1, gain Mantra ───────────────────────────────────────

def test_pray(game):
    """Pray gains Mantra."""
    hand = [sts_sim.Card.Pray]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Pray)

    assert_player_matches(state, sim)


# ── Prostrate: cost 1, block + gain Mantra ──────────────────────────

def test_prostrate(game):
    """Prostrate gains block and Mantra."""
    hand = [sts_sim.Card.Prostrate]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Prostrate)

    assert_player_matches(state, sim)


# ── WreathOfFlameCard: X-cost, exhaust ──────────────────────────────

def test_wreath_of_flame(game):
    """WreathOfFlameCard is an X-cost skill that exhausts."""
    hand = [sts_sim.Card.WreathOfFlameCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WreathOfFlameCard,
                            choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# UNCOMMON POWERS
# ===================================================================


# ── BattleHymnCard: cost 1, power ───────────────────────────────────

def test_battle_hymn_power(game):
    """BattleHymnCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.BattleHymnCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BattleHymnCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── SimmeringFuryCard: cost 2, power ────────────────────────────────

def test_simmering_fury_power(game):
    """SimmeringFuryCard is a power card that costs 2 energy."""
    hand = [sts_sim.Card.SimmeringFuryCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SimmeringFuryCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── MentalFortressCard: cost 1, power ───────────────────────────────

def test_mental_fortress_power(game):
    """MentalFortressCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.MentalFortressCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MentalFortressCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── NirvanaCard: cost 1, power ──────────────────────────────────────

def test_nirvana_power(game):
    """NirvanaCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.NirvanaCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.NirvanaCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── LikeWaterCard: cost 1, power ────────────────────────────────────

def test_like_water_power(game):
    """LikeWaterCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.LikeWaterCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.LikeWaterCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── ForesightCard: cost 1, power ────────────────────────────────────

def test_foresight_power(game):
    """ForesightCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.ForesightCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForesightCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── StudyCard: cost 2, power ────────────────────────────────────────

def test_study_power(game):
    """StudyCard is a power card that costs 2 energy."""
    hand = [sts_sim.Card.StudyCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StudyCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── RushdownCard: cost 1, power ─────────────────────────────────────

def test_rushdown_power(game):
    """RushdownCard is a power card that costs 1 energy."""
    hand = [sts_sim.Card.RushdownCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RushdownCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# RARE ATTACKS
# ===================================================================


# ── Ragnarok: cost 3, damage 1 x4, targeted ─────────────────────────

def test_ragnarok(game):
    """Ragnarok deals multi-hit damage (1 damage x 4 hits)."""
    hand = [sts_sim.Card.Ragnarok]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Ragnarok,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── BrillianceCard: cost 1, damage 2, targeted ──────────────────────

def test_brilliance(game):
    """BrillianceCard deals damage (base + mantra gained)."""
    hand = [sts_sim.Card.BrillianceCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BrillianceCard,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# RARE SKILLS
# ===================================================================


# ── Blasphemy: cost 2, exhaust, enters Divinity ─────────────────────

def test_blasphemy(game):
    """Blasphemy enters Divinity stance, exhausts. Just verify the play."""
    hand = [sts_sim.Card.Blasphemy]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Blasphemy)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── DeusExMachina: cost 0, generates miracles, exhaust ──────────────

def test_deus_ex_machina(game):
    """DeusExMachina generates Miracles and exhausts for 0 energy."""
    hand = [sts_sim.Card.DeusExMachina]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DeusExMachina)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── ScrawlCard: cost 1, draw 5, exhaust ─────────────────────────────

def test_scrawl(game):
    """ScrawlCard draws cards until hand is full and exhausts."""
    hand = [sts_sim.Card.ScrawlCard]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ScrawlCard)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# ── WishCard: cost 3, block 10, exhaust ─────────────────────────────

def test_wish(game):
    """WishCard grants block (or strength choice) and exhausts."""
    hand = [sts_sim.Card.WishCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    # Choose block option (choice 0 = Plated Armor / block)
    state = play_named_card(game, sim, setup, sts_sim.Card.WishCard,
                            choices=[0])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── SpiritShieldCard: cost 2, block per card in hand, exhaust ───────

def test_spirit_shield(game):
    """SpiritShieldCard gains block equal to number of cards in hand."""
    hand = [sts_sim.Card.SpiritShieldCard, sts_sim.Card.StrikePurple,
            sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SpiritShieldCard)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── JudgmentCard: cost 1, kill threshold, targeted skill ────────────

def test_judgment(game):
    """JudgmentCard kills an enemy if HP is at or below threshold.

    Use a monster with HP above threshold to verify no kill.
    """
    hand = [sts_sim.Card.JudgmentCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.JudgmentCard,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── WorshipCard: X-cost, exhaust, gain Mantra ───────────────────────

def test_worship(game):
    """WorshipCard is an X-cost skill that gains Mantra and exhausts."""
    hand = [sts_sim.Card.WorshipCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WorshipCard,
                            choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# RARE POWERS
# ===================================================================


# ── OmegaCard: cost 3, power ────────────────────────────────────────

def test_omega_power(game):
    """OmegaCard is a power card that costs 3 energy."""
    hand = [sts_sim.Card.OmegaCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.OmegaCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── DevaFormCard: cost 2, power ─────────────────────────────────────

def test_deva_form_power(game):
    """DevaFormCard is a power card that costs 2 energy (gain energy each turn)."""
    hand = [sts_sim.Card.DevaFormCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DevaFormCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── DevotionCard: cost 1, power ─────────────────────────────────────

def test_devotion_power(game):
    """DevotionCard is a power card that costs 1 energy (gain Mantra each turn)."""
    hand = [sts_sim.Card.DevotionCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DevotionCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── EstablishmentCard: cost 1, power ────────────────────────────────

def test_establishment_power(game):
    """EstablishmentCard is a power card that costs 1 energy (reduce retain cost)."""
    hand = [sts_sim.Card.EstablishmentCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EstablishmentCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── ConjureBladeCard: X-cost, power ─────────────────────────────────

def test_conjure_blade_power(game):
    """ConjureBladeCard is an X-cost power."""
    hand = [sts_sim.Card.ConjureBladeCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ConjureBladeCard,
                            choices=[3])

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# STANCE INTERACTION TESTS
# ===================================================================


# ── Eruption in Wrath doubles damage ────────────────────────────────

def test_eruption_in_wrath_from_crescendo(game):
    """Play Crescendo (enter Wrath), then Eruption (should deal doubled damage).

    Wrath stance doubles damage dealt. Verify sim and game agree.
    """
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.Eruption]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    # Play Crescendo to enter Wrath
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)

    # Play Eruption (should deal doubled damage in Wrath)
    state = play_named_card(game, sim, state, sts_sim.Card.Eruption,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Calm exit gives energy, then play attack ────────────────────────

def test_calm_exit_gives_energy(game):
    """Enter Calm via Vigilance, then exit via EmptyFist.

    Exiting Calm grants +2 energy. After Vigilance (cost 2) + EmptyFist (cost 1)
    = 3 spent, +2 from Calm = 2 energy remaining.
    """
    hand = [sts_sim.Card.Vigilance, sts_sim.Card.EmptyFist]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    # Play Vigilance to enter Calm
    state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance)

    # Play EmptyFist to exit Calm (gains +2 energy)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyFist,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Crescendo + Strike: Wrath doubles Strike damage ─────────────────

def test_wrath_doubles_strike_damage(game):
    """Play Crescendo (enter Wrath), then StrikePurple (doubled damage)."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    # Enter Wrath
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)

    # Play Strike (doubled in Wrath)
    state = play_named_card(game, sim, state, sts_sim.Card.StrikePurple,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
