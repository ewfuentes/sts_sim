"""Tests for multi-character infrastructure (Phase 1)."""
import sts_sim


def test_character_enum_exists():
    """Character enum is accessible from Python."""
    assert sts_sim.Character.Ironclad is not None
    assert sts_sim.Character.Silent is not None
    assert sts_sim.Character.Defect is not None
    assert sts_sim.Character.Watcher is not None


def test_default_player_is_ironclad():
    """Player() with no args creates Ironclad."""
    p = sts_sim.Player()
    assert p.name == "Ironclad"
    assert p.hp == 10
    assert p.max_hp == 10


def test_ironclad_player():
    """Ironclad: 10 HP, BurningBlood relic, 10-card deck."""
    p = sts_sim.Player(sts_sim.Character.Ironclad)
    assert p.name == "Ironclad"
    assert p.hp == 10
    assert p.max_hp == 10


def test_silent_player():
    """Silent: 9 HP, RingOfTheSnake + Shivs relics."""
    p = sts_sim.Player(sts_sim.Character.Silent)
    assert p.name == "Silent"
    assert p.hp == 9
    assert p.max_hp == 9


def test_defect_player():
    """Defect: 9 HP, CrackedCore relic."""
    p = sts_sim.Player(sts_sim.Character.Defect)
    assert p.name == "Defect"
    assert p.hp == 9
    assert p.max_hp == 9


def test_watcher_player():
    """Watcher: 9 HP, Miracles relic."""
    p = sts_sim.Player(sts_sim.Character.Watcher)
    assert p.name == "Watcher"
    assert p.hp == 9
    assert p.max_hp == 9


def test_ironclad_starter_deck():
    """Ironclad starter: 5 Strike, 4 Defend, 1 Bash = 10 cards."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Ironclad)
    deck = cs.get_deck()
    assert len(deck) == 10
    strikes = [c for c in deck if c.card == sts_sim.Card.StrikeRed]
    defends = [c for c in deck if c.card == sts_sim.Card.DefendRed]
    bashes = [c for c in deck if c.card == sts_sim.Card.Bash]
    assert len(strikes) == 5
    assert len(defends) == 4
    assert len(bashes) == 1


def test_silent_starter_deck():
    """Silent starter: 5 Strike, 5 Defend, 1 Neutralize, 1 Survivor = 12 cards."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Silent)
    deck = cs.get_deck()
    assert len(deck) == 12
    strikes = [c for c in deck if c.card == sts_sim.Card.StrikeGreen]
    defends = [c for c in deck if c.card == sts_sim.Card.DefendGreen]
    neutralizes = [c for c in deck if c.card == sts_sim.Card.Neutralize]
    survivors = [c for c in deck if c.card == sts_sim.Card.Survivor]
    assert len(strikes) == 5
    assert len(defends) == 5
    assert len(neutralizes) == 1
    assert len(survivors) == 1


def test_defect_starter_deck():
    """Defect starter: 4 Strike, 4 Defend, 1 Zap, 1 Dualcast = 10 cards."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Defect)
    deck = cs.get_deck()
    assert len(deck) == 10
    strikes = [c for c in deck if c.card == sts_sim.Card.StrikeBlue]
    defends = [c for c in deck if c.card == sts_sim.Card.DefendBlue]
    zaps = [c for c in deck if c.card == sts_sim.Card.Zap]
    dualcasts = [c for c in deck if c.card == sts_sim.Card.Dualcast]
    assert len(strikes) == 4
    assert len(defends) == 4
    assert len(zaps) == 1
    assert len(dualcasts) == 1


def test_watcher_starter_deck():
    """Watcher starter: 4 Strike, 4 Defend, 1 Eruption, 1 Vigilance = 10 cards."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Watcher)
    deck = cs.get_deck()
    assert len(deck) == 10
    strikes = [c for c in deck if c.card == sts_sim.Card.StrikePurple]
    defends = [c for c in deck if c.card == sts_sim.Card.DefendPurple]
    eruptions = [c for c in deck if c.card == sts_sim.Card.Eruption]
    vigilances = [c for c in deck if c.card == sts_sim.Card.Vigilance]
    assert len(strikes) == 4
    assert len(defends) == 4
    assert len(eruptions) == 1
    assert len(vigilances) == 1


