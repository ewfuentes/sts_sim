"""Simulator tests for Ironclad Rare cards."""
import sts_sim
from tests.live.conftest import make_sim


# ── Bludgeon ─────────────────────────────────────────────────────────────

def test_bludgeon_base():
    """Bludgeon deals 7 damage."""
    sim = make_sim(hand=[sts_sim.Card.Bludgeon], energy=3, monster_hp=15)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 8
    assert sim.player.energy == 0


def test_bludgeon_upgraded():
    """Upgraded Bludgeon deals 10 damage."""
    sim = make_sim(hand=[(sts_sim.Card.Bludgeon, True)], energy=3, monster_hp=15)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 5
    assert sim.player.energy == 0


def test_bludgeon_with_strength():
    """Bludgeon with 2 STR deals 9 damage (7 base + 2 STR)."""
    sim = make_sim(
        hand=[sts_sim.Card.Bludgeon], energy=3, monster_hp=30,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 21  # 30 - 9


# ── Impervious ───────────────────────────────────────────────────────────

def test_impervious_base():
    """Impervious grants 6 block and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Impervious], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 6
    assert len(sim.get_exhaust_pile()) == 1
    assert sim.player.energy == 1


def test_impervious_upgraded():
    """Upgraded Impervious grants 8 block."""
    sim = make_sim(hand=[(sts_sim.Card.Impervious, True)], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 8
    assert len(sim.get_exhaust_pile()) == 1


def test_impervious_stacks():
    """Impervious block stacks with existing block."""
    sim = make_sim(hand=[sts_sim.Card.Impervious], energy=3, player_block=4, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 10
    assert len(sim.get_exhaust_pile()) == 1


# ── Offering ─────────────────────────────────────────────────────────────

def test_offering_base():
    """Offering costs HP, gains energy, draws 3 cards, and exhausts."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.Offering], draw_pile=draw,
        energy=0, player_hp=9, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.hp == 8  # lost 1 HP
    assert sim.player.energy == 2  # gained 2 energy, cost 0
    assert len(sim.get_hand()) == 3  # drew 3 cards
    assert len(sim.get_exhaust_pile()) == 1


def test_offering_upgraded():
    """Upgraded Offering draws 5 cards."""
    draw = [sts_sim.Card.StrikeRed] * 6
    sim = make_sim(
        hand=[(sts_sim.Card.Offering, True)], draw_pile=draw,
        energy=0, player_hp=9, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.hp == 8
    assert sim.player.energy == 2
    assert len(sim.get_hand()) == 5
    assert len(sim.get_exhaust_pile()) == 1


def test_offering_at_1hp():
    """Offering at 1 HP still playable."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.Offering], draw_pile=draw,
        energy=0, player_hp=1, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.hp == 0
    assert len(sim.get_exhaust_pile()) == 1


# ── Barricade ────────────────────────────────────────────────────────────

def test_barricade_base_cost():
    """Barricade costs 2 energy to play."""
    sim = make_sim(hand=[sts_sim.Card.Barricade], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 1


def test_barricade_upgraded_cost():
    """Upgraded Barricade costs 1 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Barricade, True)], energy=1, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


# ── Berserk ──────────────────────────────────────────────────────────────

