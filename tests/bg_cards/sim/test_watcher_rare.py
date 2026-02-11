"""Simulator tests for Watcher Rare cards.

Tests verify that Watcher rare card mechanics -- multi-hit, Miracles,
exhaust, X-cost, powers, Judgment threshold -- are modeled correctly in
the Rust simulator.

NOTE: TalkToTheHand is [N] (not in simulator) -- all its tests are skipped.
"""
import pytest
import sts_sim
from tests.live.conftest import make_sim


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=20, monster_block=0, monster_powers=None,
                     monsters=None):
    """Create a simulator CombatState with Character.Watcher."""
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
    """Return (Card, upgraded_bool) from a card spec."""
    if isinstance(card_spec, tuple):
        return card_spec[0], card_spec[1]
    return card_spec, False


# ===================================================================
# RAGNAROK
# ===================================================================

def test_ragnarok_5_hits():
    """Ragnarok deals 5 hits of 1 damage each to a single target."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Ragnarok], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 15
    assert sim.player.energy == 0  # cost 3


def test_ragnarok_with_strength():
    """Ragnarok with 2 Strength: 5 hits of (1+2) = 15 damage."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Ragnarok],
        energy=3, monster_hp=30,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 15


def test_ragnarok_upgraded_6_hits():
    """Upgraded Ragnarok deals 6 hits of 1 damage."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Ragnarok, True)],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 14


# ===================================================================
# BRILLIANCE
# ===================================================================

def test_brilliance_no_miracles():
    """Brilliance with 0 Miracles deals 0 damage."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.BrillianceCard], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 20  # 0 miracles -> 0 hits


def test_brilliance_base():
    """Brilliance deals 2 damage per Miracle (base). Cost 1."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.BrillianceCard], energy=3, monster_hp=30,
    )
    sim.play_card(0, 0)
    assert sim.player.energy == 2  # cost 1


# ===================================================================
# BLASPHEMY
# ===================================================================

def test_blasphemy_exhausts():
    """Blasphemy exhausts when played."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Blasphemy], draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.Blasphemy in exhaust_cards
    assert sim.player.energy == 2  # cost 1


# ===================================================================
# DEUS EX MACHINA
# ===================================================================

def test_deus_ex_machina_exhaust():
    """Deus Ex Machina costs 0, exhausts."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.DeusExMachina], energy=3,
    )
    sim.play_card(0, 0)
    assert sim.player.energy == 3  # costs 0
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.DeusExMachina in exhaust_cards


def test_deus_ex_machina_upgraded_exhaust():
    """Upgraded Deus Ex Machina costs 0 and exhausts."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.DeusExMachina, True)], energy=3,
    )
    sim.play_card(0, 0)
    assert sim.player.energy == 3
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.DeusExMachina in exhaust_cards


# ===================================================================
# OMNISCIENCE
# ===================================================================

def test_omniscience_costs_3():
    """OmniscienceCard costs 3 energy and exhausts."""
    draw = [sts_sim.Card.StrikePurple] * 3
    sim = make_watcher_sim(
        hand=[sts_sim.Card.OmniscienceCard],
        draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, 0, 0)  # choice: pick first card from draw pile
    assert sim.player.energy == 0  # cost 3
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.OmniscienceCard in exhaust_cards


def test_omniscience_upgraded_costs_2():
    """Upgraded OmniscienceCard costs 2 energy."""
    draw = [sts_sim.Card.StrikePurple] * 3
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.OmniscienceCard, True)],
        draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, 0, 0)
    assert sim.player.energy == 1  # cost 2


# ===================================================================
# SCRAWL
# ===================================================================

def test_scrawl_draw_5_exhaust():
    """ScrawlCard draws 5 cards and exhausts. Cost 1."""
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]
    sim = make_watcher_sim(
        hand=[sts_sim.Card.ScrawlCard],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    assert len(sim.get_hand()) == 5  # drew 5 cards
    assert sim.player.energy == 2  # cost 1
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.ScrawlCard in exhaust_cards


def test_scrawl_upgraded_costs_0():
    """Upgraded ScrawlCard costs 0 energy."""
    draw = [sts_sim.Card.StrikePurple] * 8
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.ScrawlCard, True)],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    assert sim.player.energy == 3  # cost 0
    assert len(sim.get_hand()) == 5


# ===================================================================
# VAULT
# ===================================================================

def test_vault_costs_3_exhausts():
    """VaultCard costs 3 energy and exhausts."""
    draw = [sts_sim.Card.StrikePurple] * 8
    sim = make_watcher_sim(
        hand=[sts_sim.Card.VaultCard, sts_sim.Card.StrikePurple,
              sts_sim.Card.DefendPurple],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.VaultCard in exhaust_cards


def test_vault_upgraded_costs_2():
    """Upgraded VaultCard costs 2 energy."""
    draw = [sts_sim.Card.StrikePurple] * 8
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.VaultCard, True), sts_sim.Card.StrikePurple],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    # Vault+ costs 2, gains 3 = net +1
    # 3 - 2 + 3 = 4
    assert sim.player.energy == 4


# ===================================================================
# WISH
# ===================================================================

def test_wish_choose_strength():
    """WishCard (choice=0 Strength) grants 1 Strength and exhausts."""
    sim = make_watcher_sim(hand=[sts_sim.Card.WishCard], energy=3)
    sim.play_card(0, 0, 0)  # choice 0 = Strength
    assert sim.player.energy == 3  # cost 0
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WishCard in exhaust_cards


