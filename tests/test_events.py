"""Tests for Act 1 event system."""
import pytest
import sts_sim


# ============================================================
# Event creation
# ============================================================

@pytest.mark.parametrize("name,etype", [
    ("big_fish", sts_sim.EventType.BigFish),
    ("golden_idol", sts_sim.EventType.GoldenIdol),
    ("golden_wing", sts_sim.EventType.GoldenWing),
    ("world_of_goop", sts_sim.EventType.WorldOfGoop),
    ("cleric", sts_sim.EventType.Cleric),
    ("living_wall", sts_sim.EventType.LivingWall),
    ("scrap_ooze", sts_sim.EventType.ScrapOoze),
    ("dead_adventurer", sts_sim.EventType.DeadAdventurer),
    ("knowing_skull", sts_sim.EventType.KnowingSkull),
])
def test_create_event(name, etype):
    event = sts_sim.create_event(name)
    assert event.event_type == etype
    assert event.stage == 0
    assert not event.done


def test_create_unknown_event():
    with pytest.raises(ValueError):
        sts_sim.create_event("nonexistent")


# ============================================================
# Big Fish
# ============================================================

def test_big_fish_choices():
    event = sts_sim.create_event("big_fish")
    # Build a deck with Strikes
    deck = [sts_sim.CardInstance(sts_sim.Card.StrikeRed)] * 3
    choices = event.get_choices(deck=deck)
    assert len(choices) == 4
    assert choices[0].label == "Banana"
    assert choices[1].label == "Donut"
    assert choices[2].label == "Box"
    assert choices[3].label == "Remove Strike"
    assert all(c.enabled for c in choices)


def test_big_fish_banana_heals():
    event = sts_sim.create_event("big_fish")
    outcome = event.choose(0)
    assert outcome.hp_change == 2
    assert outcome.done
    assert event.done


def test_big_fish_donut_upgrades():
    event = sts_sim.create_event("big_fish")
    outcome = event.choose(1)
    assert outcome.needs_card_select
    assert outcome.card_select_action == "upgrade"
    assert outcome.done


def test_big_fish_box_gives_curse_and_relic():
    event = sts_sim.create_event("big_fish")
    outcome = event.choose(2)
    assert len(outcome.cards_added) == 1
    assert outcome.cards_added[0].card == sts_sim.Card.Injury
    assert outcome.relic_added is not None
    assert outcome.done


def test_big_fish_remove_strike():
    event = sts_sim.create_event("big_fish")
    outcome = event.choose(3)
    assert outcome.needs_card_select
    assert outcome.card_select_action == "remove"
    assert outcome.done


# ============================================================
# Golden Idol
# ============================================================

def test_golden_idol_two_stages():
    event = sts_sim.create_event("golden_idol")
    choices = event.get_choices()
    assert len(choices) == 2
    assert choices[0].label == "Touch the idol"
    assert choices[1].label == "Leave"


def test_golden_idol_touch_gives_relic_then_boulder():
    event = sts_sim.create_event("golden_idol")
    # Touch the idol
    outcome = event.choose(0)
    assert outcome.relic_added is not None
    assert not outcome.done  # still need to face boulder
    assert event.stage == 1

    # Boulder
    choices = event.get_choices()
    assert len(choices) == 1  # only "outrun the boulder"
    outcome2 = event.choose(0)
    assert outcome2.hp_change == -1
    assert outcome2.done


def test_golden_idol_leave():
    event = sts_sim.create_event("golden_idol")
    outcome = event.choose(1)
    assert outcome.done
    assert outcome.hp_change == 0


# ============================================================
# Golden Wing
# ============================================================

def test_golden_wing_pursue_costs_hp_and_removes():
    event = sts_sim.create_event("golden_wing")
    outcome = event.choose(0)
    assert outcome.hp_change == -2
    assert outcome.needs_card_select
    assert outcome.card_select_action == "remove"
    assert outcome.done


def test_golden_wing_demand_gold():
    event = sts_sim.create_event("golden_wing")
    outcome = event.choose(1)
    assert outcome.gold_change == 2
    assert outcome.done


# ============================================================
# World of Goop
# ============================================================

def test_world_of_goop_gather_gold():
    event = sts_sim.create_event("world_of_goop")
    outcome = event.choose(0)
    assert outcome.hp_change == -2
    assert outcome.gold_change == 3
    assert outcome.done


def test_world_of_goop_demand_relic():
    event = sts_sim.create_event("world_of_goop")
    outcome = event.choose(1)
    assert outcome.relic_added is not None
    assert len(outcome.cards_added) == 1  # curse
    assert outcome.done


def test_world_of_goop_leave():
    event = sts_sim.create_event("world_of_goop")
    outcome = event.choose(2)
    assert outcome.gold_change == -1
    assert outcome.done


# ============================================================
# Cleric
# ============================================================

def test_cleric_choices_enabled_by_gold():
    event = sts_sim.create_event("cleric")
    deck = [sts_sim.CardInstance(sts_sim.Card.StrikeRed)] * 3
    # With 0 gold, only leave is enabled
    choices = event.get_choices(gold=0, deck=deck)
    assert not choices[0].enabled  # Heal costs 1
    assert not choices[1].enabled  # Upgrade costs 2
    assert not choices[2].enabled  # Purify costs 3
    assert choices[3].enabled      # Leave always enabled

    # With 3 gold, all enabled
    choices = event.get_choices(gold=3, deck=deck)
    assert choices[0].enabled
    assert choices[1].enabled  # but deck has only base strikes, so upgradable
    assert choices[2].enabled
    assert choices[3].enabled


