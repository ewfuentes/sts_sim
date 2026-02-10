# sts_bot_2 — Slay the Spire Bot

## Overview

A Python bot for Slay the Spire. Two-phase approach:

1. **Simulator** — Standalone engine modeling STS game mechanics (cards, relics, enemies, combat, map navigation). Used for strategy analysis and testing.
2. **Game Agent** — Connects to a running STS instance via CommunicationMod to play actual runs using the simulator's logic.

## Project Structure

```
sts_bot_2/
├── simulator/          # Core game simulation
│   ├── cards/          # Card definitions and effects
│   ├── relics/         # Relic definitions and effects
│   ├── enemies/        # Enemy AI and intent patterns
│   ├── combat.py       # Combat loop simulation
│   ├── map.py          # Map generation and pathing
│   └── player.py       # Player state (HP, deck, energy, etc.)
├── agent/              # Decision-making AI
│   ├── strategy.py     # High-level strategy (pathing, card picks)
│   └── combat_ai.py    # Combat decision-making (card play order)
├── comms/              # CommunicationMod integration
│   └── client.py       # WebSocket/stdin client for game connection
├── tests/              # pytest test suite
└── main.py             # Entry point
```

## Development

- **Language:** Python 3.10+
- **Tests:** `pytest tests/`
- **Run simulator:** `python -m simulator`
- **Run agent:** `python main.py`

## Key Design Decisions

- Start with Ironclad only, expand to other characters later
- Model combat mechanics first (energy, cards, block, damage, buffs/debuffs)
- Enemy intents and patterns should be data-driven
- Card effects should be composable (deal damage, apply buff, draw cards, etc.)
- Prioritize correctness of simulation over performance

## STS Mechanics Reference

- 3 energy per turn (base), draw 5 cards per turn (base)
- Block resets each turn, HP persists across combats
- 4 acts, each with branching map paths (fights, elites, shops, rest sites, events, treasure)
- Characters: Ironclad, Silent, Defect, Watcher (start with Ironclad)
