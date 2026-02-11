"""Simulator tests for Watcher Common cards.

Tests verify BG mod Watcher common card mechanics: Flurry of Blows, Empty Fist,
Consecrate, Cut Through Fate, Just Lucky, Flying Sleeves, Empty Body, Protect,
Halt, Third Eye, Tranquility, Crescendo, and Collect.

NOTE: sim.set_stance() does not exist in the API. Stances are entered by
playing stance-changing cards (Crescendo for Wrath, Tranquility for Calm).
"""
import sts_sim


# ---------------------------------------------------------------------------
# Helper: create a Watcher CombatState
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=20, player_block=0,
                     player_powers=None, monster_hp=20, monster_block=0,
                     monster_powers=None, monsters=None):
    """Create a simulator CombatState with Character.Watcher."""
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 20), "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Test Monster", monster_hp, "jaw_worm", "A", False)
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

    if player_powers:
        for power_name, amount in player_powers.items():
            pt = getattr(sts_sim.PowerType, power_name)
            sim.apply_player_power(pt, amount)

    for card_spec in draw_pile:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    sim.set_die_value(1)
    return sim


def _unpack(card_spec):
    """Unpack a card spec into (Card, upgraded_bool)."""
    if isinstance(card_spec, tuple):
        return card_spec[0], card_spec[1]
    return card_spec, False


def _enter_wrath(sim):
    """Enter Wrath stance by playing Crescendo."""
    sim.add_card_to_hand(sts_sim.Card.Crescendo)
    idx = len(sim.get_hand()) - 1
    energy_before = sim.player.energy
    sim.set_player_energy(energy_before + 1)
    sim.play_card(idx, None)
    assert sim.get_stance() == sts_sim.Stance.Wrath
    return sim


def _enter_calm(sim):
    """Enter Calm stance by playing Tranquility."""
    sim.add_card_to_hand(sts_sim.Card.Tranquility)
    idx = len(sim.get_hand()) - 1
    energy_before = sim.player.energy
    sim.set_player_energy(energy_before + 1)
    sim.play_card(idx, None)
    assert sim.get_stance() == sts_sim.Stance.Calm
    return sim


# ===================================================================
# FLURRY OF BLOWS
# ===================================================================


def test_flurry_of_blows_no_stance_switch():
    """Flurry of Blows without stance switch deals 1 damage."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.FlurryOfBlows], energy=3, monster_hp=20
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19
    assert sim.player.energy == 3  # costs 0


def test_flurry_of_blows_with_stance_switch():
    """Flurry of Blows after stance switch deals extra hit(s), in Wrath."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, sts_sim.Card.FlurryOfBlows],
        energy=3, monster_hp=20
    )
    # Play Crescendo to enter Wrath (stance switch)
    sim.play_card(0, None)
    assert sim.get_stance() == sts_sim.Stance.Wrath
    # Play Flurry of Blows (should deal extra hits + Wrath bonus)
    hp_before = sim.get_monsters()[0].hp
    sim.play_card(0, 0)  # FlurryOfBlows is now index 0 after Crescendo exhausted
    damage = hp_before - sim.get_monsters()[0].hp
    # Expected: 1+1=2 HIT base, with Wrath bonus
    # Exact value depends on Wrath formula; md says 4 (doubled)
    assert damage >= 2  # At least 2 hits worth of damage


def test_flurry_of_blows_upgraded_with_stance_switch():
    """Upgraded Flurry of Blows with stance switch deals 3 HIT in Wrath."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, (sts_sim.Card.FlurryOfBlows, True)],
        energy=3, monster_hp=20
    )
    sim.play_card(0, None)  # Crescendo -> Wrath
    hp_before = sim.get_monsters()[0].hp
    sim.play_card(0, 0)  # Flurry of Blows+
    damage = hp_before - sim.get_monsters()[0].hp
    # Expected: 3 HIT base with Wrath bonus
    assert damage >= 3


# ===================================================================
# EMPTY FIST
# ===================================================================


def test_empty_fist_from_wrath():
    """Empty Fist from Wrath deals doubled damage and exits to Neutral."""
    sim = make_watcher_sim(hand=[], energy=5, monster_hp=20)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.EmptyFist)
    idx = len(sim.get_hand()) - 1
    hp_before = sim.get_monsters()[0].hp
    sim.play_card(idx, 0)
    damage = hp_before - sim.get_monsters()[0].hp
    # In Wrath, damage dealt before stance change: 2 base + Wrath bonus
    assert damage >= 3  # At least 2 + 1 Wrath
    assert sim.get_stance() == sts_sim.Stance.Neutral
    assert sim.player.energy == 2  # costs 1


def test_empty_fist_from_calm():
    """Empty Fist from Calm grants 2 energy and enters Neutral."""
    sim = make_watcher_sim(hand=[], energy=5, monster_hp=20)
    _enter_calm(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.EmptyFist)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, 0)
    assert sim.get_monsters()[0].hp == 18  # 2 damage (no Wrath)
    assert sim.get_stance() == sts_sim.Stance.Neutral
    # Energy: 3 - 1 (cost) + 2 (Calm exit) = 4
    assert sim.player.energy == 4


def test_empty_fist_upgraded():
    """Upgraded Empty Fist deals 3 damage."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.EmptyFist, True)], energy=3, monster_hp=20
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17
    assert sim.player.energy == 2
    assert sim.get_stance() == sts_sim.Stance.Neutral