def test_cleric_heal():
    event = sts_sim.create_event("cleric")
    outcome = event.choose(0)
    assert outcome.hp_change == 3
    assert outcome.gold_change == -1
    assert outcome.done


def test_cleric_upgrade():
    event = sts_sim.create_event("cleric")
    outcome = event.choose(1)
    assert outcome.gold_change == -2
    assert outcome.needs_card_select
    assert outcome.card_select_action == "upgrade"
    assert outcome.done


def test_cleric_purify():
    event = sts_sim.create_event("cleric")
    outcome = event.choose(2)
    assert outcome.gold_change == -3
    assert outcome.needs_card_select
    assert outcome.card_select_action == "remove"
    assert outcome.done


def test_cleric_leave():
    event = sts_sim.create_event("cleric")
    outcome = event.choose(3)
    assert outcome.hp_change == 0
    assert outcome.gold_change == 0
    assert outcome.done


# ============================================================
# Living Wall
# ============================================================

def test_living_wall_forget():
    event = sts_sim.create_event("living_wall")
    outcome = event.choose(0)
    assert outcome.needs_card_select
    assert outcome.card_select_action == "remove"
    assert outcome.done


def test_living_wall_change():
    event = sts_sim.create_event("living_wall")
    outcome = event.choose(1)
    assert outcome.needs_card_select
    assert outcome.card_select_action == "transform"
    assert outcome.done


def test_living_wall_grow():
    event = sts_sim.create_event("living_wall")
    outcome = event.choose(2)
    assert outcome.needs_card_select
    assert outcome.card_select_action == "upgrade"
    assert outcome.done


# ============================================================
# Scrap Ooze (die-roll event)
# ============================================================

def test_scrap_ooze_reach_in_needs_roll():
    event = sts_sim.create_event("scrap_ooze")
    outcome = event.choose(0)
    assert not outcome.done  # needs die roll


def test_scrap_ooze_low_roll_damage():
    event = sts_sim.create_event("scrap_ooze")
    event.choose(0)  # reach in
    outcome = event.resolve_die_roll(1)
    assert outcome.hp_change == -1
    assert not outcome.done  # can try again


def test_scrap_ooze_mid_roll_gold():
    event = sts_sim.create_event("scrap_ooze")
    event.choose(0)
    outcome = event.resolve_die_roll(4)
    assert outcome.gold_change == 2
    assert outcome.done


def test_scrap_ooze_high_roll_relic():
    event = sts_sim.create_event("scrap_ooze")
    event.choose(0)
    outcome = event.resolve_die_roll(6)
    assert outcome.relic_added is not None
    assert outcome.done


def test_scrap_ooze_leave():
    event = sts_sim.create_event("scrap_ooze")
    outcome = event.choose(1)
    assert outcome.done


# ============================================================
# Dead Adventurer (die-roll event)
# ============================================================

def test_dead_adventurer_low_roll_elite():
    event = sts_sim.create_event("dead_adventurer")
    event.choose(0)
    outcome = event.resolve_die_roll(2)
    assert "elite" in outcome.description.lower()
    assert outcome.done


def test_dead_adventurer_mid_roll_gold():
    event = sts_sim.create_event("dead_adventurer")
    event.choose(0)
    outcome = event.resolve_die_roll(3)
    assert outcome.gold_change == 2
    assert outcome.done


def test_dead_adventurer_high_roll_relic():
    event = sts_sim.create_event("dead_adventurer")
    event.choose(0)
    outcome = event.resolve_die_roll(5)
    assert outcome.relic_added is not None
    assert outcome.done


# ============================================================
# Knowing Skull
# ============================================================

def test_knowing_skull_initial_choices():
    event = sts_sim.create_event("knowing_skull")
    choices = event.get_choices(hp=10)
    assert len(choices) == 4
    assert choices[0].label == "Potion"
    assert choices[1].label == "Gold"
    assert choices[2].label == "Card"
    assert choices[3].label == "Leave"


def test_knowing_skull_gold_costs_hp():
    event = sts_sim.create_event("knowing_skull")
    outcome = event.choose(1)  # Gold
    assert outcome.hp_change == -1  # First pick costs 1 HP
    assert outcome.gold_change == 3
    assert not outcome.done  # can make second pick


def test_knowing_skull_second_pick_costs_more():
    event = sts_sim.create_event("knowing_skull")
    event.choose(1)  # First pick: Gold
    outcome = event.choose(0)  # Second pick: Potion
    assert outcome.hp_change == -2  # Second pick costs 2 HP
    assert outcome.done  # max 2 picks


def test_knowing_skull_leave_early():
    event = sts_sim.create_event("knowing_skull")
    outcome = event.choose(3)  # Leave
    assert outcome.done
    assert outcome.hp_change == 0


def test_knowing_skull_cant_afford_if_low_hp():
    event = sts_sim.create_event("knowing_skull")
    # With 1 HP, can't afford anything (cost 1 HP would kill)
    choices = event.get_choices(hp=1)
    assert not choices[0].enabled
    assert not choices[1].enabled
    assert not choices[2].enabled
    assert choices[3].enabled  # Leave always enabled


# ============================================================
# Smoke tests — all events create without crash
# ============================================================

@pytest.mark.parametrize("name", [
    "big_fish",
    "golden_idol",
    "golden_wing",
    "world_of_goop",
    "cleric",
    "living_wall",
    "scrap_ooze",
    "dead_adventurer",
    "knowing_skull",
])
def test_event_smoke(name):
    """Creating any event and getting choices should not crash."""
    event = sts_sim.create_event(name)
    choices = event.get_choices(gold=5, hp=10, max_hp=10)
    assert len(choices) > 0
    # Make first choice
    outcome = event.choose(0)
    assert outcome is not None