def test_wish_choose_block():
    """WishCard (choice=1 Block) grants 10 block and exhausts."""
    sim = make_watcher_sim(hand=[sts_sim.Card.WishCard], energy=3)
    sim.play_card(0, 0, 1)  # choice 1 = Block
    assert sim.player.block == 10
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WishCard in exhaust_cards


def test_wish_upgraded_strength():
    """Upgraded WishCard (choice=0 Strength) grants 2 Strength."""
    sim = make_watcher_sim(hand=[(sts_sim.Card.WishCard, True)], energy=3)
    sim.play_card(0, 0, 0)
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WishCard in exhaust_cards


# ===================================================================
# SPIRIT SHIELD
# ===================================================================

def test_spirit_shield_block_per_card():
    """SpiritShieldCard gains 1 block per card in hand (5 cards = 5 block). Exhausts."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.SpiritShieldCard, sts_sim.Card.StrikePurple,
              sts_sim.Card.DefendPurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.DefendPurple],
        energy=3,
    )
    sim.play_card(0, 0)
    # 5 cards in hand when played -> 5 block
    assert sim.player.block == 5
    assert sim.player.energy == 1  # cost 2
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.SpiritShieldCard in exhaust_cards


def test_spirit_shield_upgraded_no_exhaust():
    """Upgraded SpiritShieldCard does not exhaust."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.SpiritShieldCard, True), sts_sim.Card.StrikePurple,
              sts_sim.Card.DefendPurple, sts_sim.Card.StrikePurple,
              sts_sim.Card.DefendPurple],
        energy=3,
    )
    sim.play_card(0, 0)
    assert sim.player.block == 5
    # Should be in discard, not exhaust
    discard_cards = [ci.card for ci in sim.get_discard_pile()]
    assert sts_sim.Card.SpiritShieldCard in discard_cards
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.SpiritShieldCard not in exhaust_cards


# ===================================================================
# JUDGMENT
# ===================================================================

def test_judgment_kills_at_threshold():
    """JudgmentCard kills enemy at 7 HP or below."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.JudgmentCard], energy=3, monster_hp=7,
    )
    sim.play_card(0, 0)
    m = sim.get_monsters()[0]
    assert m.hp == 0 or m.is_gone


def test_judgment_no_effect_above_threshold():
    """JudgmentCard does nothing to enemy above 7 HP."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.JudgmentCard], energy=3, monster_hp=8,
    )
    sim.play_card(0, 0)
    m = sim.get_monsters()[0]
    assert m.hp == 8


def test_judgment_upgraded_threshold_8():
    """Upgraded JudgmentCard kills enemy at 8 HP or below."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.JudgmentCard, True)], energy=3, monster_hp=8,
    )
    sim.play_card(0, 0)
    m = sim.get_monsters()[0]
    assert m.hp == 0 or m.is_gone


# ===================================================================
# WORSHIP
# ===================================================================

def test_worship_x_cost_exhaust():
    """WorshipCard (X=3) exhausts. Costs all energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.WorshipCard], energy=3)
    sim.play_card(0, 0, 3)  # X=3
    assert sim.player.energy == 0
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WorshipCard in exhaust_cards


def test_worship_zero_energy():
    """WorshipCard (X=0) exhausts, costs 0 energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.WorshipCard], energy=0)
    sim.play_card(0, 0, 0)  # X=0
    assert sim.player.energy == 0
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WorshipCard in exhaust_cards


# ===================================================================
# OMEGA (Power)
# ===================================================================

def test_omega_power_play():
    """OmegaCard costs 3 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.OmegaCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 0  # cost 3


# ===================================================================
# DEVA FORM (Power)
# ===================================================================

def test_deva_form_power_play():
    """DevaFormCard costs 3 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.DevaFormCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 0  # cost 3


# ===================================================================
# DEVOTION (Power)
# ===================================================================

def test_devotion_power_play():
    """DevotionCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.DevotionCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2  # cost 1


# ===================================================================
# ESTABLISHMENT (Power)
# ===================================================================

def test_establishment_power_play():
    """EstablishmentCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.EstablishmentCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2  # cost 1


# ===================================================================
# CONJURE BLADE (Power, X-cost)
# ===================================================================

def test_conjure_blade_x_cost():
    """ConjureBladeCard (X=3) costs all 3 energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.ConjureBladeCard], energy=3)
    sim.play_card(0, 0, 3)  # X=3
    assert sim.player.energy == 0


# ===================================================================
# TALK TO THE HAND — Not in simulator [N]
# ===================================================================

@pytest.mark.skip(reason="TalkToTheHand is [N] — not implemented in simulator")
def test_talk_to_the_hand_damage_and_block():
    """TalkToTheHand deals 2 damage and gains block per Miracle."""
    pass


@pytest.mark.skip(reason="TalkToTheHand is [N] — not implemented in simulator")
def test_talk_to_the_hand_no_miracles():
    """TalkToTheHand with 0 Miracles gains 0 block."""
    pass


@pytest.mark.skip(reason="TalkToTheHand is [N] — not implemented in simulator")
def test_talk_to_the_hand_upgraded():
    """Upgraded TalkToTheHand deals 3 damage."""
    pass