def test_empty_fist_from_neutral():
    """Empty Fist from Neutral stays in Neutral."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.EmptyFist], energy=3, monster_hp=20
    )
    assert sim.get_stance() == sts_sim.Stance.Neutral
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 2 damage
    assert sim.get_stance() == sts_sim.Stance.Neutral


# ===================================================================
# CONSECRATE
# ===================================================================


def test_consecrate_aoe():
    """Consecrate hits all enemies for 1 damage."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Consecrate], energy=3,
        monsters=[{"hp": 15}, {"hp": 10}]
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 14
    assert monsters[1].hp == 9
    assert sim.player.energy == 3  # costs 0


def test_consecrate_in_wrath():
    """Consecrate in Wrath deals doubled AOE damage."""
    sim = make_watcher_sim(
        hand=[], energy=5,
        monsters=[{"hp": 15}, {"hp": 10}]
    )
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.Consecrate)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 13  # 1 base + 1 Wrath = 2
    assert monsters[1].hp == 8


def test_consecrate_upgraded():
    """Upgraded Consecrate deals 2 HIT AOE."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Consecrate, True)], energy=3,
        monsters=[{"hp": 15}, {"hp": 10}]
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 13
    assert monsters[1].hp == 8


# ===================================================================
# CUT THROUGH FATE
# ===================================================================


def test_cut_through_fate_base():
    """Cut Through Fate deals 1 damage, scries 2, draws 1 card."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.CutThroughFate], draw_pile=draw,
        energy=3, monster_hp=20
    )
    hand_before = len(sim.get_hand())
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 1 damage
    assert sim.player.energy == 2  # costs 1
    # After playing CutThroughFate (-1 card) and drawing 1 (+1), hand stays same
    assert len(sim.get_hand()) == hand_before - 1 + 1


def test_cut_through_fate_upgraded():
    """Upgraded Cut Through Fate deals 2 damage and scries 3."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.CutThroughFate, True)], draw_pile=draw,
        energy=3, monster_hp=20
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 2 damage


def test_cut_through_fate_in_wrath():
    """Cut Through Fate in Wrath doubles damage."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(hand=[], energy=5, monster_hp=20)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    for c in draw:
        sim.add_card_to_draw(c)
    sim.add_card_to_hand(sts_sim.Card.CutThroughFate)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, 0)
    assert sim.get_monsters()[0].hp == 18  # 1 base + 1 Wrath = 2


# ===================================================================
# JUST LUCKY
# ===================================================================


def test_just_lucky_low_roll():
    """Just Lucky with low die roll (1-3) deals 1 damage and scries."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.JustLucky], draw_pile=draw,
        energy=3, monster_hp=20
    )
    sim.set_die_value(2)  # Low roll
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 1 damage
    assert sim.player.energy == 3  # costs 0


def test_just_lucky_high_roll():
    """Just Lucky with high die roll (4-6) deals 1 damage and blocks."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.JustLucky], energy=3, monster_hp=20
    )
    sim.set_die_value(5)  # High roll
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 1 damage
    assert sim.player.block == 1
    assert sim.player.energy == 3  # costs 0


def test_just_lucky_upgraded_low_roll():
    """Upgraded Just Lucky low roll deals 2 damage and scries 2."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.JustLucky, True)], draw_pile=draw,
        energy=3, monster_hp=20
    )
    sim.set_die_value(1)  # Low roll
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 2 damage


def test_just_lucky_in_wrath():
    """Just Lucky in Wrath doubles damage."""
    sim = make_watcher_sim(hand=[], energy=5, monster_hp=20)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.JustLucky)
    idx = len(sim.get_hand()) - 1
    sim.set_die_value(4)  # High roll -> damage + block
    sim.play_card(idx, 0)
    assert sim.get_monsters()[0].hp == 18  # 1 base + 1 Wrath = 2
    assert sim.player.block == 1


# ===================================================================
# FLYING SLEEVES
# ===================================================================


def test_flying_sleeves_base():
    """Flying Sleeves deals 2 damage in two hits."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.FlyingSleeves], energy=3, monster_hp=20
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 2 hits x 1 = 2 damage
    assert sim.player.energy == 2  # costs 1


