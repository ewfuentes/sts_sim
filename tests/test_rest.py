"""Tests for rest site system."""
import pytest
import sts_sim


def test_create_rest_site():
    rest = sts_sim.create_rest_site()
    assert not rest.done


def test_rest_choices():
    rest = sts_sim.create_rest_site()
    choices = rest.get_choices()
    assert len(choices) == 2
    assert choices[0].label == "Rest"
    assert choices[1].label == "Smith"


def test_rest_heals_3hp():
    rest = sts_sim.create_rest_site()
    outcome = rest.choose(0)
    assert outcome.hp_healed == 3
    assert not outcome.needs_card_select
    assert rest.done


def test_smith_upgrades_card():
    rest = sts_sim.create_rest_site()
    outcome = rest.choose(1)
    assert outcome.hp_healed == 0
    assert outcome.needs_card_select
    assert outcome.card_select_action == "upgrade"
    assert rest.done


def test_rest_enabled():
    rest = sts_sim.create_rest_site()
    choices = rest.get_choices()
    assert choices[0].enabled  # Rest always enabled


def test_smith_disabled_if_no_upgradable():
    rest = sts_sim.create_rest_site()
    # All upgraded deck
    deck = [
        sts_sim.CardInstance(sts_sim.Card.StrikeRed, True),
        sts_sim.CardInstance(sts_sim.Card.DefendRed, True),
    ]
    choices = rest.get_choices(deck=deck)
    assert not choices[1].enabled  # Smith disabled


def test_smith_enabled_if_has_upgradable():
    rest = sts_sim.create_rest_site()
    deck = [
        sts_sim.CardInstance(sts_sim.Card.StrikeRed, False),
        sts_sim.CardInstance(sts_sim.Card.DefendRed, True),
    ]
    choices = rest.get_choices(deck=deck)
    assert choices[1].enabled  # Smith enabled
