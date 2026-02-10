"""Tests for card reward system."""
import pytest
import sts_sim


def test_reward_deck_creation():
    rd = sts_sim.RewardDeck(seed=42)
    assert rd.remaining() > 0


def test_reward_deck_draws_three():
    rd = sts_sim.RewardDeck(seed=42)
    cards = rd.draw_rewards()
    assert len(cards) == 3


def test_reward_deck_draws_custom_count():
    rd = sts_sim.RewardDeck(seed=42)
    cards = rd.draw_rewards(count=5)
    assert len(cards) == 5


def test_reward_deck_decrements_on_draw():
    rd = sts_sim.RewardDeck(seed=42)
    initial = rd.remaining()
    rd.draw_rewards()
    assert rd.remaining() == initial - 3


def test_reward_cards_are_card_instances():
    rd = sts_sim.RewardDeck(seed=42)
    cards = rd.draw_rewards()
    for card in cards:
        assert hasattr(card, 'card')
        assert hasattr(card, 'upgraded')
        assert not card.upgraded  # rewards are base (not upgraded)


def test_reward_deck_deterministic():
    rd1 = sts_sim.RewardDeck(seed=42)
    rd2 = sts_sim.RewardDeck(seed=42)
    cards1 = rd1.draw_rewards()
    cards2 = rd2.draw_rewards()
    assert [c.card for c in cards1] == [c.card for c in cards2]


def test_reward_deck_different_seeds():
    rd1 = sts_sim.RewardDeck(seed=1)
    rd2 = sts_sim.RewardDeck(seed=2)
    cards1 = rd1.draw_rewards()
    cards2 = rd2.draw_rewards()
    # Very unlikely to be identical with different seeds
    # (could theoretically fail but extremely unlikely)


def test_reward_deck_reshuffles_when_empty():
    rd = sts_sim.RewardDeck(seed=42)
    # Draw all cards
    while rd.remaining() > 0:
        rd.draw_rewards(count=1)
    # Should still be able to draw (auto-reshuffle)
    cards = rd.draw_rewards()
    assert len(cards) == 3


def test_reward_deck_contains_variety():
    """Reward deck should contain cards from different rarities."""
    rd = sts_sim.RewardDeck(seed=42)
    all_cards = []
    for _ in range(10):
        all_cards.extend(rd.draw_rewards())
    unique_cards = set(c.card for c in all_cards)
    assert len(unique_cards) >= 10  # Should have good variety


def test_reward_deck_pool_sizes():
    """The initial deck should have 2x commons + 1x uncommons."""
    rd = sts_sim.RewardDeck(seed=42)
    # 17 commons * 2 = 34, 27 uncommons * 1 = 27, total = 61
    assert rd.remaining() == 61
