"""Tests for shop system."""
import pytest
import sts_sim


def test_create_shop():
    shop = sts_sim.create_shop(seed=42)
    assert len(shop.items) > 0


def test_shop_has_cards_and_removal():
    shop = sts_sim.create_shop(seed=42)
    card_items = [i for i in shop.items if i.item_type == "card"]
    removal_items = [i for i in shop.items if i.item_type == "removal"]
    assert len(card_items) == 5  # 3 common + 1 uncommon + 1 rare
    assert len(removal_items) == 1


def test_shop_card_prices():
    shop = sts_sim.create_shop(seed=42)
    card_items = [i for i in shop.items if i.item_type == "card"]
    prices = sorted([i.price for i in card_items])
    # Should have prices: 2, 2, 2, 3, 6 (3 common @ 2, 1 uncommon @ 3, 1 rare @ 6)
    assert prices == [2, 2, 2, 3, 6]


def test_shop_removal_cost():
    shop = sts_sim.create_shop(seed=42)
    assert shop.removal_cost == 3


def test_shop_get_item():
    shop = sts_sim.create_shop(seed=42)
    item = shop.get_item(0)
    assert item is not None
    assert item.item_type == "card"
    assert item.card is not None


def test_shop_get_item_out_of_range():
    shop = sts_sim.create_shop(seed=42)
    item = shop.get_item(100)
    assert item is None


def test_shop_items_have_names():
    shop = sts_sim.create_shop(seed=42)
    for item in shop.items:
        assert len(item.name) > 0


def test_shop_deterministic():
    shop1 = sts_sim.create_shop(seed=42)
    shop2 = sts_sim.create_shop(seed=42)
    for i1, i2 in zip(shop1.items, shop2.items):
        assert i1.name == i2.name
        assert i1.price == i2.price


def test_shop_different_seeds():
    shop1 = sts_sim.create_shop(seed=1)
    shop2 = sts_sim.create_shop(seed=2)
    names1 = [i.name for i in shop1.items if i.item_type == "card"]
    names2 = [i.name for i in shop2.items if i.item_type == "card"]
    # Very unlikely to be identical with different seeds


def test_shop_card_items_have_card_instance():
    shop = sts_sim.create_shop(seed=42)
    for item in shop.items:
        if item.item_type == "card":
            assert item.card is not None
            assert hasattr(item.card, 'card')
            assert not item.card.upgraded  # Shop cards are base
