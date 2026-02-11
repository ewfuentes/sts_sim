# Silent (BGGreen) — Basic

- **Strike** [Y] — BGStrike_G — Attack, Basic, Cost 1
  1 HIT.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic Strike deals 1 damage**
  Setup: Player has Strike in hand, 3 energy. Enemy has 10 HP, 0 block.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 1 HP (now 9 HP). Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Strike with Strength adds bonus damage per HIT**
  Setup: Player has Strike in hand, 3 energy, 2 STR. Enemy has 10 HP, 0 block.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 3 HP (1 HIT + 2 STR = 3 damage, now 7 HP).

  - [ ] Sim - [ ] Live — **Test: Upgraded Strike deals 2 HIT**
  Setup: Player has Strike+ in hand, 3 energy, 1 STR. Enemy has 10 HP, 0 block.
  Actions: Play Strike+ targeting enemy.
  Expected: Enemy loses 4 HP (2 HIT, each dealing 1+1 STR = 2 damage each, now 6 HP).

- **Defend** [Y] — BGDefend_G — Skill, Basic, Cost 1
  1 BLK.
  *Upgrade: 2 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Basic Defend grants 1 block to self**
  Setup: Player has Defend in hand, 3 energy, 0 block.
  Actions: Play Defend.
  Expected: Player gains 1 block. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] N/A — **Test: Upgraded Defend can assign 2 BLK to different players**
  Setup: Player has Defend+ in hand, 3 energy, 0 block. Ally has 0 block.
  Actions: Play Defend+, assign 1 BLK to self and 1 BLK to ally.
  Expected: Player gains 1 block. Ally gains 1 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded Defend can stack both BLK on self**
  Setup: Player has Defend+ in hand, 3 energy, 0 block.
  Actions: Play Defend+, assign both BLK to self.
  Expected: Player gains 2 block.

- **Neutralize** [Y] — BGNeutralize — Attack, Basic, Cost 0
  1 HIT 1 WEAK.
  *Upgrade: 2 HIT 1 WEAK.*

  - [ ] Sim - [ ] Live — **Test: Neutralize deals 1 damage and applies 1 Weak at zero cost**
  Setup: Player has Neutralize in hand, 3 energy. Enemy has 10 HP, 0 block, no debuffs.
  Actions: Play Neutralize targeting enemy.
  Expected: Enemy loses 1 HP (now 9 HP). Enemy gains 1 WEAK. Player energy remains 3.

  - [ ] Sim - [ ] Live — **Test: Neutralize with Strength**
  Setup: Player has Neutralize in hand, 1 STR. Enemy has 10 HP.
  Actions: Play Neutralize targeting enemy.
  Expected: Enemy loses 2 HP (1 HIT + 1 STR = 2 damage, now 8 HP). Enemy gains 1 WEAK.

  - [ ] Sim - [ ] Live — **Test: Upgraded Neutralize deals 2 HIT and applies 1 Weak**
  Setup: Player has Neutralize+ in hand, 1 STR. Enemy has 10 HP, no debuffs.
  Actions: Play Neutralize+ targeting enemy.
  Expected: Enemy loses 4 HP (2 HIT, each dealing 1+1 STR = 2 damage, now 6 HP). Enemy gains 1 WEAK.

- **Survivor** [Y] — BGSurvivor — Skill, Basic, Cost 1
  2 BLK. Discard 1 card.
  *Upgrade: 3 BLK. Discard 1 card.*

  - [ ] Sim - [ ] Live — **Test: Survivor grants 2 block and forces a discard**
  Setup: Player has Survivor and Strike in hand, 3 energy, 0 block.
  Actions: Play Survivor, discard Strike.
  Expected: Player gains 2 block. Strike moves to discard pile. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Survivor grants 3 block and forces a discard**
  Setup: Player has Survivor+ and Defend in hand, 3 energy, 0 block.
  Actions: Play Survivor+, discard Defend.
  Expected: Player gains 3 block. Defend moves to discard pile. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] N/A — **Test: Survivor discard triggers After Image**
  Setup: Player has Survivor and Strike in hand, 3 energy, 0 block. After Image power is active.
  Actions: Play Survivor, discard Strike.
  Expected: Player gains 2 block from Survivor. Player gains 1 block from After Image (triggered by discarding Strike). Total block = 3.
