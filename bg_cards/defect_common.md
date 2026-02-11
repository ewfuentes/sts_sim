# Defect (BGBlue) — Common

- **Ball Lightning** [Y] — BGBallLightning — Attack, Common, Cost 1
  1 HIT. Channel 1 Lightning.
  *Upgrade: 2 HIT. Channel 1 Lightning.*

  - [ ] Sim - [ ] Live — **Test: Ball Lightning deals 1 damage and channels Lightning**
  Setup: Player has 3 energy, Ball Lightning in hand, 0 orbs, 3 orb slots. Enemy has 20 HP.
  Actions: Play Ball Lightning targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player has 1 Lightning orb channeled. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Ball Lightning deals 2 damage**
  Setup: Player has 3 energy, Ball Lightning+ in hand, 0 orbs, 3 orb slots. Enemy has 20 HP.
  Actions: Play Ball Lightning+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player has 1 Lightning orb channeled.

  - [ ] Sim - [ ] Live — **Test: Ball Lightning with full orb slots evokes oldest orb**
  Setup: Player has 3 energy, Ball Lightning in hand, 3 orb slots all occupied by Frost orbs. Enemy has 20 HP.
  Actions: Play Ball Lightning targeting enemy.
  Expected: Enemy loses 1 HP. Leftmost Frost orb is evoked (player gains block). Lightning orb is channeled in the rightmost slot.

