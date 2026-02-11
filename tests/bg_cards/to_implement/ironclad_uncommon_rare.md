# Tests that cannot be live tests (require multi-turn, end_player_turn, or special mechanics)

## Ironclad Uncommon

### Carnage — Ethereal exhaust on end turn
- **Test: Carnage is exhausted if not played (Ethereal)** — Requires ending the turn without playing Carnage and verifying it moves to exhaust. Multi-turn test.

### Blood for Blood — Reduced cost after HP loss
- **Test: Blood for Blood costs 1 after losing HP** — Requires the player to have lost HP this combat, which means taking damage from an enemy attack (multi-turn).
- **Test: Upgraded Blood for Blood costs 0 after losing HP** — Same issue, requires HP loss tracking across turns.

### Flame Barrier — Retaliation on enemy attack
- **Test: Flame Barrier grants block and retaliates against attackers** — Requires ending the turn and having the enemy attack, then checking retaliation damage. Multi-turn.
- **Test: Flame Barrier does not retaliate against non-attacking enemies** — Same, requires ending the turn.
- **Test: Upgraded Flame Barrier grants 4 BLK** — Retaliation part requires end turn + enemy attack.

### Ghostly Armor — Ethereal exhaust on end turn
- **Test: Ghostly Armor is exhausted if not played (Ethereal)** — Requires ending the turn without playing. Multi-turn.

### Metallicize — End of turn block
- **Test: Metallicize grants 1 BLK at end of turn** — Requires end_player_turn to trigger the power.
- **Test: Metallicize triggers every turn** — Multi-turn test (multiple end turns).
- **Test: Upgraded Metallicize costs 0 energy** — The cost test is doable live, but verifying block at end of turn requires ending the turn.

### Power Through — Evolve interaction
- **Test: Power Through DAZED interacts with Evolve** — Requires drawing DAZED on a future turn. Multi-turn.

### Sentinel — Exhaust-triggered energy gain via another card
- **Test: Upgraded Sentinel grants 3 BLK and 3 energy on exhaust** — Requires playing Burning Pact to exhaust Sentinel+, which involves choice screens. Complex live interaction but potentially doable.

### Spot Weakness — Die manipulation
- **Test: Spot Weakness fails when die is on invalid face** — Requires setting die to 5 (set_scenario sets die=1 by default, and live die manipulation is limited).
- **Test: Upgraded Spot Weakness succeeds on die face [4]** — Requires setting die to 4.

### Combust — Activation mechanics
- **Test: Combust deals 1 damage once per turn** — Combust is a power with activation mechanics that differ from standard card play.
- **Test: Combust can only fire once per turn** — Multi-turn to test once-per-turn limit.
- **Test: Upgraded Combust deals 2 damage** — Same activation issue.

### Dark Embrace — Draw on exhaust
- **Test: Dark Embrace draws a card on exhaust** — Requires having Dark Embrace as an active power, then exhausting a card. Testable via Burning Pact + Dark Embrace power, but complex.
- **Test: Dark Embrace triggers for each card exhausted** — Same, requires Second Wind + Dark Embrace interaction.

### Evolve — Draw triggers
- **Test: Evolve triggers when drawing a DAZED** — Requires drawing a DAZED from draw pile (multi-turn or card draw effect with specific draw pile ordering).
- **Test: Evolve triggers on BURN and SLIMED as well** — Same draw-trigger issue.

### Feel No Pain — Block on exhaust
- **Test: Feel No Pain grants block on exhaust** — Requires having Feel No Pain power active and exhausting a card. Testable but complex.
- **Test: Feel No Pain triggers for each card exhausted** — Requires Second Wind + Feel No Pain power interaction.

### Fire Breathing — Damage on draw
- **Test: Fire Breathing deals damage when drawing a status card** — Requires drawing a status card from the draw pile (multi-turn).
- **Test: Fire Breathing triggers on Curse cards** — Same draw-trigger issue.
- **Test: Upgraded Fire Breathing deals 3 damage** — Same.

### Burning Pact — Dark Embrace synergy
- **Test: Burning Pact synergy with exhaust-trigger powers** — Requires Dark Embrace power active. Complex setup but potentially doable.

## Ironclad Rare

### Barricade — Block retention across turns
- **Test: Barricade retains block between turns** — Requires ending the turn and starting the next turn to verify block persists. Multi-turn.
- **Test: Barricade respects 20 BLK cap** — Block cap is testable within a turn, but retention requires multi-turn.

### Berserk — Damage on exhaust
- **Test: Berserk deals damage when a card is exhausted** — Requires Berserk as active power + exhausting via Burning Pact. Complex row-targeting.
- **Test: Berserk triggers for each card exhausted** — Same, requires Second Wind + Berserk power.
- **Test: Upgraded Berserk deals 2 damage per exhaust** — Same.

### Corruption — Skills cost 0 and exhaust
- **Test: Corruption makes Skills cost 0 and exhaust them** — Requires Corruption power active, then playing a Skill. Two-card sequence.
- **Test: Corruption does not affect Attacks** — Requires verifying an Attack still costs energy with Corruption active.
- **Test: Corruption exhausts Skills even if they normally would not exhaust** — Same multi-card sequence.

### Demon Form — STR at start of turn
- **Test: Demon Form grants STR at start of each turn** — Multi-turn (play, end turn, start next turn).
- **Test: Demon Form STR accumulates over multiple turns** — Requires multiple turn cycles.

### Double Tap — Next Attack doubled
- **Test: Double Tap only affects the next Attack, not subsequent ones** — Requires playing 3 cards in sequence (Double Tap + 2 Strikes). Complex but doable.

### Exhume — Retrieve from exhaust pile
- **Test: Exhume retrieves a card from exhaust pile** — Requires a non-empty exhaust pile, which means exhausting a card first. Complex setup.
- **Test: Exhume with empty exhaust pile** — Simpler, but Exhume's choice screen with empty pile may behave unexpectedly.
- **Test: Upgraded Exhume costs 0 energy** — Same exhaust pile setup issue.

### Feed — Kill-based STR
- **Test: Feed deals damage and gains STR on kill** — Requires the enemy to die from Feed's damage (3 HP enemy). Killing the last enemy ends combat, making post-assertion impossible in live tests.
- **Test: Upgraded Feed grants 2 STR on kill** — Same combat-ending issue.

### Juggernaut — Multiple triggers
- **Test: Juggernaut triggers on each source of block gain** — Requires playing 2 Defends in sequence with Juggernaut active. Multi-card sequence.
- **Test: Upgraded Juggernaut deals 2 damage per block gain** — Same but with upgraded power amount.
