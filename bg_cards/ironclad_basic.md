# Ironclad (BGRed) — Basic

- **Strike** [Y] — BGStrike_R — Attack, Basic, Cost 1
  1 HIT.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Base Strike deals 1 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Strike in hand.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Strike with Strength adds +1 damage per HIT**
  Setup: Player has 3 energy, 2 STR. Enemy has 20 HP, 0 block. Strike in hand.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). 1 HIT base + 2 STR = 3 damage.

  - [ ] Sim - [ ] Live — **Test: Upgraded Strike deals 2 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Strike+ in hand.
  Actions: Play Strike+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 2 HIT = 2 damage.

- **Defend** [Y] — BGDefend_R — Skill, Basic, Cost 1
  1 BLK.
  *Upgrade: 2 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Base Defend grants 1 block**
  Setup: Player has 3 energy, 0 block. Defend in hand.
  Actions: Play Defend.
  Expected: Player gains 1 block. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Defend grants 2 block to any player**
  Setup: Player has 3 energy, 0 block. Defend+ in hand. Ally player has 0 block.
  Actions: Play Defend+ targeting ally player.
  Expected: Ally player gains 2 block. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Block from Defend is removed at start of next turn**
  Setup: Player has 3 energy, 0 block. Defend in hand.
  Actions: Play Defend. End turn. Start next turn.
  Expected: After playing Defend, player has 1 block. At start of next turn, block resets to 0.

- **Bash** [Y] — BGBash — Attack, Basic, Cost 2
  2 HIT VULN.
  *Upgrade: 4 HIT VULN.*

  - [ ] Sim - [ ] Live — **Test: Base Bash deals 2 damage and applies Vulnerable**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block, no debuffs. Bash in hand.
  Actions: Play Bash targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Enemy gains 1 VULN. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Bash deals 4 damage and applies Vulnerable**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block, no debuffs. Bash+ in hand.
  Actions: Play Bash+ targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). Enemy gains 1 VULN. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Bash with Strength scales per HIT**
  Setup: Player has 3 energy, 1 STR. Enemy has 20 HP, 0 block. Bash in hand.
  Actions: Play Bash targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 2 HIT each gaining +1 from STR = (1+1) + (1+1) = 4 damage. Enemy gains 1 VULN.