def test_encounter_default_is_ironclad():
    """create_encounter without character arg defaults to Ironclad."""
    cs = sts_sim.create_encounter("jaw_worm", 0)
    assert cs.player.name == "Ironclad"
    assert cs.player.hp == 10
    deck = cs.get_deck()
    assert len(deck) == 10


def test_starter_card_types():
    """Verify card types for all starter cards."""
    # Silent
    assert sts_sim.Card.StrikeGreen.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.DefendGreen.py_card_type == sts_sim.CardType.Skill
    assert sts_sim.Card.Neutralize.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.Survivor.py_card_type == sts_sim.CardType.Skill
    # Defect
    assert sts_sim.Card.StrikeBlue.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.DefendBlue.py_card_type == sts_sim.CardType.Skill
    assert sts_sim.Card.Zap.py_card_type == sts_sim.CardType.Skill
    assert sts_sim.Card.Dualcast.py_card_type == sts_sim.CardType.Skill
    # Watcher
    assert sts_sim.Card.StrikePurple.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.DefendPurple.py_card_type == sts_sim.CardType.Skill
    assert sts_sim.Card.Eruption.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.Vigilance.py_card_type == sts_sim.CardType.Skill


def test_starter_card_costs():
    """Verify costs for all starter cards."""
    assert sts_sim.Card.StrikeGreen.py_cost == 1
    assert sts_sim.Card.DefendGreen.py_cost == 1
    assert sts_sim.Card.Neutralize.py_cost == 0
    assert sts_sim.Card.Survivor.py_cost == 1
    assert sts_sim.Card.StrikeBlue.py_cost == 1
    assert sts_sim.Card.DefendBlue.py_cost == 1
    assert sts_sim.Card.Zap.py_cost == 1
    assert sts_sim.Card.Dualcast.py_cost == 1
    assert sts_sim.Card.StrikePurple.py_cost == 1
    assert sts_sim.Card.DefendPurple.py_cost == 1
    assert sts_sim.Card.Eruption.py_cost == 2
    assert sts_sim.Card.Vigilance.py_cost == 2


def test_starter_relic_new_relics_exist():
    """New relic enum values exist."""
    assert sts_sim.Relic.RingOfTheSnake is not None
    assert sts_sim.Relic.Shivs is not None
    assert sts_sim.Relic.CrackedCore is not None
    assert sts_sim.Relic.Miracles is not None


def test_neutralize_applies_weak():
    """Neutralize deals damage and applies 1 Weak."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Silent)
    cs.start_combat()
    monsters = cs.get_monsters()
    hp_before = monsters[0].hp
    # Find Neutralize in hand (cost 0)
    hand = cs.get_hand()
    neut_idx = None
    for i, c in enumerate(hand):
        if c.card == sts_sim.Card.Neutralize:
            neut_idx = i
            break
    if neut_idx is not None:
        cs.play_card(neut_idx, 0)
        monsters = cs.get_monsters()
        assert monsters[0].hp < hp_before
        assert monsters[0].get_power(sts_sim.PowerType.Weak) > 0


def test_survivor_gives_block_and_discards():
    """Survivor gives block and discards 1 card."""
    cs = sts_sim.create_encounter("jaw_worm", 0, sts_sim.Character.Silent)
    cs.start_combat()
    hand = cs.get_hand()
    surv_idx = None
    for i, c in enumerate(hand):
        if c.card == sts_sim.Card.Survivor:
            surv_idx = i
            break
    if surv_idx is not None:
        hand_before = len(cs.get_hand())
        cs.play_card(surv_idx, None)
        # Survivor itself is removed + 1 discard = 2 fewer cards
        assert len(cs.get_hand()) == hand_before - 2
        assert cs.player.block > 0


def test_reward_deck_accepts_character():
    """RewardDeck accepts character parameter."""
    rd = sts_sim.RewardDeck(0, sts_sim.Character.Ironclad)
    cards = rd.draw_rewards(3)
    assert len(cards) == 3


def test_shop_accepts_character():
    """create_shop accepts character parameter."""
    shop = sts_sim.create_shop(0, sts_sim.Character.Ironclad)
    assert len(shop.items) > 0
