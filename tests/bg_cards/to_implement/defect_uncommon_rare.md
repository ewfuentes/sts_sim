# Defect Uncommon & Rare — Tests Requiring Special Implementation

These tests cannot be straightforwardly implemented as single-action live tests
because they require multi-turn sequences, enemy attack resolution, ally targeting,
or game states that cannot be set up via `set_scenario` alone.

## Uncommon Cards

### Blizzard
- **Blizzard with Strength** — Requires setting player Strength via powers, then
  verifying per-HIT Strength bonus on AOE multi-hit. Sim-only for now (Strength
  interaction with multi-hit AOE).

### FTL
- **FTL not first card of turn** — Requires playing a card first, then FTL second.
  Multi-action live test: play Strike, then FTL. Need to verify no draw on second
  card. Can be done live but requires two `play_card` calls in sequence.

### Scrape
- **Scrape with non-zero cost card on top of discard** — Requires discard pile top
  card to be non-zero cost. The set_scenario discard ordering may not be
  deterministic for "top" card semantics.

### Streamline
- **Streamline cost reduction with 2 powers** — Requires having 2 powers already in
  play. Multi-step: play 2 powers first, then Streamline. Needs 3+ actions in one test.

### Sunder
- **Sunder kills enemy and refunds energy** — Monster must die to trigger refund.
  Requires very low HP monster (4 HP). If the encounter has multiple monsters, the
  test must handle combat not ending on kill.
- **Upgraded Sunder kills enemy** — Same issue, needs low HP monster.

### Equilibrium
- **Equilibrium retain interaction** — Requires ending turn and verifying retained
  cards persist into next turn. Multi-turn live test with `end_turn` + verify hand
  next turn.
- **Upgraded Equilibrium retains 2 cards** — Same multi-turn requirement plus
  choose-2-cards interaction.

### Force Field
- **Force Field with no powers (unplayable)** — Negative test: verify card cannot be
  played. Hard to test in live (no error returned, just command rejected).
- **Force Field with 4+ powers costs 0** — Requires 4 powers in play before playing
  Force Field. Multi-step setup.

### Glacier
- **Upgraded Glacier targeting ally** — Requires ally present in game. Not supported
  by current set_scenario (single-player only).

### Hologram
- **Hologram with empty discard** — When discard is empty, Hologram may have no
  choice screen. Behavior may differ between sim/live.

### Recycle
- **Recycle a 2-cost card** — Requires choice screen to select which card to exhaust.
  Can be done live with `choices=[idx]`.
- **Recycle a 0-cost card** — Same choice screen requirement.
- **Recycle an X-cost card doubles energy** — Same, plus X-cost card handling.
- **Upgraded Recycle costs 0** — Same choice screen requirement.

### Reinforced Body
- **Reinforced Body X can't be 0** — Negative test: verify cannot be played with
  X=0. Hard to test in live.
- **Reinforced Body spending 3 energy (X=3)** — X-cost choice screen handling.
- **Upgraded Reinforced Body applies block twice** — X-cost choice.

### Capacitor
- **Capacitor allows more orbs** — Multi-step: play Capacitor, then channel an orb.
  Requires verifying orb slots expanded.

### Consume
- **Consume boosts Lightning/Frost evoke** — Multi-step: play Consume, then force
  evoke by channeling into full orb slots. Complex interaction test.

### Fusion / Machine Learning / Storm
- **Multi-turn power effects** — Requires ending turn and starting next turn to see
  start-of-turn triggers. Multi-turn live tests need careful state tracking.
- **Multiple Fusions stack** — Requires 2 Fusions in play, multi-turn.
- **Multiple Machine Learnings stack** — Same.

### Heatsinks
- **Heatsinks triggers on playing a power** — Multi-step: Heatsinks must be in play,
  then play a power card. Verify draw count increased.
- **Heatsinks does not trigger on non-power cards** — Same setup, play attack instead.
- **Upgraded Heatsinks draws 3** — Same with upgraded variant.

### Loop
- **All Loop tests** — End-of-turn orb trigger tests require ending turn and
  observing orb passive effects. Multi-turn live tests.

### Stack
- **Stack targeting an ally** — Requires ally present. Not supported by current
  set_scenario.

### TURBO
- **TURBO does not exceed energy cap** — Requires 5 starting energy, may need special
  energy setup.

## Rare Cards

### Core Surge
- **Core Surge retains between turns** — Multi-turn: end turn without playing, verify
  card remains in hand.
- **Upgraded Core Surge removes debuffs from all players** — Requires ally present.

### Meteor Strike
- **Meteor Strike with no powers (unplayable)** — Negative test.
- **Meteor Strike with 3 powers** — Multi-step: play 3 powers first.
- **Upgraded Meteor Strike with 5 powers (free)** — Requires 5 powers in play.
- **Meteor Strike with Strength** — Requires 5 energy + Strength.

### Amplify
- **Amplify boosts Dark orb evoke** — Multi-step: play Amplify, then force Dark evoke.
- **Upgraded Amplify boosts by +5** — Same.
- **Amplify does not affect non-Dark evokes** — Same, with Lightning orb.

### Multi-Cast
- **All Multi-Cast tests** — X-cost card with orb evoke interaction. Requires choice
  screen for X value and orb evoke verification.

### Tempest
- **Tempest with X=3** — X-cost choice screen plus orb channel verification.
- **Tempest with X=0** — 0 energy edge case.
- **Upgraded Tempest with X=2 channels 3** — X+1 channel verification.
- **Tempest overflows orb slots** — Complex: X=3 with 2 existing Frost orbs, causes
  evoke chain.

### Seek
- **All Seek tests** — Choice screen to select card(s) from draw pile.

### Buffer
- **Buffer prevents damage** — Multi-turn: play Buffer, end turn, enemy attacks.
  Requires enemy intent control.
- **Buffer does not prevent block loss** — Same, with block present.
- **Upgraded Buffer prevents twice** — Two enemy attacks required.

### Defragment
- **Defragment boosts orb passive** — Multi-turn: play Defragment, end turn, verify
  boosted orb passive.
- **Defragment is Ethereal** — End turn without playing, verify exhausted.
- **Upgraded Defragment not Ethereal** — End turn, verify goes to discard.
- **Defragment boosts Frost passive** — Same as above but with Frost orb.

### Echo Form
- **Echo Form doubles first attack** — Multi-turn: must be in play from previous
  turn, then play attack and verify doubled.
- **Echo Form does not double second card** — Same, play two cards.
- **Echo Form is Ethereal** — End turn without playing.
- **Upgraded Echo Form not Ethereal** — End turn, verify discard.

### Electrodynamics
- **Electrodynamics makes Lightning hit any row** — End turn with Lightning orb to
  verify AOE behavior. Complex interaction test.

### Static Discharge
- **Static Discharge boosts Lightning passive** — Multi-turn: play power, end turn,
  verify boosted Lightning passive damage.
- **Static Discharge does not affect Frost** — Same, with Frost orb.
- **Upgraded Static Discharge boosts by +2** — Same with upgraded.
