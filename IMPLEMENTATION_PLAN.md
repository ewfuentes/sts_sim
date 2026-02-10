# Implementation Plan

Comprehensive plan of everything left to implement in the simulator.
Track progress by marking items `[x]` as they are completed.

Last updated: 2026-02-09

---

## Current State Summary

| Component | Implemented | Total in BG Mod | Coverage |
|-----------|-------------|-----------------|----------|
| Cards | ~250 | ~253 | ~99% |
| Relics | 35 | 83 | 42% |
| Enemies | 19 (Act 1 only) | 60 | 32% |
| Potions | 0 | 21 | 0% |
| Events | 9 | 45+ | ~20% |
| Shop | Cards + removal | Full | ~60% |
| Agent/Bot AI | 0 | N/A | 0% |

---

## Phase 1: Missing Cards (2 cards)

### Defect — Fix Claw (bug)
- [ ] Fix `Claw` mechanic in `combat.rs:711` — currently just a plain attack, missing core mechanic
- [ ] BG mod behavior: +1 bonus damage (upgraded: +3) if top card of discard pile costs 0
- [ ] Need to check discard pile top card cost before calculating damage
- [ ] Card glows gold when bonus is active (visual only, sim doesn't need this)

### Defect — Claw2 (skip)
Optional "for fun" card enabled by mod config. Not in default card pool — skipping.

### Watcher — TalkToTheHand (Uncommon Attack)
- [ ] Add `TalkToTheHand` card variant to `cards.rs`
- [ ] BG mod ID: `"BGTalkToTheHand"`
- [ ] Cost: 1 energy
- [ ] Base: 2 damage, gain block equal to MiracleCount (1 block per miracle)
- [ ] Upgraded: 3 damage, same block mechanic
- [ ] Needs: MiracleCount power already exists

### Ironclad — Cards NOT in BG mod (6 cards) — REMOVED
~~Hemokinesis, Intimidate, Bloodletting, DualWield, Reaper, Brutality~~ — removed from simulator, reward pools, shop, and all tests.

---

## Phase 2: Potions (21 potions — new system)

No potion system exists yet. Need to add:

### Infrastructure
- [ ] Add `Potion` enum to `enums.rs`
- [ ] Add potion slots to Player (BG mod has 2-3 slots)
- [ ] Add `use_potion(potion_index, target_index)` to combat interface
- [ ] Add potion rewards to reward system

### Common Potions (10)
| # | Potion | BG ID | Effect |
|---|--------|-------|--------|
| 1 | BloodPotion | `BGBloodPotion` | Heal 2 HP |
| 2 | BlockPotion | `BGBlock Potion` | Gain 2 Block |
| 3 | EnergyPotion | `Energy Potion` | Gain 2 Energy |
| 4 | FirePotion | `Fire Potion` | Deal 4 damage to target |
| 5 | ExplosivePotion | `BGExplosive Potion` | Deal 2 damage to ALL enemies |
| 6 | FearPotion | `BGFearPotion` | Apply 1 Vulnerable to target |
| 7 | WeakPotion | `BGWeak Potion` | Apply 2 Weak to target |
| 8 | AttackPotion | `BGAttackPotion` | DoubleTap (play attacks twice) for 1 turn |
| 9 | SkillPotion | `BGSkillPotion` | Burst (play skills twice) for 1 turn |
| 10 | SwiftPotion | `Swift Potion` | Draw 3 cards |
| 11 | SteroidPotion | `BGFlexPotion` | Gain 1 temporary Strength |
| 12 | GhostInAJar | `BGGhostInAJar` | 1 turn Invincibility |

### Uncommon Potions (5)
| # | Potion | BG ID | Effect |
|---|--------|-------|--------|
| 1 | AncientPotion | `BGAncientPotion` | Remove Weak and Vulnerable |
| 2 | ElixirPotion | `BGElixirPotion` | Exhaust 3 cards from hand |
| 3 | CunningPotion | `BGCunningPotion` | Use 3 Shivs (4 damage attacks) |
| 4 | LiquidMemories | `LiquidMemories` | Return 1 card from discard to hand, costs 0 |
| 5 | DistilledChaos | `BGDistilledChaos` | Draw 3 cards and play them |

### Rare Potions (3)
| # | Potion | BG ID | Effect |
|---|--------|-------|--------|
| 1 | FairyPotion | `BGFairyPotion` | Revive with 2 HP on death (passive) |
| 2 | SneckoOil | `BGSneckoOil` | Draw 5 cards, shuffle 2 Dazed into draw pile |
| 3 | EntropicBrew | `BGEntropicBrew` | Obtain 2 random potions |

- [ ] Implement Potion enum (21 variants)
- [ ] Implement potion infrastructure (slots, use_potion)
- [ ] Implement Common potions (12)
- [ ] Implement Uncommon potions (5)
- [ ] Implement Rare potions (3)
- [ ] Add potion tests
- [ ] Add live potion tests

---

## Phase 3: Relics — Remaining (48 relics)

35 of 83 relics are implemented. The remaining 48 are grouped by implementation complexity.

### Already Implemented (35)
BurningBlood, RingOfTheSnake, Shivs, CrackedCore, Miracles, Lantern, BagOfPreparation,
Anchor, Orichalcum, Vajra, OddlySmoothStone, PenNib, HornCleat, HappyFlower, RedSkull,
MeatOnTheBone, MercuryHourglass, BlackBlood, CaptainsWheel, Sundial, TungstenRod, RedMask,
Necronomicon, InkBottle, Pocketwatch, GremlinHorn, StoneCalendar, TheBoot, Duality,
BloodVial, FrozenCore, MutagenicStrength, IncenseBurner, SneckoEye, BirdFacedUrn

### Tier A: Simple Die-Roll / Passive (9) — fit existing hooks
| # | Relic | BG ID | Tier | Effect |
|---|-------|-------|------|--------|
| 1 | Akabeko | `BGAkabeko` | Common | Right-click: gain 1 Vigor (once/combat) |
| 2 | NilrysCodex | `BGNilry's Codex` | Common | Die 2: draw 1; Die 4: copy relic effect |
| 3 | DollysMirror | `BGDollysMirror` | Shop | Die 1: copy any die relic effect |
| 4 | TheAbacus | `BGTheAbacus` | Shop | Change die roll +1 (once/combat) |
| 5 | Toolbox | `BGToolbox` | Shop | Change die roll -1 (once/combat) |
| 6 | GamblingChip | `BGGambling Chip` | Rare | Reroll the die (once/combat) |
| 7 | CharonsAshes | `BGCharonsAshes` | Rare | Die 1-2: exhaust card + deal 2 damage |
| 8 | StrikeDummy | `BGStrikeDummy` | Uncommon | Starter Strikes deal +1 damage |
| 9 | WristBlade | `BGWristBlade` | Boss | 0-cost cards deal +1 damage |

- [ ] Implement Tier A relics (9)

### Tier B: Combat-Start / Passive Effects (10)
| # | Relic | BG ID | Tier | Effect |
|---|-------|-------|------|--------|
| 1 | RegalPillow | `BGRegal Pillow` | Common | Heal 3 extra HP when resting |
| 2 | Whetstone | `BGWhetstone` | Common | Right-click: upgrade 2 Attacks (one-time) |
| 3 | Omamori | `BGOmamori` | Common | Negate curses |
| 4 | RunicPyramid | `BGRunic Pyramid` | Common | Right-click: retain hand (once/combat) |
| 5 | BlueCandle | `BGBlue Candle` | Uncommon | Right-click: exhaust 2 cards (once/combat) |
| 6 | SelfFormingClay | `BGSelf Forming Clay` | Uncommon | After damage: right-click gain 3 Block (once/combat) |
| 7 | CentennialPuzzle | `BGCentennialPuzzle` | Uncommon | After damage: right-click draw 3 (once/combat) |
| 8 | MummifiedHand | `BGMummified Hand` | Uncommon | After Power: right-click gain 2 energy (once/combat) |
| 9 | Calipers | `BGCalipers` | Rare | Right-click: gain Blur (once/combat) |
| 10 | IceCream | `BGIce Cream` | Rare | Unused energy carries over |

- [ ] Implement Tier B relics (10)

### Tier C: Gold / Out-of-Combat (6)
| # | Relic | BG ID | Tier | Effect |
|---|-------|-------|------|--------|
| 1 | GoldenIdol | `BGGolden Idol` | Uncommon | +1 gold after combat |
| 2 | SsserpentHead | `BGSsserpentHead` | Uncommon | +2 gold at events |
| 3 | OldCoin | `BGOld Coin` | Rare | +10 gold when obtained |
| 4 | PeacePipe | `BGPeace Pipe` | Rare | Can remove card when resting |
| 5 | GoldenEye | `BGGoldenEye` | Rare | Right-click: Scry 3 (once/combat) |
| 6 | WingBoots | `BGWingedGreaves` | Rare | Skip 3 rooms on map |

- [ ] Implement Tier C relics (6)

### Tier D: Egg Relics / Card Upgrade (3)
| # | Relic | BG ID | Tier | Effect |
|---|-------|-------|------|--------|
| 1 | MoltenEgg2 | `BGMolten Egg 2` | Uncommon | Auto-upgrade 3 Attack cards on obtain |
| 2 | ToxicEgg2 | `BGToxic Egg 2` | Uncommon | Auto-upgrade 3 Skill cards on obtain |
| 3 | WarPaint | `BGWar Paint` | Rare | Right-click: upgrade 2 Skills (one-time) |

- [ ] Implement Tier D relics (3)

### Tier E: Boss Relics (15)
| # | Relic | BG ID | Effect |
|---|-------|-------|--------|
| 1 | Astrolabe | `BGAstrolabe` | Choose 3 cards to upgrade |
| 2 | CallingBell | `BGCalling Bell` | 3 random relics + 1 curse |
| 3 | CoffeeDripper | `BGCoffee Dripper` | +1 energy, can't rest |
| 4 | CursedKey | `BGCursed Key` | +1 energy, +2 curses |
| 5 | Ectoplasm | `BGEctoplasm` | +1 energy, can't gain gold |
| 6 | EmptyCage | `BGEmpty Cage` | Remove 2 cards |
| 7 | Enchiridion | `BGEnchiridion` | Choose 1 of 5 Rare cards |
| 8 | FusionHammer | `BGFusion Hammer` | +1 energy, can't upgrade at rest |
| 9 | HolyWater | `BGHolyWater` | Right-click: +1 energy (2 uses/combat) |
| 10 | MarkOfPain | `BGMarkOfPain` | +1 energy, max HP = 6 |
| 11 | NinjaScroll | `BGNinjaScroll` | Right-click: use 2 Shivs (once/combat) |
| 12 | Orrery | `BGOrrery` | Choose 1 of 3 card rewards |
| 13 | RingOfTheSerpent | `BGRing of the Serpent` | Draw +1 each turn, heal 2 at start |
| 14 | Sozu | `BGSozu` | +1 energy, can't get potions |
| 15 | TinyHouse | `BGTiny House` | Card + potion + 3 gold + upgrade |

- [ ] Implement Tier E boss relics (15)

### Tier F: Special / Niche (5)
| # | Relic | BG ID | Effect |
|---|-------|-------|--------|
| 1 | DuVuDoll | `BGDu-Vu Doll` | +1 temp Strength when drawing Curse |
| 2 | DeadBranch | `BGDead Branch` | Right-click: draw cards = exhaust pile size (once/combat) |
| 3 | PrismaticShard | `BGPrismaticShard` | +2 orb slots if not Defect |
| 4 | WhiteBeast | `BGWhite Beast Statue` | Reward screen in boss combats |
| 5 | SecretPortal | `BGSecretPortalRelic` | Secret portal ability |

- [ ] Implement Tier F relics (5)

### Right-Click Relic Infrastructure
Many BG mod relics use a "right-click to activate" mechanic (once per combat). This needs:
- [ ] Add `use_relic(relic_index)` action to combat interface
- [ ] Add `used_this_combat` tracking per relic
- [ ] Wire into combat loop as a player action choice

---

## Phase 4: Enemies — Act 2 (18 enemies)

### Normal Enemies (12)
| # | Enemy | BG ID | HP | Notes |
|---|-------|-------|----|-------|
| 1 | SnakePlant | `BGSnakePlant` | ? | |
| 2 | Centurion | `BGCenturion` | ? | Paired with Healer |
| 3 | ShelledParasite | `BGShelled Parasite` | ? | |
| 4 | Snecko | `BGSnecko` | ? | |
| 5 | SphericGuardian | `BGSphericGuardian` | ? | |
| 6 | Healer | `BGHealer` | ? | Paired with Centurion |
| 7 | BronzeOrb | `BGBronzeOrb` | ? | Paired with Automaton boss |
| 8 | TorchHead | `BGTorchHead` | ? | |
| 9 | Byrd | `BGByrd` | ? | Flight mechanic |
| 10 | Mugger | `Mugger` | ? | |
| 11 | Chosen | `BGChosen` | ? | |
| 12 | GremlinPlaceholder | `BGGremlinPlaceholder` | ? | Summoned gremlin |

### Elite Enemies (3)
| # | Enemy | BG ID | Notes |
|---|-------|-------|-------|
| 1 | BookOfStabbing | `BGBookOfStabbing` | Multi-stab attack |
| 2 | Taskmaster (Slavers) | `BGSlaverBoss` | Slavers boss fight |
| 3 | GremlinLeader | `BGGremlinLeader` | Summons gremlins |

### Bosses (3)
| # | Enemy | BG ID | Notes |
|---|-------|-------|-------|
| 1 | BronzeAutomaton | `BGBronzeAutomaton` | Summons Bronze Orbs |
| 2 | TheCollector | `TheCollector` | Summons Torch Heads |
| 3 | Champ | `BGChamp` | Phase-based (defensive/offensive) |

### Encounters to Define
- [ ] Act 2 normal encounter pool
- [ ] Act 2 elite encounters
- [ ] Act 2 boss encounters

### Implementation Checklist
- [ ] Implement Act 2 normal enemies (12)
- [ ] Implement Act 2 elites (3)
- [ ] Implement Act 2 bosses (3)
- [ ] Define Act 2 encounter table
- [ ] Add Act 2 enemy tests
- [ ] Add live enemy tests

---

## Phase 5: Enemies — Act 3 (17 enemies)

### Normal Enemies (10)
| # | Enemy | BG ID | Notes |
|---|-------|-------|-------|
| 1 | SpireGrowth | `BGSerpent` | |
| 2 | Darkling | `BGDarkling` | Revives unless all killed at once |
| 3 | OrbWalker | `BGOrb Walker` | |
| 4 | SnakeDagger | `BGSnakeDagger` | |
| 5 | WrithingMass | `BGWrithingMass` | Copies player's last action |
| 6 | Maw | `BGMaw` | |
| 7 | Spiker | `Spiker` | Thorns |
| 8 | Repulsor | `Repulsor` | Pushes cards to draw pile |
| 9 | Exploder | `Exploder` | Explodes after countdown |
| 10 | Transient | `BGTransient` | Fades after N turns |

### Elite Enemies (3)
| # | Enemy | BG ID | Notes |
|---|-------|-------|-------|
| 1 | Nemesis | `BGNemesis` | Goes intangible |
| 2 | GiantHead | `BGGiantHead` | Slow debuff |
| 3 | Reptomancer | `BGReptomancer` | Summons daggers |

### Bosses (4)
| # | Enemy | BG ID | Notes |
|---|-------|-------|-------|
| 1 | TimeEater | `BGTimeEater` | Punishes playing many cards |
| 2 | Deca | `BGDeca` | Half of Deca & Donu |
| 3 | Donu | `BGDonu` | Half of Deca & Donu |
| 4 | AwakenedOne | `BGAwakenedOne` | Phase 2 on death, punishes Powers |

### Implementation Checklist
- [ ] Implement Act 3 normal enemies (10)
- [ ] Implement Act 3 elites (3)
- [ ] Implement Act 3 bosses (4)
- [ ] Define Act 3 encounter table
- [ ] Add Act 3 enemy tests
- [ ] Add live enemy tests

---

## Phase 6: Enemies — Act 4 (3 enemies)

| # | Enemy | BG ID | Type | Notes |
|---|-------|-------|------|-------|
| 1 | SpireSpear | `BGSpireSpear` | Elite | Paired with Shield |
| 2 | SpireShield | `BGSpireShield` | Elite | Paired with Spear |
| 3 | CorruptHeart | `BGCorruptHeart` | Boss | The Heart, final boss |

- [ ] Implement Act 4 elite pair
- [ ] Implement The Heart
- [ ] Define Act 4 encounters

---

## Phase 7: Events — Remaining (~36 events)

9 events are implemented. The BG mod has 45+. Priority events for Act 1 and 2:

### High Priority (Act 1-2 events needed for full act progression)
- [ ] Survey all BG mod events and catalog by act
- [ ] Implement remaining Act 1 events
- [ ] Implement Act 2 events
- [ ] Implement Act 3 events

### Event Infrastructure
- [ ] Event selection/weighting system (which events appear in which acts)

---

## Phase 8: Shop Expansion

### Missing Shop Features
- [ ] Relic purchase (shop relics: DollysMirror, TheAbacus, Toolbox)
- [ ] Potion purchase (requires Phase 2 potion system)
- [ ] Proper pricing model

---

## Recommended Priority Order

Based on impact and dependencies:

1. **Phase 2: Potions** — New system, self-contained, needed for many relics
2. **Phase 3: Relics (Tier A-B)** — Die-roll and passive relics, ~19 relics
3. **Phase 1: Missing Cards** — Just 2 cards, quick win
4. **Phase 4: Act 2 Enemies** — Unlocks Act 2 gameplay
5. **Phase 3: Relics (Tier C-F)** — Remaining 29 relics
6. **Phase 5: Act 3 Enemies** — Unlocks Act 3
7. **Phase 6: Act 4 Enemies** — Unlocks full game
8. **Phase 7: Events** — More event variety
9. **Phase 8: Shop** — Quality of life

---

## Quick Reference: BG Mod Source Locations

```
Cards:    /data/code/StSBoardGameMod/src/main/java/BoardGame/cards/
Relics:   /data/code/StSBoardGameMod/src/main/java/BoardGame/relics/
Enemies:  /data/code/StSBoardGameMod/src/main/java/BoardGame/monsters/
Potions:  /data/code/StSBoardGameMod/src/main/java/BoardGame/potions/
Events:   /data/code/StSBoardGameMod/src/main/java/BoardGame/events/
```

## Build & Test

```bash
cd /data/code/sts_bot_2
.venv/bin/maturin develop --release && cp target/release/libsts_sim.so sts_sim.so
.venv/bin/python -m pytest tests/ -v                    # All unit tests
.venv/bin/python -m pytest tests/live/ -v               # All live tests (game required)
```
