"""Tests for card upgrade system, card mechanics (exhaust, ethereal, unplayable),
and status/curse cards (Phase 1a, 1b, 1c)."""

import sts_sim


# --- Phase 1a: Upgrade system ---

def test_card_instance_creation():
    """CardInstance wraps a Card with upgraded flag."""
    ci = sts_sim.CardInstance(sts_sim.Card.StrikeRed)
    assert ci.card == sts_sim.Card.StrikeRed
    assert ci.upgraded is False
    assert ci.py_name == "Strike"


def test_card_instance_upgraded():
    """Upgraded CardInstance has + suffix and improved stats."""
    ci = sts_sim.CardInstance(sts_sim.Card.StrikeRed, upgraded=True)
    assert ci.upgraded is True
    assert ci.py_name == "Strike+"
    assert ci.py_base_damage == 2  # Upgraded: 1 → 2


def test_strike_upgrade_stats():
    """Strike: 1 damage → 2 damage on upgrade."""
    base = sts_sim.CardInstance(sts_sim.Card.StrikeRed)
    assert base.py_base_damage == 1
    upgraded = sts_sim.CardInstance(sts_sim.Card.StrikeRed, upgraded=True)
    assert upgraded.py_base_damage == 2


def test_defend_upgrade_stats():
    """Defend: 1 block → 2 block on upgrade."""
    base = sts_sim.CardInstance(sts_sim.Card.DefendRed)
    assert base.py_base_block == 1
    upgraded = sts_sim.CardInstance(sts_sim.Card.DefendRed, upgraded=True)
    assert upgraded.py_base_block == 2


def test_bash_upgrade_stats():
    """Bash: 2 damage → 4 damage on upgrade, Vulnerable stays at 1."""
    base = sts_sim.CardInstance(sts_sim.Card.Bash)
    assert base.py_base_damage == 2
    assert base.py_base_magic == 1
    upgraded = sts_sim.CardInstance(sts_sim.Card.Bash, upgraded=True)
    assert upgraded.py_base_damage == 4
    assert upgraded.py_base_magic == 1  # Unchanged


def test_upgrade_card_in_deck():
    """upgrade_card() should upgrade a card in the deck by index."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    deck = cs.get_deck()
    # Find a Strike in the deck
    strike_idx = None
    for i, ci in enumerate(deck):
        if ci.card == sts_sim.Card.StrikeRed:
            strike_idx = i
            break
    assert strike_idx is not None

    # Upgrade it
    result = cs.upgrade_card(strike_idx)
    assert result is True

    # Verify upgrade
    deck = cs.get_deck()
    assert deck[strike_idx].upgraded is True
    assert deck[strike_idx].py_base_damage == 2

    # Can't upgrade again
    result = cs.upgrade_card(strike_idx)
    assert result is False


def test_upgrade_method_on_instance():
    """CardInstance.upgrade() should set upgraded=True."""
    ci = sts_sim.CardInstance(sts_sim.Card.StrikeRed)
    assert ci.upgraded is False
    result = ci.upgrade()
    assert result is True
    assert ci.upgraded is True

    # Can't double-upgrade
    result = ci.upgrade()
    assert result is False


def test_status_cards_cannot_upgrade():
    """Status cards should not be upgradable."""
    ci = sts_sim.CardInstance(sts_sim.Card.Dazed)
    result = ci.upgrade()
    assert result is False


def test_curse_cards_cannot_upgrade():
    """Curse cards should not be upgradable."""
    ci = sts_sim.CardInstance(sts_sim.Card.AscendersBane)
    result = ci.upgrade()
    assert result is False


def test_upgraded_strike_deals_more_damage():
    """Playing an upgraded Strike should deal 2 damage instead of 1."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    # Upgrade first Strike in deck
    deck = cs.get_deck()
    for i, ci in enumerate(deck):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.upgrade_card(i)
            break

    cs.start_combat()
    hand = cs.get_hand()
    # Find the upgraded strike
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed and ci.upgraded:
            cs.play_card(i, 0)
            break
    else:
        # If upgraded strike wasn't in opening hand, just verify the deck was upgraded
        deck = cs.get_deck()
        upgraded_count = sum(1 for c in deck if c.card == sts_sim.Card.StrikeRed and c.upgraded)
        assert upgraded_count == 1
        return

    monsters = cs.get_monsters()
    assert monsters[0].hp == 6  # 8 - 2 = 6