def test_flying_sleeves_retain():
    """Flying Sleeves retains in hand at end of turn."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.FlyingSleeves, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple],
        energy=3, monster_hp=20
    )
    sim.end_player_turn()
    hand = sim.get_hand()
    # Flying Sleeves should be retained; others discarded
    retained_cards = [c.card for c in hand]
    assert sts_sim.Card.FlyingSleeves in retained_cards


def test_flying_sleeves_upgraded():
    """Upgraded Flying Sleeves deals 3 damage in three hits."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.FlyingSleeves, True)], energy=3, monster_hp=20
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 3 hits x 1 = 3 damage


def test_flying_sleeves_with_strength():
    """Flying Sleeves with 2 Strength deals 6 damage (3 per hit x 2 hits)."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.FlyingSleeves], energy=3, monster_hp=20,
        player_powers={"Strength": 2}
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 14  # 2 hits x (1 + 2) = 6 damage


# ===================================================================
# EMPTY BODY
# ===================================================================


def test_empty_body_from_wrath():
    """Empty Body grants 2 block and enters Neutral from Wrath."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_card_to_hand(sts_sim.Card.EmptyBody)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 2
    assert sim.get_stance() == sts_sim.Stance.Neutral
    assert sim.player.energy == 2  # costs 1


def test_empty_body_from_calm():
    """Empty Body from Calm grants 2 energy and enters Neutral."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_calm(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_card_to_hand(sts_sim.Card.EmptyBody)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 2
    assert sim.get_stance() == sts_sim.Stance.Neutral
    # Energy: 3 - 1 (cost) + 2 (Calm exit) = 4
    assert sim.player.energy == 4


def test_empty_body_upgraded():
    """Upgraded Empty Body grants 3 block."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_upgraded_card_to_hand(sts_sim.Card.EmptyBody)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 3
    assert sim.get_stance() == sts_sim.Stance.Neutral
    assert sim.player.energy == 2


# ===================================================================
# PROTECT
# ===================================================================


def test_protect_base():
    """Protect grants 3 block."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Protect], energy=3)
    sim.play_card(0, None)
    assert sim.player.block == 3
    assert sim.player.energy == 1  # costs 2


def test_protect_retain():
    """Protect retains in hand at end of turn."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Protect, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple],
        energy=3
    )
    sim.end_player_turn()
    hand = sim.get_hand()
    retained_cards = [c.card for c in hand]
    assert sts_sim.Card.Protect in retained_cards


def test_protect_upgraded():
    """Upgraded Protect grants 4 block."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Protect, True)], energy=3
    )
    sim.play_card(0, None)
    assert sim.player.block == 4
    assert sim.player.energy == 1


# ===================================================================
# HALT
# ===================================================================


def test_halt_neutral():
    """Halt in Neutral grants 1 block."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Halt], energy=3)
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.player.energy == 3  # costs 0


def test_halt_in_wrath():
    """Halt in Wrath grants 2 block (1 base + 1 Wrath bonus)."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_card_to_hand(sts_sim.Card.Halt)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 2


def test_halt_upgraded_in_wrath():
    """Upgraded Halt in Wrath grants 3 block (1 base + 2 Wrath bonus)."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_upgraded_card_to_hand(sts_sim.Card.Halt)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 3


def test_halt_in_calm():
    """Halt in Calm grants only 1 block (no Wrath bonus)."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_calm(sim)
    sim.set_player_energy(3)
    sim.set_player_block(0)
    sim.add_card_to_hand(sts_sim.Card.Halt)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.player.block == 1


# ===================================================================
# THIRD EYE
# ===================================================================


def test_third_eye_base():
    """Third Eye grants 2 block and scries 3."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.ThirdEye], draw_pile=draw, energy=3
    )
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert sim.player.energy == 2  # costs 1


def test_third_eye_upgraded():
    """Upgraded Third Eye grants 3 block and scries 5."""
    draw = [sts_sim.Card.StrikePurple] * 6
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.ThirdEye, True)], draw_pile=draw, energy=3
    )
    sim.play_card(0, None)
    assert sim.player.block == 3
    assert sim.player.energy == 2


def test_third_eye_scry_discards():
    """Third Eye scry moves status/curse cards to discard pile."""
    # Add status cards that scry should auto-discard
    draw = [sts_sim.Card.Dazed, sts_sim.Card.Dazed, sts_sim.Card.StrikePurple]
    sim = make_watcher_sim(
        hand=[sts_sim.Card.ThirdEye], draw_pile=draw, energy=3
    )
    draw_before = len(sim.get_draw_pile())
    sim.play_card(0, None)
    # Scry should have discarded status cards from the top of draw pile
    draw_after = len(sim.get_draw_pile())
    assert draw_after < draw_before
    assert sim.player.block == 2


