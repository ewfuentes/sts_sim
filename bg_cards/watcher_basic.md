# Watcher (BGPurple) — Basic

- **Strike** [Y] — BGStrike_W — Attack, Basic, Cost 1
  1 HIT.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic Strike deals 1 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Strike in Wrath deals double damage**
  Setup: Player in Wrath stance, 3 energy. Enemy has 20 HP.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining) because Wrath doubles damage dealt.

  - [ ] Sim - [ ] Live — **Test: Upgraded Strike deals 2 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Strike is upgraded.
  Actions: Play Strike+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Strike with Strength adds damage per HIT**
  Setup: Player in Neutral stance, 3 energy, 2 Strength. Enemy has 20 HP.
  Actions: Play Strike targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). Strength adds +1 per HIT, so 1 HIT = 1 base + 2 Strength = 3 damage.

- **Defend** [Y] — BGDefend_W — Skill, Basic, Cost 1
  1 BLK.
  *Upgrade: 2 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Basic Defend grants 1 block**
  Setup: Player in Neutral stance, 3 energy, 0 block.
  Actions: Play Defend.
  Expected: Player gains 1 block. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Defend grants 2 block to any player**
  Setup: Player in Neutral stance, 3 energy, 0 block. Defend is upgraded.
  Actions: Play Defend+ targeting self.
  Expected: Player gains 2 block. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Defend in Wrath still grants normal block**
  Setup: Player in Wrath stance, 3 energy, 0 block.
  Actions: Play Defend.
  Expected: Player gains 1 block. Wrath does not affect block gained.

- **Eruption** [Y] — BGEruption — Attack, Basic, Cost 2
  2 HIT. Enter Wrath.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Basic Eruption deals 2 damage and enters Wrath**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP.
  Actions: Play Eruption targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player enters Wrath stance. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Eruption from Calm grants 2 energy on exit then enters Wrath**
  Setup: Player in Calm stance, 3 energy. Enemy has 20 HP.
  Actions: Play Eruption targeting enemy.
  Expected: Player leaves Calm (gains 2 energy, going to 3 after spending 2), enters Wrath. Enemy loses 2 HP (18 HP remaining). Player ends with 3 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Eruption costs 1 energy**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Eruption is upgraded.
  Actions: Play Eruption+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player enters Wrath. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Eruption while already in Wrath deals double damage**
  Setup: Player in Wrath stance, 3 energy. Enemy has 20 HP.
  Actions: Play Eruption targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 2 HIT at base, doubled by Wrath = 4 damage. Player remains in Wrath.

- **Vigilance** [Y] — BGVigilance — Skill, Basic, Cost 2
  2 BLK to any player. Enter Calm.
  *Upgrade: 3 BLK to any player. Enter Calm.*

  - [ ] Sim - [ ] Live — **Test: Basic Vigilance grants 2 block and enters Calm**
  Setup: Player in Neutral stance, 3 energy, 0 block.
  Actions: Play Vigilance targeting self.
  Expected: Player gains 2 block. Player enters Calm stance. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Vigilance grants 3 block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Vigilance is upgraded.
  Actions: Play Vigilance+ targeting self.
  Expected: Player gains 3 block. Player enters Calm stance. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Vigilance from Wrath exits Wrath and enters Calm**
  Setup: Player in Wrath stance, 3 energy, 0 block.
  Actions: Play Vigilance targeting self.
  Expected: Player gains 2 block. Player leaves Wrath and enters Calm. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Vigilance while already in Calm stays in Calm**
  Setup: Player in Calm stance, 3 energy, 0 block.
  Actions: Play Vigilance targeting self.
  Expected: Player gains 2 block. Player remains in Calm (no stance change, so no energy gain from leaving Calm). Player spends 2 energy (1 remaining).