def test_berserk_base_cost():
    """Berserk costs 1 energy to play."""
    sim = make_sim(hand=[sts_sim.Card.BerserkCard], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 2


# ── Corruption ───────────────────────────────────────────────────────────

def test_corruption_base_cost():
    """Corruption costs 3 energy to play."""
    sim = make_sim(hand=[sts_sim.Card.Corruption], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


def test_corruption_upgraded_cost():
    """Upgraded Corruption costs 2 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Corruption, True)], energy=2, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


def test_corruption_makes_skills_free_and_exhaust():
    """Corruption makes Skills cost 0 and exhaust them."""
    sim = make_sim(
        hand=[sts_sim.Card.Corruption, sts_sim.Card.ShrugItOff],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)  # Play Corruption (cost 3)
    sim.play_card(0, None)  # Play Shrug It Off (should cost 0, should exhaust)
    assert sim.player.block == 2  # Shrug It Off grants 2 block
    assert len(sim.get_exhaust_pile()) == 1  # Shrug It Off exhausted


# ── Demon Form ───────────────────────────────────────────────────────────

def test_demon_form_base_cost():
    """Demon Form costs 3 energy to play."""
    sim = make_sim(hand=[sts_sim.Card.DemonForm], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


def test_demon_form_upgraded_cost():
    """Upgraded Demon Form costs 2 energy."""
    sim = make_sim(hand=[(sts_sim.Card.DemonForm, True)], energy=2, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


def test_demon_form_grants_str():
    """Demon Form grants STR at start of next turn."""
    sim = make_sim(hand=[sts_sim.Card.DemonForm], energy=3, monster_hp=20)
    sim.play_card(0, None)
    sim.end_player_turn()
    assert sim.get_player_power(sts_sim.PowerType.Strength) >= 1


# ── Double Tap ───────────────────────────────────────────────────────────

def test_double_tap_base():
    """Double Tap causes next Attack to play twice."""
    sim = make_sim(
        hand=[sts_sim.Card.DoubleTap, sts_sim.Card.StrikeRed],
        energy=3, monster_hp=10,
    )
    sim.play_card(0, None)  # Play Double Tap
    sim.play_card(0, 0)  # Play Strike
    assert sim.get_monsters()[0].hp == 8  # 10 - 2 (1 HIT x 2 plays)
    assert sim.player.energy == 1  # 3 - 1 (DT) - 1 (Strike)


def test_double_tap_only_next_attack():
    """Double Tap only affects the next Attack, not subsequent ones."""
    sim = make_sim(
        hand=[sts_sim.Card.DoubleTap, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed],
        energy=3, monster_hp=10,
    )
    sim.play_card(0, None)  # Double Tap
    sim.play_card(0, 0)  # First Strike (doubled)
    sim.play_card(0, 0)  # Second Strike (normal)
    assert sim.get_monsters()[0].hp == 7  # 10 - 2 - 1


def test_double_tap_upgraded():
    """Upgraded Double Tap costs 0 energy."""
    sim = make_sim(
        hand=[(sts_sim.Card.DoubleTap, True), sts_sim.Card.StrikeRed],
        energy=2, monster_hp=10,
    )
    sim.play_card(0, None)  # Double Tap+ (0 energy)
    sim.play_card(0, 0)  # Strike (doubled)
    assert sim.get_monsters()[0].hp == 8  # 10 - 2
    assert sim.player.energy == 1  # 2 - 0 - 1


# ── Exhume ───────────────────────────────────────────────────────────────

def test_exhume_base():
    """Exhume retrieves a card from exhaust pile."""
    sim = make_sim(hand=[sts_sim.Card.Exhume], energy=3, monster_hp=20)
    sim.add_card_to_exhaust(sts_sim.Card.Impervious)
    sim.play_card(0, None, 0)  # choose Impervious from exhaust
    hand = sim.get_hand()
    assert any(c.card == sts_sim.Card.Impervious for c in hand)
    # Exhume itself should be exhausted
    exhaust = sim.get_exhaust_pile()
    assert any(c.card == sts_sim.Card.Exhume for c in exhaust)


def test_exhume_empty_exhaust():
    """Exhume with empty exhaust pile just exhausts itself."""
    sim = make_sim(hand=[sts_sim.Card.Exhume], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert len(sim.get_exhaust_pile()) == 1
    assert len(sim.get_hand()) == 0


def test_exhume_upgraded():
    """Upgraded Exhume costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Exhume, True)], energy=0, monster_hp=20)
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.play_card(0, None, 0)
    assert sim.player.energy == 0
    hand = sim.get_hand()
    assert any(c.card == sts_sim.Card.StrikeRed for c in hand)


# ── Feed ─────────────────────────────────────────────────────────────────

def test_feed_kill_grants_str():
    """Feed deals 3 damage, gains 1 STR on kill, and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Feed], energy=3, monster_hp=3)
    sim.play_card(0, 0)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert len(sim.get_exhaust_pile()) == 1


def test_feed_no_kill():
    """Feed does not grant STR if enemy survives."""
    sim = make_sim(hand=[sts_sim.Card.Feed], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_feed_upgraded_kill():
    """Upgraded Feed grants 2 STR on kill."""
    sim = make_sim(hand=[(sts_sim.Card.Feed, True)], energy=3, monster_hp=3)
    sim.play_card(0, 0)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 2
    assert len(sim.get_exhaust_pile()) == 1


# ── Fiend Fire ───────────────────────────────────────────────────────────

def test_fiend_fire_base():
    """Fiend Fire exhausts hand and deals 1 HIT per card exhausted."""
    sim = make_sim(
        hand=[
            sts_sim.Card.FiendFire,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.Bash,
        ],
        energy=3, monster_hp=10,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7  # 3 cards exhausted = 3 HIT = 3 damage
    assert len(sim.get_hand()) == 0
    # All 3 other cards + Fiend Fire itself exhausted = 4
    assert len(sim.get_exhaust_pile()) == 4


def test_fiend_fire_empty_hand():
    """Fiend Fire with no other cards deals 0 damage."""
    sim = make_sim(hand=[sts_sim.Card.FiendFire], energy=2, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 10
    assert len(sim.get_exhaust_pile()) == 1  # Fiend Fire itself


def test_fiend_fire_upgraded():
    """Upgraded Fiend Fire deals 2 HIT per card exhausted."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.FiendFire, True),
            sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed,
        ],
        energy=3, monster_hp=15,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 11  # 2 cards x 2 HIT = 4 damage