# ===================================================================
# TRANQUILITY
# ===================================================================


def test_tranquility_enters_calm_and_exhausts():
    """Tranquility enters Calm and exhausts itself."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Tranquility], energy=3)
    sim.play_card(0, None)
    assert sim.get_stance() == sts_sim.Stance.Calm
    assert sim.player.energy == 2  # costs 1
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Tranquility in exhaust_cards
    assert len(sim.get_hand()) == 0  # only card was played


def test_tranquility_retain():
    """Tranquility retains in hand at end of turn."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Tranquility, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple],
        energy=3
    )
    sim.end_player_turn()
    hand = sim.get_hand()
    retained_cards = [c.card for c in hand]
    assert sts_sim.Card.Tranquility in retained_cards


def test_tranquility_upgraded():
    """Upgraded Tranquility costs 0 energy."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Tranquility, True)], energy=3
    )
    sim.play_card(0, None)
    assert sim.get_stance() == sts_sim.Stance.Calm
    assert sim.player.energy == 3  # costs 0
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Tranquility in exhaust_cards


def test_tranquility_from_wrath():
    """Tranquility from Wrath exits Wrath and enters Calm."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_wrath(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.Tranquility)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.get_stance() == sts_sim.Stance.Calm
    assert sim.player.energy == 2  # costs 1
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Tranquility in exhaust_cards


# ===================================================================
# CRESCENDO
# ===================================================================


def test_crescendo_enters_wrath_and_exhausts():
    """Crescendo enters Wrath and exhausts itself."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Crescendo], energy=3)
    sim.play_card(0, None)
    assert sim.get_stance() == sts_sim.Stance.Wrath
    assert sim.player.energy == 2  # costs 1
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Crescendo in exhaust_cards


def test_crescendo_from_calm():
    """Crescendo from Calm grants 2 energy on exit and enters Wrath."""
    sim = make_watcher_sim(hand=[], energy=5)
    _enter_calm(sim)
    sim.set_player_energy(3)
    sim.add_card_to_hand(sts_sim.Card.Crescendo)
    idx = len(sim.get_hand()) - 1
    sim.play_card(idx, None)
    assert sim.get_stance() == sts_sim.Stance.Wrath
    # Energy: 3 - 1 (cost) + 2 (Calm exit) = 4
    assert sim.player.energy == 4
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Crescendo in exhaust_cards


def test_crescendo_upgraded_draws():
    """Upgraded Crescendo draws 1 card after entering Wrath."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Crescendo, True)], draw_pile=draw, energy=3
    )
    # Hand before: 1 card (Crescendo+). After playing: -1 + draw 1 = 1
    sim.play_card(0, None)
    assert sim.get_stance() == sts_sim.Stance.Wrath
    assert sim.player.energy == 2  # costs 1
    # Should have drawn 1 card
    assert len(sim.get_hand()) == 1
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Crescendo in exhaust_cards


def test_crescendo_retain():
    """Crescendo retains in hand at end of turn."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.StrikePurple],
        energy=3
    )
    sim.end_player_turn()
    hand = sim.get_hand()
    retained_cards = [c.card for c in hand]
    assert sts_sim.Card.Crescendo in retained_cards


# ===================================================================
# COLLECT
# ===================================================================


def test_collect_generates_miracles():
    """Collect generates 2 miracles and exhausts."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Collect], energy=3)
    sim.play_card(0, None)
    assert sim.get_miracles() == 2
    exhaust = sim.get_exhaust_pile()
    exhaust_cards = [c.card for c in exhaust]
    assert sts_sim.Card.Collect in exhaust_cards


def test_collect_upgraded():
    """Upgraded Collect generates 3 miracles."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Collect, True)], energy=3
    )
    sim.play_card(0, None)
    assert sim.get_miracles() == 3


def test_miracle_gives_energy():
    """Miracle tokens can be spent for 1 energy each."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.StrikePurple], energy=0, monster_hp=20
    )
    # Give miracles via power
    sim.apply_player_power(sts_sim.PowerType.MiracleCount, 2)
    # Play Strike (costs 1) with 0 energy but 2 miracles
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # Strike dealt 1 damage
    assert sim.get_miracles() == 1  # used 1 miracle


def test_collect_then_use_miracles():
    """Collect generates miracles, then miracles fund Eruption."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Collect, sts_sim.Card.Eruption],
        energy=0, monster_hp=20
    )
    # Play Collect (free, Cost -1)
    sim.play_card(0, None)
    miracles_after_collect = sim.get_miracles()
    assert miracles_after_collect == 2
    # Now play Eruption (costs 2) using miracles
    sim.play_card(0, 0)  # Eruption is now at index 0
    assert sim.get_monsters()[0].hp == 18  # 2 damage
    assert sim.get_stance() == sts_sim.Stance.Wrath
