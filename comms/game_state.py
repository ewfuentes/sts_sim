"""Parse CommunicationMod JSON into structured Python objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ScreenType(Enum):
    EVENT = "EVENT"
    CHEST = "CHEST"
    SHOP_ROOM = "SHOP_ROOM"
    REST = "REST"
    CARD_REWARD = "CARD_REWARD"
    COMBAT_REWARD = "COMBAT_REWARD"
    MAP = "MAP"
    BOSS_REWARD = "BOSS_REWARD"
    SHOP_SCREEN = "SHOP_SCREEN"
    GRID = "GRID"
    HAND_SELECT = "HAND_SELECT"
    GAME_OVER = "GAME_OVER"
    COMPLETE = "COMPLETE"
    NONE = "NONE"


class Intent(Enum):
    ATTACK = "ATTACK"
    ATTACK_BUFF = "ATTACK_BUFF"
    ATTACK_DEBUFF = "ATTACK_DEBUFF"
    ATTACK_DEFEND = "ATTACK_DEFEND"
    BUFF = "BUFF"
    DEBUFF = "DEBUFF"
    STRONG_DEBUFF = "STRONG_DEBUFF"
    DEBUG = "DEBUG"
    DEFEND = "DEFEND"
    DEFEND_DEBUFF = "DEFEND_DEBUFF"
    DEFEND_BUFF = "DEFEND_BUFF"
    ESCAPE = "ESCAPE"
    MAGIC = "MAGIC"
    NONE = "NONE"
    SLEEP = "SLEEP"
    STUN = "STUN"
    UNKNOWN = "UNKNOWN"


class CardType(Enum):
    ATTACK = "ATTACK"
    SKILL = "SKILL"
    POWER = "POWER"
    STATUS = "STATUS"
    CURSE = "CURSE"


class CardRarity(Enum):
    BASIC = "BASIC"
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    SPECIAL = "SPECIAL"
    CURSE = "CURSE"


@dataclass
class Power:
    power_id: str
    name: str
    amount: int
    damage: int = 0
    misc: int = 0
    just_applied: bool = False

    @staticmethod
    def from_json(data: dict) -> Power:
        return Power(
            power_id=data.get("id", ""),
            name=data.get("name", ""),
            amount=data.get("amount", 0),
            damage=data.get("damage", 0),
            misc=data.get("misc", 0),
            just_applied=data.get("just_applied", False),
        )


@dataclass
class Card:
    card_id: str
    name: str
    card_type: CardType
    rarity: CardRarity
    uuid: str = ""
    cost: int = 0
    upgrades: int = 0
    has_target: bool = False
    is_playable: bool = False
    exhausts: bool = False
    misc: int = 0
    price: int = 0

    @staticmethod
    def from_json(data: dict) -> Card:
        return Card(
            card_id=data.get("id", ""),
            name=data.get("name", ""),
            card_type=CardType(data.get("type", "ATTACK")),
            rarity=CardRarity(data.get("rarity", "BASIC")),
            uuid=data.get("uuid", ""),
            cost=data.get("cost", 0),
            upgrades=data.get("upgrades", 0),
            has_target=data.get("has_target", False),
            is_playable=data.get("is_playable", False),
            exhausts=data.get("exhausts", False),
            misc=data.get("misc", 0),
            price=data.get("price", 0),
        )


@dataclass
class Relic:
    relic_id: str
    name: str
    counter: int = 0
    price: int = 0

    @staticmethod
    def from_json(data: dict) -> Relic:
        return Relic(
            relic_id=data.get("id", ""),
            name=data.get("name", ""),
            counter=data.get("counter", 0),
            price=data.get("price", 0),
        )


@dataclass
class Potion:
    potion_id: str
    name: str
    can_use: bool = False
    can_discard: bool = False
    requires_target: bool = False
    price: int = 0

    @staticmethod
    def from_json(data: dict) -> Potion:
        return Potion(
            potion_id=data.get("id", ""),
            name=data.get("name", ""),
            can_use=data.get("can_use", False),
            can_discard=data.get("can_discard", False),
            requires_target=data.get("requires_target", False),
            price=data.get("price", 0),
        )


@dataclass
class Monster:
    name: str
    monster_id: str
    max_hp: int
    current_hp: int
    block: int
    intent: Intent
    half_dead: bool = False
    is_gone: bool = False
    move_id: int = 0
    last_move_id: int = 0
    second_last_move_id: int = 0
    move_base_damage: int = 0
    move_adjusted_damage: int = 0
    move_hits: int = 0
    powers: list[Power] = field(default_factory=list)
    monster_index: int = 0

    @staticmethod
    def from_json(data: dict, index: int = 0) -> Monster:
        intent_str = data.get("intent", "UNKNOWN")
        try:
            intent = Intent(intent_str)
        except ValueError:
            intent = Intent.UNKNOWN
        return Monster(
            name=data.get("name", ""),
            monster_id=data.get("id", ""),
            max_hp=data.get("max_hp", 0),
            current_hp=data.get("current_hp", 0),
            block=data.get("block", 0),
            intent=intent,
            half_dead=data.get("half_dead", False),
            is_gone=data.get("is_gone", False),
            move_id=data.get("move_id", 0),
            last_move_id=data.get("last_move_id", 0),
            second_last_move_id=data.get("second_last_move_id", 0),
            move_base_damage=data.get("move_base_damage", 0),
            move_adjusted_damage=data.get("move_adjusted_damage", 0),
            move_hits=data.get("move_hits", 0),
            powers=[Power.from_json(p) for p in data.get("powers", [])],
            monster_index=index,
        )

    def get_power(self, power_id: str) -> Optional[Power]:
        for p in self.powers:
            if p.power_id == power_id:
                return p
        return None


@dataclass
class Player:
    max_hp: int
    current_hp: int
    block: int
    energy: int
    powers: list[Power] = field(default_factory=list)

    @staticmethod
    def from_json(data: dict) -> Player:
        return Player(
            max_hp=data.get("max_hp", 0),
            current_hp=data.get("current_hp", 0),
            block=data.get("block", 0),
            energy=data.get("energy", 0),
            powers=[Power.from_json(p) for p in data.get("powers", [])],
        )

    def get_power(self, power_id: str) -> Optional[Power]:
        for p in self.powers:
            if p.power_id == power_id:
                return p
        return None


@dataclass
class CombatState:
    player: Player
    monsters: list[Monster]
    hand: list[Card]
    draw_pile: list[Card]
    discard_pile: list[Card]
    exhaust_pile: list[Card]
    turn: int = 0
    cards_discarded_this_turn: int = 0

    @staticmethod
    def from_json(data: dict) -> CombatState:
        return CombatState(
            player=Player.from_json(data.get("player", {})),
            monsters=[Monster.from_json(m, i) for i, m in enumerate(data.get("monsters", []))],
            hand=[Card.from_json(c) for c in data.get("hand", [])],
            draw_pile=[Card.from_json(c) for c in data.get("draw_pile", [])],
            discard_pile=[Card.from_json(c) for c in data.get("discard_pile", [])],
            exhaust_pile=[Card.from_json(c) for c in data.get("exhaust_pile", [])],
            turn=data.get("turn", 0),
            cards_discarded_this_turn=data.get("cards_discarded_this_turn", 0),
        )


@dataclass
class MapNode:
    x: int
    y: int
    symbol: str
    children: list[MapNode] = field(default_factory=list)

    @staticmethod
    def from_json(data: dict) -> MapNode:
        node = MapNode(
            x=data.get("x", 0),
            y=data.get("y", 0),
            symbol=data.get("symbol", "?"),
        )
        for child_data in data.get("children", []):
            node.children.append(MapNode.from_json(child_data))
        return node


@dataclass
class EventOption:
    text: str
    label: str = ""
    choice_index: int = 0
    disabled: bool = False

    @staticmethod
    def from_json(data: dict, index: int = 0) -> EventOption:
        return EventOption(
            text=data.get("text", ""),
            label=data.get("label", ""),
            choice_index=index,
            disabled=data.get("disabled", False),
        )


@dataclass
class GameState:
    """Full game state from CommunicationMod."""
    # General
    current_hp: int = 0
    max_hp: int = 0
    floor: int = 0
    act: int = 1
    gold: int = 0
    seed: int = 0
    character_class: str = "IRONCLAD"
    ascension_level: int = 0

    # Deck/relics/potions
    deck: list[Card] = field(default_factory=list)
    relics: list[Relic] = field(default_factory=list)
    potions: list[Potion] = field(default_factory=list)

    # Map
    map_nodes: list[MapNode] = field(default_factory=list)
    act_boss: str = ""

    # Screen
    screen_type: ScreenType = ScreenType.NONE
    room_phase: str = ""
    room_type: str = ""
    is_screen_up: bool = False
    choice_list: list[str] = field(default_factory=list)
    available_commands: list[str] = field(default_factory=list)

    # Combat (only populated during combat)
    combat_state: Optional[CombatState] = None

    # Screen-specific data
    screen_data: dict = field(default_factory=dict)


def parse_game_state(data: dict, available_commands: Optional[list] = None) -> GameState:
    """Parse raw game_state JSON dict into a GameState object."""
    gs = GameState()

    gs.current_hp = data.get("current_hp", 0)
    gs.max_hp = data.get("max_hp", 0)
    gs.floor = data.get("floor", 0)
    gs.act = data.get("act", 1)
    gs.gold = data.get("gold", 0)
    gs.seed = data.get("seed", 0)
    gs.character_class = data.get("class", "IRONCLAD")
    gs.ascension_level = data.get("ascension_level", 0)
    gs.act_boss = data.get("act_boss", "")

    gs.deck = [Card.from_json(c) for c in data.get("deck", [])]
    gs.relics = [Relic.from_json(r) for r in data.get("relics", [])]
    gs.potions = [Potion.from_json(p) for p in data.get("potions", [])]
    gs.map_nodes = [MapNode.from_json(n) for n in data.get("map", [])]

    gs.is_screen_up = data.get("is_screen_up", False)
    gs.room_phase = data.get("room_phase", "")
    gs.room_type = data.get("room_type", "")
    gs.choice_list = data.get("choice_list", [])
    gs.available_commands = available_commands or []

    screen_type_str = data.get("screen_type", "NONE")
    try:
        gs.screen_type = ScreenType(screen_type_str)
    except ValueError:
        gs.screen_type = ScreenType.NONE

    gs.screen_data = data.get("screen_state", {}) or {}

    combat_data = data.get("combat_state")
    if combat_data:
        gs.combat_state = CombatState.from_json(combat_data)

    return gs