def test_fiend_fire_with_strength():
    """Fiend Fire with Strength scales per HIT."""
    sim = make_sim(
        hand=[
            sts_sim.Card.FiendFire,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.Bash,
        ],
        energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    # 3 cards exhausted = 3 HIT, each (1+2 STR) = 3 damage, total 9
    assert sim.get_monsters()[0].hp == 11


# ── Immolate ─────────────────────────────────────────────────────────────

def test_immolate_base():
    """Immolate deals 5 AOE damage and adds 2 DAZED."""
    sim = make_sim(
        hand=[sts_sim.Card.Immolate], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.hp == 5
    discard = sim.get_discard_pile()
    dazed_count = sum(1 for c in discard if c.card == sts_sim.Card.Dazed)
    assert dazed_count == 2


def test_immolate_upgraded():
    """Upgraded Immolate deals 7 AOE damage."""
    sim = make_sim(
        hand=[(sts_sim.Card.Immolate, True)], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.hp == 3
    discard = sim.get_discard_pile()
    dazed_count = sum(1 for c in discard if c.card == sts_sim.Card.Dazed)
    assert dazed_count == 2


def test_immolate_with_strength():
    """Immolate with 1 STR deals 6 damage (5 base + 1 STR)."""
    sim = make_sim(
        hand=[sts_sim.Card.Immolate], energy=3, monster_hp=15,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, None)
    assert sim.get_monsters()[0].hp == 9  # 15 - 6


# ── Juggernaut ───────────────────────────────────────────────────────────

def test_juggernaut_on_block_gain():
    """Juggernaut deals 1 damage when gaining block."""
    sim = make_sim(
        hand=[sts_sim.Card.DefendRed], energy=3, monster_hp=10,
        player_powers={"Juggernaut": 1},
    )
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert sim.get_monsters()[0].hp == 9  # 1 Juggernaut damage


def test_juggernaut_multiple_triggers():
    """Juggernaut triggers on each source of block gain."""
    sim = make_sim(
        hand=[sts_sim.Card.DefendRed, sts_sim.Card.DefendRed],
        energy=3, monster_hp=10,
        player_powers={"Juggernaut": 1},
    )
    sim.play_card(0, None)
    sim.play_card(0, None)
    assert sim.get_monsters()[0].hp == 8  # 2 triggers x 1 damage


def test_juggernaut_upgraded():
    """Upgraded Juggernaut deals 2 damage per block gain."""
    sim = make_sim(
        hand=[sts_sim.Card.DefendRed], energy=3, monster_hp=10,
        player_powers={"Juggernaut": 2},
    )
    sim.play_card(0, None)
    assert sim.get_monsters()[0].hp == 8  # 2 Juggernaut damage


# ── Limit Break ──────────────────────────────────────────────────────────

def test_limit_break_base():
    """Limit Break doubles STR and exhausts."""
    sim = make_sim(
        hand=[sts_sim.Card.LimitBreak], energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 4
    assert len(sim.get_exhaust_pile()) == 1


def test_limit_break_cap():
    """Limit Break respects 8 STR cap."""
    sim = make_sim(
        hand=[sts_sim.Card.LimitBreak], energy=3, monster_hp=20,
        player_powers={"Strength": 5},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 8


def test_limit_break_zero_str():
    """Limit Break with 0 STR does nothing."""
    sim = make_sim(hand=[sts_sim.Card.LimitBreak], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_limit_break_upgraded():
    """Upgraded Limit Break does not exhaust."""
    sim = make_sim(
        hand=[(sts_sim.Card.LimitBreak, True)], energy=3, monster_hp=20,
        player_powers={"Strength": 3},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 6
    assert len(sim.get_exhaust_pile()) == 0
    assert len(sim.get_discard_pile()) == 1
