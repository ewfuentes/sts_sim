# Watcher Uncommon & Rare — Tests Needing Implementation / Not Live-Testable

This file tracks tests from the watcher_uncommon.md and watcher_rare.md
specs that cannot be written as single-turn live tests, require missing
simulator APIs, or involve cards not yet implemented in the simulator.

---

## Not in Simulator (marked [N])

- **Talk to the Hand** — All tests skipped in both sim and live.
  The card is marked [N] and has no simulator implementation.
  - Deal damage and gain block from Miracles
  - No Miracles means no block
  - Upgraded version deals 3 HIT with Miracle block

---

## Multi-Turn Tests (cannot be live-tested in single-turn set_scenario)

These tests require ending a turn and starting a new one, which the
current live test harness (set_scenario + play_card) does not support.

### Uncommon

- **Sands of Time — Retain keyword keeps card in hand at end of turn**
  Requires ending turn and verifying the card remains in hand.

- **Windmill Strike — Bonus damage after being Retained**
  Requires retaining the card one turn, then playing it next turn.

- **Windmill Strike — Upgraded version after being Retained**
  Same as above with upgraded version.

- **Perseverance — Bonus block after being Retained**
  Requires retaining the card one turn, then playing it next turn.

- **Perseverance — Upgraded version with Retain bonus**
  Same as above with upgraded version.

- **Wreath of Flame — Temporary Strength is lost at end of turn**
  Requires ending the turn to verify Strength loss.

- **Wreath of Flame — Upgraded version does not Exhaust**
  Can test play (goes to discard), but verifying end-of-turn Strength
  loss requires multi-turn.

- **Battle Hymn — Basic passive damage from Neutral**
  Requires ending turn to trigger power effect.

- **Battle Hymn — Wrath bonus doubles the passive damage**
  Requires triggering power at end of turn.

- **Battle Hymn — Upgraded version deals more base and Wrath damage**
  Requires triggering power at end of turn.

- **Simmering Fury — Bonus damage per HIT in Wrath**
  Requires playing a separate attack card while power is active.
  (Partially testable; needs careful hand setup.)

- **Simmering Fury — No bonus in Neutral stance**
  Same as above.

- **Simmering Fury — Upgraded version adds +2 per HIT in Wrath**
  Same as above.

- **Mental Fortress — Multiple stance switches accumulate block**
  Requires multiple stance changes in one turn (partially testable
  with careful hand setup).

- **Mental Fortress — Upgraded version grants 2 block per switch**
  Same as above.

- **Nirvana — Gain block when Scrying** / **Multiple Scrys** / **Upgraded**
  Requires playing Scry cards with Nirvana power active.
  Partially testable with careful hand setup.

- **Like Water — Gain block at end of turn in Calm**
  Requires ending turn to trigger power.

- **Like Water — No block if not in Calm** / **Upgraded**
  Same as above.

- **Foresight — Scry at start of turn** / **Upgraded** / **Nirvana interaction**
  Requires starting a new turn to trigger power.

- **Study — Draw 2 in Calm at start of turn** / **No extra draw if not in Calm**
  Requires starting a new turn to trigger power.

- **Rushdown — Only triggers once per turn**
  Requires multiple stance changes; partially testable.

- **Pray — Draw lock prevents further draws this turn**
  Requires playing two cards in sequence; partially testable.

- **Prostrate — Miracle can be spent for energy**
  Requires playing a Miracle card after Prostrate.

- **Meditate — Retrieved card retains into next turn**
  Requires ending turn and verifying retain.

- **Meditate — Upgraded version retrieves 2 cards**
  Requires choice interaction with discard pile.

### Rare

- **Blasphemy — Next Attack plays 3 times**
  Requires playing two cards in sequence; complex interaction.

- **Blasphemy — Draw pile is fully exhausted**
  Requires playing two cards and verifying exhaust pile.

- **Blasphemy — Upgraded version has Retain**
  Requires ending turn to verify Retain.

- **Deus Ex Machina — Miracles usable for energy after playing**
  Requires spending Miracle cards after playing.

- **Omniscience — Search and play an Attack twice**
  Requires choice screen interaction with draw pile search.

- **Omniscience — Search and play a Skill twice** / **Upgraded**
  Same as above.

- **Scrawl — Draw pile has fewer than 5 cards**
  Requires shuffle mechanic; partially testable.

- **Vault — Discard non-Retain cards, draw 5, gain 3 energy**
  Complex hand manipulation; partially testable.

- **Vault — Retain cards stay in hand** / **Upgraded**
  Same as above.

- **Wish — Choose Miracles** / **Upgraded Strength option**
  Choice interactions; partially testable (Strength choice is tested).

- **Judgment — Kill enemy at or below 7 HP**
  Requires enemy at exactly 7 HP (partially testable with set_scenario).

- **Judgment — Ethereal causes exhaust if not played**
  Requires ending turn without playing.

- **Judgment — Upgraded version kills at 8 HP and has Retain**
  Requires multi-turn to test Retain + kill.

- **Worship — Spend 0 energy still gives 1 Miracle**
  Requires 0 energy setup (partially testable).

- **Worship — Upgraded version has Retain**
  Requires ending turn to verify Retain.

- **Omega — Deal 5 damage at end of turn** / **Triggers every turn** / **Upgraded**
  Requires ending turn to trigger power.

- **Deva Form — All tests**
  Requires starting new turn to trigger power.

- **Devotion — All tests**
  Requires starting new turn and multi-turn tracking.

- **Establishment — All tests**
  Requires retaining cards and starting new turn.

- **Conjure Blade — Strikes deal extra damage**
  Requires playing power then Strike in sequence; partially testable.

- **Conjure Blade — Spend 0 energy gives +1** / **Upgraded**
  Same as above.

---

## Missing Simulator APIs

- **sim.get_stance()** — May not exist. Needed to verify stance transitions
  (Wrath, Calm, Neutral, Divinity) directly. Tests currently infer stance
  from damage multipliers and energy gains.

- **Scry mechanics** — Weave auto-play during Scry, Foresight start-of-turn
  Scry, Nirvana block on Scry. These require the simulator to model the
  Scry interaction fully.

- **Miracle count API** — No direct way to query Miracle count. Tests
  infer from hand contents (Miracle cards in hand).

- **Foreign Influence copy mode** — The "copy another player's Attack"
  mode is a multiplayer-only mechanic and cannot be tested in single-player.

---

## Partially Testable (in sim only, no live match)

Some tests can be written as sim-only tests but cannot have live
counterparts because the live harness does not support:
- Ending turns and starting new ones
- Complex multi-card sequences within set_scenario
- Power trigger verification at end/start of turn
