# Defect (BGBlue) — Basic

- **Strike** [Y] — BGStrike_B — Attack, Basic, Cost 1
  1 HIT.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Strike deals 1 damage**
  Setup: Player has 3 energy, Strike in hand. Enemy has 20 HP.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Strike benefits from Strength**
  Setup: Player has 3 energy, Strike in hand, 2 STR. Enemy has 20 HP.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). 1 base HIT + 2 from STR.

  - [ ] Sim - [ ] Live — **Test: Upgraded Strike costs 0**
  Setup: Player has 3 energy, Strike+ in hand. Enemy has 20 HP.
  Actions: Play Strike+ targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player still has 3 energy.

- **Defend** [Y] — BGDefend_B — Skill, Basic, Cost 1
  1 BLK.
  *Upgrade: 2 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Basic Defend grants 1 block**
  Setup: Player has 3 energy, Defend in hand, 0 block.
  Actions: Play Defend.
  Expected: Player gains 1 block. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Defend grants 2 block to any player**
  Setup: Player has 3 energy, Defend+ in hand, 0 block. Ally has 0 block.
  Actions: Play Defend+ targeting ally.
  Expected: Ally gains 2 block. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Defend block stacks with existing block**
  Setup: Player has 3 energy, Defend in hand, 3 block.
  Actions: Play Defend.
  Expected: Player has 4 block total.

- **Zap** [Y] — BGZap — Skill, Basic, Cost 1
  Channel 1 Lightning.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Zap channels a Lightning orb**
  Setup: Player has 3 energy, Zap in hand, 0 orbs, 3 orb slots.
  Actions: Play Zap.
  Expected: Player has 1 Lightning orb channeled. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Zap evokes oldest orb when orb slots are full**
  Setup: Player has 3 energy, Zap in hand, 3 orb slots all occupied by Frost orbs.
  Actions: Play Zap.
  Expected: Leftmost Frost orb is evoked (player gains block from evoke). Lightning orb is channeled in the rightmost slot.

  - [ ] Sim - [ ] Live — **Test: Upgraded Zap costs 0**
  Setup: Player has 3 energy, Zap+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Zap+.
  Expected: Player has 1 Lightning orb channeled. Player still has 3 energy.

- **Dualcast** [Y] — BGDualcast — Skill, Basic, Cost 1
  Evoke an Orb twice.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Dualcast evokes Lightning orb twice for double damage**
  Setup: Player has 3 energy, Dualcast in hand. 1 Lightning orb channeled. Enemy has 20 HP.
  Actions: Play Dualcast.
  Expected: Lightning orb is evoked twice, dealing its evoke damage to a random enemy two times. Player has 2 energy.

  - [ ] Sim - [ ] Live — **Test: Dualcast evokes Frost orb twice for double block**
  Setup: Player has 3 energy, Dualcast in hand, 0 block. 1 Frost orb channeled.
  Actions: Play Dualcast.
  Expected: Frost orb is evoked twice. Player gains block from two Frost evocations.

  - [ ] Sim - [ ] Live — **Test: Upgraded Dualcast costs 0**
  Setup: Player has 3 energy, Dualcast+ in hand. 1 Dark orb channeled. Enemy has 20 HP.
  Actions: Play Dualcast+.
  Expected: Dark orb is evoked twice, dealing its stored damage to the enemy with lowest HP two times. Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Dualcast with no orbs does nothing**
  Setup: Player has 3 energy, Dualcast in hand, 0 orbs channeled.
  Actions: Play Dualcast.
  Expected: No orb is evoked. Player has 2 energy. No other effect occurs.