- **Barrage** [Y] — BGBarrage — Attack, Common, Cost 1
  Deal 1 HIT for each Orb you have.
  *Upgrade: Deal 1 HIT for each Orb you have +1.*

  - [ ] Sim - [ ] Live — **Test: Barrage deals hits equal to number of orbs**
  Setup: Player has 3 energy, Barrage in hand, 3 orbs channeled (Lightning, Frost, Dark). Enemy has 20 HP.
  Actions: Play Barrage targeting enemy.
  Expected: Enemy takes 3 hits of 1 damage each (17 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Barrage with no orbs deals no damage**
  Setup: Player has 3 energy, Barrage in hand, 0 orbs channeled. Enemy has 20 HP.
  Actions: Play Barrage targeting enemy.
  Expected: Enemy takes 0 hits. Enemy remains at 20 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Barrage deals one extra hit**
  Setup: Player has 3 energy, Barrage+ in hand, 2 orbs channeled (Lightning, Frost). Enemy has 20 HP.
  Actions: Play Barrage+ targeting enemy.
  Expected: Enemy takes 3 hits of 1 damage each (2 orbs + 1 = 3 hits, 17 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Barrage benefits from Strength on each hit**
  Setup: Player has 3 energy, Barrage in hand, 2 orbs channeled, 2 STR. Enemy has 20 HP.
  Actions: Play Barrage targeting enemy.
  Expected: Enemy takes 2 hits of 3 damage each (1 base + 2 STR per hit = 6 total, 14 HP remaining).

- **Beam Cell** [Y] — BGBeamCell — Attack, Common, Cost 0
  [1] [2] [3] 1 HIT VULN. [4] [5] [6] 1 HIT.
  *Upgrade: 1 HIT VULN. (Always applies VULN.)*

  - [ ] Sim - [ ] Live — **Test: Beam Cell applies Vulnerable on low die roll**
  Setup: Player has 3 energy, Beam Cell in hand. Die shows 2. Enemy has 20 HP, no debuffs.
  Actions: Play Beam Cell targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy gains VULN. Player still has 3 energy (cost 0).

  - [ ] Sim - [ ] Live — **Test: Beam Cell does not apply Vulnerable on high die roll**
  Setup: Player has 3 energy, Beam Cell in hand. Die shows 5. Enemy has 20 HP, no debuffs.
  Actions: Play Beam Cell targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy does not gain VULN.

  - [ ] Sim - [ ] Live — **Test: Upgraded Beam Cell always applies Vulnerable**
  Setup: Player has 3 energy, Beam Cell+ in hand. Die shows 6. Enemy has 20 HP, no debuffs.
  Actions: Play Beam Cell+ targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy gains VULN regardless of die roll.

- **Claw** [Y] — BGClaw — Attack, Common, Cost 0
  1 HIT. +1 damage if the topmost card in your discard pile costs 0.
  *Upgrade: +3 damage if the topmost card in your discard pile costs 0.*

  - [ ] Sim - [ ] Live — **Test: Claw deals base 1 damage when discard top is not cost 0**
  Setup: Player has 3 energy, Claw in hand. Discard pile topmost card is Defend (cost 1). Enemy has 20 HP.
  Actions: Play Claw targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Claw deals 2 damage when discard top is cost 0**
  Setup: Player has 3 energy, Claw in hand. Discard pile topmost card is another Claw (cost 0). Enemy has 20 HP.
  Actions: Play Claw targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 1 base + 1 bonus from cost-0 top of discard.

  - [ ] Sim - [ ] Live — **Test: Upgraded Claw deals 4 damage when discard top is cost 0**
  Setup: Player has 3 energy, Claw+ in hand. Discard pile topmost card is Beam Cell (cost 0). Enemy has 20 HP.
  Actions: Play Claw+ targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 1 base + 3 bonus from cost-0 top of discard.

  - [ ] Sim - [ ] Live — **Test: Claw bonus stacks with Strength**
  Setup: Player has 3 energy, Claw in hand, 2 STR. Discard pile topmost card is Claw (cost 0). Enemy has 20 HP.
  Actions: Play Claw targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 1 base HIT + 1 cost-0 bonus + 2 STR.

- **Compile Driver** [Y] — BGCompileDriver — Attack, Common, Cost 1
  1 HIT. Draw a card for each type of Orb you have.
  *Upgrade: 2 HIT. Draw a card for each type of Orb you have.*

  - [ ] Sim - [ ] Live — **Test: Compile Driver draws cards for each unique orb type**
  Setup: Player has 3 energy, Compile Driver in hand, 4 cards in hand. 3 orbs: Lightning, Frost, Lightning. Draw pile has 5 cards. Enemy has 20 HP.
  Actions: Play Compile Driver targeting enemy.
  Expected: Enemy loses 1 HP. Player draws 2 cards (2 unique orb types: Lightning and Frost). Player has 5 cards in hand.

  - [ ] Sim - [ ] Live — **Test: Compile Driver with no orbs draws nothing**
  Setup: Player has 3 energy, Compile Driver in hand, 4 cards in hand. 0 orbs channeled. Draw pile has 5 cards. Enemy has 20 HP.
  Actions: Play Compile Driver targeting enemy.
  Expected: Enemy loses 1 HP. Player draws 0 cards. Player has 4 cards in hand.

  - [ ] Sim - [ ] Live — **Test: Upgraded Compile Driver deals 2 damage**
  Setup: Player has 3 energy, Compile Driver+ in hand. 1 Dark orb channeled. Draw pile has 5 cards. Enemy has 20 HP.
  Actions: Play Compile Driver+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player draws 1 card (1 unique orb type: Dark).

- **Go for the Eyes** [Y] — BGGoForTheEyes — Attack, Common, Cost 0
  [1] [2] [3] 1 HIT. [4] [5] [6] 1 HIT WEAK.
  *Upgrade: 1 HIT WEAK. (Always applies WEAK.)*

  - [ ] Sim - [ ] Live — **Test: Go for the Eyes applies Weak on high die roll**
  Setup: Player has 3 energy, Go for the Eyes in hand. Die shows 4. Enemy has 20 HP, no debuffs.
  Actions: Play Go for the Eyes targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy gains WEAK. Player still has 3 energy (cost 0).

  - [ ] Sim - [ ] Live — **Test: Go for the Eyes does not apply Weak on low die roll**
  Setup: Player has 3 energy, Go for the Eyes in hand. Die shows 1. Enemy has 20 HP, no debuffs.
  Actions: Play Go for the Eyes targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy does not gain WEAK.

  - [ ] Sim - [ ] Live — **Test: Upgraded Go for the Eyes always applies Weak**
  Setup: Player has 3 energy, Go for the Eyes+ in hand. Die shows 2. Enemy has 20 HP, no debuffs.
  Actions: Play Go for the Eyes+ targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Enemy gains WEAK regardless of die roll.

- **Sweeping Beam** [Y] — BGSweepingBeam — Attack, Common, Cost 1
  AOE 1 HIT. Draw a card.
  *Upgrade: AOE 2 HIT. Draw a card.*

  - [ ] Sim - [ ] Live — **Test: Sweeping Beam hits all enemies and draws a card**
  Setup: Player has 3 energy, Sweeping Beam in hand, 4 cards in hand. 3 enemies each with 10 HP. Draw pile has 5 cards.
  Actions: Play Sweeping Beam.
  Expected: All 3 enemies each lose 1 HP (9 HP each). Player draws 1 card (5 cards in hand). Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Sweeping Beam deals 2 damage to all enemies**
  Setup: Player has 3 energy, Sweeping Beam+ in hand. 2 enemies each with 10 HP. Draw pile has 5 cards.
  Actions: Play Sweeping Beam+.
  Expected: Both enemies each lose 2 HP (8 HP each). Player draws 1 card.

  - [ ] Sim - [ ] Live — **Test: Sweeping Beam with Strength hits all enemies for boosted damage**
  Setup: Player has 3 energy, Sweeping Beam in hand, 3 STR. 2 enemies each with 20 HP.
  Actions: Play Sweeping Beam.
  Expected: Both enemies each lose 4 HP (16 HP each). 1 base HIT + 3 STR per enemy.

- **Charge Battery** [Y] — BGChargeBattery — Skill, Common, Cost 1
  2 BLK. Gain Energy(B) if you have 3 or more Orbs.
  *Upgrade: 3 BLK.*

  - [ ] Sim - [ ] Live — **Test: Charge Battery grants 2 block without enough orbs**
  Setup: Player has 3 energy, Charge Battery in hand, 0 block, 2 orbs channeled.
  Actions: Play Charge Battery.
  Expected: Player gains 2 block. Player has 2 energy. No bonus energy gained.

  - [ ] Sim - [ ] Live — **Test: Charge Battery grants block and energy with 3 orbs**
  Setup: Player has 3 energy, Charge Battery in hand, 0 block, 3 orbs channeled (Lightning, Frost, Dark).
  Actions: Play Charge Battery.
  Expected: Player gains 2 block. Player gains 1 Energy(B). Player has 3 energy (spent 1, gained 1 back).

  - [ ] Sim - [ ] Live — **Test: Upgraded Charge Battery grants 3 block**
  Setup: Player has 3 energy, Charge Battery+ in hand, 0 block, 1 orb channeled.
  Actions: Play Charge Battery+.
  Expected: Player gains 3 block. Player has 2 energy. No bonus energy (fewer than 3 orbs).

- **Chaos** [Y] — BGChaos — Skill, Common, Cost 1
  Channel the Orb the die is on. [1][2] Lightning [3][4] Frost [5][6] Dark.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Chaos channels Lightning on die roll 1 or 2**
  Setup: Player has 3 energy, Chaos in hand, 0 orbs, 3 orb slots. Die shows 2.
  Actions: Play Chaos.
  Expected: Player channels 1 Lightning orb. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Chaos channels Frost on die roll 3 or 4**
  Setup: Player has 3 energy, Chaos in hand, 0 orbs, 3 orb slots. Die shows 3.
  Actions: Play Chaos.
  Expected: Player channels 1 Frost orb. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Chaos channels Dark on die roll 5 or 6**
  Setup: Player has 3 energy, Chaos in hand, 0 orbs, 3 orb slots. Die shows 6.
  Actions: Play Chaos.
  Expected: Player channels 1 Dark orb. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Chaos costs 0**
  Setup: Player has 3 energy, Chaos+ in hand, 0 orbs, 3 orb slots. Die shows 4.
  Actions: Play Chaos+.
  Expected: Player channels 1 Frost orb. Player still has 3 energy.

- **Coolheaded** [Y] — BGCoolheaded — Skill, Common, Cost 1
  Channel 1 Frost.
  *Upgrade: Channel 1 Frost. Draw a card.*

  - [ ] Sim - [ ] Live — **Test: Coolheaded channels a Frost orb**
  Setup: Player has 3 energy, Coolheaded in hand, 0 orbs, 3 orb slots.
  Actions: Play Coolheaded.
  Expected: Player has 1 Frost orb channeled. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Coolheaded channels Frost and draws a card**
  Setup: Player has 3 energy, Coolheaded+ in hand, 4 cards in hand, 0 orbs, 3 orb slots. Draw pile has 5 cards.
  Actions: Play Coolheaded+.
  Expected: Player has 1 Frost orb channeled. Player draws 1 card (5 cards in hand). Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Coolheaded with full orb slots evokes oldest orb**
  Setup: Player has 3 energy, Coolheaded in hand, 3 orb slots all occupied by Lightning orbs. Enemy has 20 HP.
  Actions: Play Coolheaded.
  Expected: Leftmost Lightning orb is evoked (deals damage to random enemy). Frost orb is channeled in the rightmost slot.

- **Leap** [Y] — BGLeap — Skill, Common, Cost 1
  2 BLK to any player. You may switch rows with another player.
  *Upgrade: 3 BLK to any player. You may switch rows with another player.*

  - [ ] Sim - [ ] Live — **Test: Leap grants 2 block to self**
  Setup: Player has 3 energy, Leap in hand, 0 block.
  Actions: Play Leap targeting self. Decline row switch.
  Expected: Player gains 2 block. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Leap grants 2 block to an ally**
  Setup: Player has 3 energy, Leap in hand. Ally has 0 block.
  Actions: Play Leap targeting ally. Decline row switch.
  Expected: Ally gains 2 block. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Leap grants 3 block and allows row switch**
  Setup: Player has 3 energy, Leap+ in hand, 0 block. Player is in front row, ally is in back row.
  Actions: Play Leap+ targeting self. Choose to switch rows with ally.
  Expected: Player gains 3 block. Player moves to back row, ally moves to front row.

- **Recursion** [Y] — BGRecursion — Skill, Common, Cost 1
  Evoke 1 Orb. Channel the Orb that was just Evoked.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Recursion evokes and re-channels a Lightning orb**
  Setup: Player has 3 energy, Recursion in hand. 1 Lightning orb channeled, 3 orb slots. Enemy has 20 HP.
  Actions: Play Recursion.
  Expected: Lightning orb is evoked (deals damage to a random enemy). Then a new Lightning orb is channeled. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Recursion evokes Frost and re-channels it**
  Setup: Player has 3 energy, Recursion in hand. 1 Frost orb channeled, 3 orb slots, 0 block.
  Actions: Play Recursion.
  Expected: Frost orb is evoked (player gains block). Then a new Frost orb is channeled.

  - [ ] Sim - [ ] Live — **Test: Upgraded Recursion costs 0**
  Setup: Player has 3 energy, Recursion+ in hand. 1 Dark orb channeled, 3 orb slots. Enemy has 20 HP.
  Actions: Play Recursion+.
  Expected: Dark orb is evoked (deals stored damage to lowest HP enemy). Then a new Dark orb is channeled. Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Recursion with no orbs does nothing**
  Setup: Player has 3 energy, Recursion in hand, 0 orbs channeled.
  Actions: Play Recursion.
  Expected: No orb is evoked or channeled. Player has 2 energy.

- **Steam Barrier** [Y] — BGSteamBarrier — Skill, Common, Cost 0
  1 BLK. +1 BLK if the topmost card of your discard pile costs 0.
  *Upgrade: 2 BLK. +1 BLK if the topmost card of your discard pile costs 0.*

  - [ ] Sim - [ ] Live — **Test: Steam Barrier grants 1 block when discard top is not cost 0**
  Setup: Player has 3 energy, Steam Barrier in hand, 0 block. Discard pile topmost card is Defend (cost 1).
  Actions: Play Steam Barrier.
  Expected: Player gains 1 block. Player still has 3 energy (cost 0).

  - [ ] Sim - [ ] Live — **Test: Steam Barrier grants 2 block when discard top is cost 0**
  Setup: Player has 3 energy, Steam Barrier in hand, 0 block. Discard pile topmost card is Claw (cost 0).
  Actions: Play Steam Barrier.
  Expected: Player gains 2 block (1 base + 1 bonus). Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Steam Barrier grants 3 block when discard top is cost 0**
  Setup: Player has 3 energy, Steam Barrier+ in hand, 0 block. Discard pile topmost card is Beam Cell (cost 0).
  Actions: Play Steam Barrier+.
  Expected: Player gains 3 block (2 base + 1 bonus). Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Steam Barrier with empty discard pile grants only base block**
  Setup: Player has 3 energy, Steam Barrier in hand, 0 block. Discard pile is empty.
  Actions: Play Steam Barrier.
  Expected: Player gains 1 block. No bonus since discard pile is empty.