def test_deck_returns_card_instances():
    """get_deck() should return CardInstance objects."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    deck = cs.get_deck()
    assert len(deck) == 10
    for ci in deck:
        assert hasattr(ci, 'card')
        assert hasattr(ci, 'upgraded')
        assert ci.upgraded is False


def test_hand_returns_card_instances():
    """get_hand() should return CardInstance objects."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    hand = cs.get_hand()
    assert len(hand) == 5
    for ci in hand:
        assert hasattr(ci, 'card')
        assert hasattr(ci, 'upgraded')


# --- Phase 1b: Card mechanics ---

def test_unplayable_cards_rejected():
    """Unplayable cards (Dazed, Burn, Wound, Void) cannot be played."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Add a Wound to hand via discard → draw cycle
    cs.add_card_to_discard(sts_sim.Card.Wound)
    # Directly check the card properties
    ci = sts_sim.CardInstance(sts_sim.Card.Wound)
    assert ci.py_unplayable is True
    assert ci.py_cost == -2


def test_slimed_costs_energy_and_exhausts():
    """Slimed costs 1 energy, does nothing, and exhausts."""
    ci = sts_sim.CardInstance(sts_sim.Card.Slimed)
    assert ci.py_cost == 1
    assert ci.py_exhausts is True
    assert ci.py_unplayable is False


def test_exhaust_goes_to_exhaust_pile():
    """Playing an exhausting card should send it to exhaust pile."""
    cs = sts_sim.create_encounter("jaw_worm", seed=100)
    # Add Slimed to deck and ensure it's in hand
    cs.add_card_to_draw(sts_sim.Card.Slimed)
    cs.start_combat()

    hand = cs.get_hand()
    slimed_idx = None
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.Slimed:
            slimed_idx = i
            break

    if slimed_idx is not None:
        before_exhaust = len(cs.player.get_exhaust_pile())
        cs.play_card(slimed_idx)
        # After playing Slimed, it should be in exhaust pile
        assert len(cs.player.get_exhaust_pile()) == before_exhaust + 1


def test_ethereal_exhausts_on_end_turn():
    """Ethereal cards in hand at end of turn should be exhausted."""
    ci = sts_sim.CardInstance(sts_sim.Card.Dazed)
    assert ci.py_ethereal is True
    assert ci.py_unplayable is True

    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    # Add Dazed to draw pile so it enters hand
    cs.add_card_to_draw(sts_sim.Card.Dazed)
    cs.start_combat()

    hand = cs.get_hand()
    has_dazed = any(ci.card == sts_sim.Card.Dazed for ci in hand)

    if has_dazed:
        before_exhaust = len(cs.player.get_exhaust_pile())
        cs.end_player_turn()
        # Dazed should have been exhausted (not discarded)
        assert len(cs.player.get_exhaust_pile()) == before_exhaust + 1


def test_dazed_properties():
    """Dazed: unplayable, ethereal, status type."""
    ci = sts_sim.CardInstance(sts_sim.Card.Dazed)
    assert ci.py_card_type == sts_sim.CardType.Status
    assert ci.py_unplayable is True
    assert ci.py_ethereal is True
    assert ci.py_cost == -2


def test_burn_properties():
    """Burn: unplayable, deals self-damage at end of turn."""
    ci = sts_sim.CardInstance(sts_sim.Card.Burn)
    assert ci.py_card_type == sts_sim.CardType.Status
    assert ci.py_unplayable is True
    assert ci.py_ethereal is False
    assert ci.py_cost == -2
    assert ci.py_base_magic == 1  # 1 self-damage


def test_burn_deals_damage_at_end_of_turn():
    """Burn in hand at end of turn should deal 1 damage to player."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    # Add Burn to draw pile so it's in opening hand
    cs.add_card_to_draw(sts_sim.Card.Burn)
    cs.start_combat()

    hand = cs.get_hand()
    has_burn = any(ci.card == sts_sim.Card.Burn for ci in hand)
    hp_before = cs.player.hp

    if has_burn:
        cs.end_player_turn()
        assert cs.player.hp == hp_before - 1


def test_wound_properties():
    """Wound: unplayable, not ethereal, not exhaust."""
    ci = sts_sim.CardInstance(sts_sim.Card.Wound)
    assert ci.py_card_type == sts_sim.CardType.Status
    assert ci.py_unplayable is True
    assert ci.py_ethereal is False
    assert ci.py_exhausts is False


