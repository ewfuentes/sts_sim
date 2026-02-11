# Defect Basic & Common — Tests That Cannot Be Live Tests

These test scenarios require mechanics not easily testable via the live
set_scenario + play_card_both pattern (e.g. multi-player / ally targeting,
row switching, die manipulation mid-scenario, or multi-enemy setups that
require specific encounter types).

## Defect Basic

### Defend (Blue)

- **Upgraded Defend grants 2 block to any player**
  Requires an ally player target. The live test harness only supports
  single-player scenarios (no ally targeting via set_scenario).

### Zap

- **Zap evokes oldest orb when orb slots are full** (partially covered)
  The live test covers the play, but verifying the evoked Frost orb's block
  gain independently is hard because the evoked block amount depends on Focus
  and is added to player block alongside any existing block. The sim test
  checks orb list contents directly.

### Dualcast

- **Dualcast evokes Frost orb twice for double block** (partially covered)
  The live test verifies player block matches sim, but cannot independently
  verify the orb was evoked exactly twice vs. some other source of block.

- **Upgraded Dualcast costs 0** (partially covered)
  Dark orb evoke targets lowest-HP enemy. With a single monster this is
  deterministic, but the stored damage amount depends on turn count. The live
  test verifies HP/energy match between live and sim, but the absolute values
  depend on Dark orb state.

## Defect Common

### Beam Cell

- **Beam Cell does not apply Vulnerable on high die roll**
  Requires setting the die to 5 or 6 before playing. set_scenario always
  sets die=1. A custom die-setting mechanism would be needed. Only the
  sim test can verify this.

### Go for the Eyes

- **Go for the Eyes applies Weak on high die roll**
  Requires die=4 or higher. Same limitation as Beam Cell above. Only the
  sim test can verify this.

### Chaos

- **Chaos channels Frost on die roll 3 or 4**
  Requires die=3 or die=4. set_scenario sets die=1 (Lightning). Only the
  sim test covers Frost and Dark outcomes.

- **Chaos channels Dark on die roll 5 or 6**
  Requires die=5 or die=6. Same limitation.

### Sweeping Beam

- **Sweeping Beam hits all enemies and draws a card** (multi-enemy)
  The full 3-enemy version requires a specific encounter. The live test uses
  the default single-monster encounter and verifies damage + draw on that one
  monster. The sim test covers the 3-enemy scenario.

### Leap

- **Leap grants 2 block to an ally**
  Requires ally targeting. Not supported by set_scenario.

- **Upgraded Leap grants 3 block and allows row switch**
  Requires row-switching mechanics and ally targeting. Not supported by
  set_scenario.
