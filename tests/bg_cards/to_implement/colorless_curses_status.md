# Unimplemented Cards: Colorless, Curses, Status

## Summary

This file tracks all cards that are NOT yet implemented in the simulator ([N] tag)
and lists missing APIs that would be needed to fully test them.

---

## Colorless Common (ALL unimplemented)

- **Blind** — BGBlind — Skill, Cost 0
  Needs: Card enum, WEAK application, Exhaust mechanic
- **Finesse** — BGFinesse — Skill, Cost 0
  Needs: Card enum, block gain, draw, Exhaust mechanic
- **Flash of Steel** — BGFlash of Steel — Attack, Cost 0
  Needs: Card enum, 1 HIT damage, draw, Exhaust mechanic
- **Good Instincts** — BGGood Instincts — Skill, Cost 0
  Needs: Card enum, block gain, multi-player targeting API
- **Impatience** — BGImpatience — Skill, Cost 0
  Needs: Card enum, draw 2/3 cards
- **Madness** — BGMadness — Skill, Cost 0
  Needs: Card enum, "next card costs 0" effect, Retain keyword, Exhaust
- **Purity** — BGPurity — Skill, Cost 0
  Needs: Card enum, "exhaust up to N from hand" choice mechanic
- **Swift Strike** — BGSwift Strike — Attack, Cost 0
  Needs: Card enum, 1 HIT damage, row-switching API (multi-player)
- **Thinking Ahead** — BGThinking Ahead — Skill, Cost 0
  Needs: Card enum, draw, put-card-on-top-of-draw mechanic, Exhaust
- **Trip** — BGTrip — Skill, Cost 0
  Needs: Card enum, VULN application, Exhaust mechanic

## Colorless Uncommon (ALL unimplemented)

- **Dark Shackles** — BGDarkShackles — Skill, Cost 0
  Needs: Card enum, enemy intent query API, conditional block gain, Exhaust
- **Dramatic Entrance** — BGDramatic Entrance — Attack, Cost 0
  Needs: Card enum, AOE damage, turn-number tracking, first-turn bonus, Exhaust
- **Hand of Greed** — BGHandOfGreed — Attack, Cost 2
  Needs: Card enum, gold tracking API, conditional bonus damage
- **Mayhem** — BGMayhem — Power, Cost 2
  Needs: Card enum, Power type, auto-draw-and-play trigger, once-per-turn limit
- **Mind Blast** — BGMind Blast — Attack, Cost 2
  Needs: Card enum, dynamic damage based on hand size
- **Panacea** — BGPanacea — Skill, Cost 0
  Needs: Card enum, debuff removal API, Retain keyword, multi-player targeting, Exhaust
- **Sadistic Nature** — BGSadistic Nature — Power, Cost 0
  Needs: Card enum, Power type, on-debuff-apply trigger, reactive damage

## Colorless Rare (ALL unimplemented)

- **Apotheosis** — BGApotheosis — Skill, Cost 2
  Needs: Card enum, starter-card identification, persistent buff to starter Strikes/Defends
- **Apparition** — BGGhostly — Skill, Cost 1
  Needs: Card enum, damage cap mechanic (max 1 HP loss per turn), Ethereal, Exhaust
- **Master of Strategy** — BGMaster of Strategy — Skill, Cost 0
  Needs: Card enum, draw 3/4 cards
- **Panache** — BGPanache — Power, Cost 0
  Needs: Card enum, Power type, end-of-turn trigger, empty-hand check, row-targeting damage
- **The Bomb** — BGThe Bomb — Skill, Cost 2
  Needs: Card enum, delayed-effect countdown (3 turns), AOE damage, Exhaust

## Curses (6 of 10 unimplemented)

Implemented: AscendersBane, Decay, Injury, Pain

- **Clumsy** — Clumsy — Curse, Cost -2
  Needs: Card enum, Unplayable flag, Ethereal keyword
- **Doubt** — BGDoubt — Curse, Cost -2
  Needs: Card enum, Unplayable flag, end-of-turn WEAK application
- **Parasite** — BGParasite — Curse, Cost -2
  Needs: Card enum, Unplayable flag, on-removal HP loss trigger
- **Regret** — BGRegret — Curse, Cost -2
  Needs: Card enum, Unplayable flag, Retain keyword
- **Shame** — BGShame — Curse, Cost -2
  Needs: Card enum, Unplayable flag, end-of-turn block reduction
- **Writhe** — BGWrithe — Curse, Cost 1
  Needs: Card enum, playable curse (cost 1), Exhaust on play

## Status (1 of 5 unimplemented)

Implemented: Burn, Dazed, Slimed, VoidCard

- **Desync** — BGDesync — Status, Cost -2
  Needs: Card enum, Unplayable flag (error indicator card, mod compatibility issue)

---

## Missing APIs / Mechanics Needed

1. **Multi-player targeting** — Good Instincts, Panacea target "any player" or "all players"
2. **Row-switching** — Swift Strike allows switching rows with another player
3. **Row-targeting damage** — Panache deals damage to "any row"
4. **Gold tracking** — Hand of Greed checks player gold amount
5. **Enemy intent query** — Dark Shackles needs to know which enemies intend to attack
6. **Turn-number tracking** — Dramatic Entrance checks if it's the first turn of combat
7. **Next-card-cost-zero effect** — Madness applies a one-shot cost reduction
8. **Delayed effects / countdown** — The Bomb detonates after 3 turns
9. **Auto-draw-and-play** — Mayhem draws and plays a card automatically each turn
10. **Dynamic damage from hand size** — Mind Blast deals X damage where X = other cards in hand
11. **Damage cap** — Apparition limits HP loss to 1 per turn
12. **Starter card identification** — Apotheosis buffs only starter Strikes/Defends
13. **On-debuff-apply trigger** — Sadistic Nature deals damage when tokens are applied
14. **Put-card-on-top-of-draw** — Thinking Ahead places a chosen card on top of draw pile
15. **Exhaust-from-hand choice** — Purity lets player choose cards to exhaust from hand
16. **Retain keyword** — Madness+, Panacea, Regret stay in hand across turns
17. **On-removal trigger** — Parasite triggers HP loss when removed from deck
18. **End-of-turn curse effects** — Doubt (WEAK), Shame (block loss) need end-of-turn hooks