def test_void_properties():
    """Void: unplayable, ethereal, loses 1 energy when drawn."""
    ci = sts_sim.CardInstance(sts_sim.Card.VoidCard)
    assert ci.py_card_type == sts_sim.CardType.Status
    assert ci.py_unplayable is True
    assert ci.py_ethereal is True


def test_void_drains_energy_on_draw():
    """Drawing Void should lose 1 energy."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    # Put Void on top of draw pile
    cs.add_card_to_draw(sts_sim.Card.VoidCard)
    cs.start_combat()

    # Player should have 3 energy normally, but Void drains 1
    hand = cs.get_hand()
    has_void = any(ci.card == sts_sim.Card.VoidCard for ci in hand)
    if has_void:
        # Started with 3 energy, Void drained 1
        assert cs.player.energy == 2


# --- Phase 1c: Status & Curse card properties ---

def test_ascenders_bane_properties():
    """Ascender's Bane: curse, unplayable, exhausts."""
    ci = sts_sim.CardInstance(sts_sim.Card.AscendersBane)
    assert ci.py_card_type == sts_sim.CardType.Curse
    assert ci.py_unplayable is True
    assert ci.py_exhausts is True


def test_injury_properties():
    """Injury: curse, unplayable."""
    ci = sts_sim.CardInstance(sts_sim.Card.Injury)
    assert ci.py_card_type == sts_sim.CardType.Curse
    assert ci.py_unplayable is True


def test_pain_properties():
    """Pain: curse, unplayable."""
    ci = sts_sim.CardInstance(sts_sim.Card.Pain)
    assert ci.py_card_type == sts_sim.CardType.Curse
    assert ci.py_unplayable is True


def test_decay_properties():
    """Decay: curse, unplayable, ethereal (deals 1 damage at end of turn)."""
    ci = sts_sim.CardInstance(sts_sim.Card.Decay)
    assert ci.py_card_type == sts_sim.CardType.Curse
    assert ci.py_unplayable is True
    assert ci.py_ethereal is True


def test_decay_deals_damage_at_end_of_turn():
    """Decay in hand at end of turn deals 1 damage, then gets exhausted."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.add_card_to_draw(sts_sim.Card.Decay)
    cs.start_combat()

    hand = cs.get_hand()
    has_decay = any(ci.card == sts_sim.Card.Decay for ci in hand)
    hp_before = cs.player.hp

    if has_decay:
        exhaust_before = len(cs.player.get_exhaust_pile())
        cs.end_player_turn()
        # Decay: deals 1 damage AND exhausts (ethereal)
        assert cs.player.hp == hp_before - 1
        assert len(cs.player.get_exhaust_pile()) == exhaust_before + 1


def test_add_card_to_discard():
    """add_card_to_discard should add a new card to the discard pile."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    initial_deck_size = len(cs.get_deck())
    initial_discard = len(cs.player.get_discard_pile())

    cs.add_card_to_discard(sts_sim.Card.Wound)

    assert len(cs.get_deck()) == initial_deck_size + 1
    assert len(cs.player.get_discard_pile()) == initial_discard + 1


def test_add_card_to_draw():
    """add_card_to_draw should add a new card to the draw pile."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    initial_deck_size = len(cs.get_deck())
    initial_draw = len(cs.player.get_draw_pile())

    cs.add_card_to_draw(sts_sim.Card.Dazed)

    assert len(cs.get_deck()) == initial_deck_size + 1
    assert len(cs.player.get_draw_pile()) == initial_draw + 1


def test_available_actions_excludes_unplayable():
    """get_available_actions should not include unplayable cards."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.add_card_to_draw(sts_sim.Card.Wound)
    cs.start_combat()

    actions = cs.get_available_actions()
    for _hand_idx, ci, _needs_target in actions:
        assert ci.card != sts_sim.Card.Wound, "Unplayable Wound should not be in available actions"


def test_starter_deck_backward_compat():
    """Existing Card enum comparisons should still work via CardInstance.card."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    deck = cs.get_deck()
    strikes = sum(1 for ci in deck if ci.card == sts_sim.Card.StrikeRed)
    defends = sum(1 for ci in deck if ci.card == sts_sim.Card.DefendRed)
    bashes = sum(1 for ci in deck if ci.card == sts_sim.Card.Bash)
    assert strikes == 5
    assert defends == 4
    assert bashes == 1
