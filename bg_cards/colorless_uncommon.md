# Colorless — Uncommon

- **Dark Shackles** [N] — BGDarkShackles — Skill, Uncommon, Cost 0
  2 BLK for each enemy that intends to attack you. Exhaust.
  *Upgrade: 3 BLK for each enemy that intends to attack you. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic — gain block based on attacking enemies**
  Setup: Player has 0 block, 3 energy. Dark Shackles in hand. 2 enemies intend to attack the player.
  Actions: Play Dark Shackles.
  Expected: Player gains 4 block (2 BLK x 2 attacking enemies). Dark Shackles is exhausted. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: No enemies intending to attack**
  Setup: Player has 0 block. Dark Shackles in hand. 2 enemies, both intending to buff (not attack).
  Actions: Play Dark Shackles.
  Expected: Player gains 0 block (2 BLK x 0 attacking enemies). Dark Shackles is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded — 3 block per attacking enemy**
  Setup: Player has 0 block. Dark Shackles+ in hand. 3 enemies all intend to attack the player.
  Actions: Play Dark Shackles+.
  Expected: Player gains 9 block (3 BLK x 3 attacking enemies). Dark Shackles+ is exhausted.

- **Dramatic Entrance** [N] — BGDramatic Entrance — Attack, Uncommon, Cost 0
  AOE 2 HIT. +1 damage if it's the first turn of combat. Exhaust.
  *Upgrade: +3 damage if it's the first turn of combat.*

  - [ ] Sim - [ ] Live — **Test: Basic — AOE damage on first turn**
  Setup: First turn of combat. Player has 3 energy. Dramatic Entrance in hand. Enemy A has 10 HP, Enemy B has 8 HP. Both have 0 block.
  Actions: Play Dramatic Entrance.
  Expected: Enemy A takes 3 damage (2 HIT + 1 bonus = 3, now 7 HP). Enemy B takes 3 damage (now 5 HP). Dramatic Entrance is exhausted.

  - [ ] Sim - [ ] Live — **Test: After first turn — no bonus damage**
  Setup: Turn 2 of combat. Player has Dramatic Entrance in hand. Enemy A has 10 HP, Enemy B has 8 HP.
  Actions: Play Dramatic Entrance.
  Expected: Enemy A takes 2 damage (8 HP). Enemy B takes 2 damage (6 HP). No bonus damage. Dramatic Entrance is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded — +3 bonus on first turn**
  Setup: First turn of combat. Dramatic Entrance+ in hand. Enemy A has 10 HP, Enemy B has 10 HP.
  Actions: Play Dramatic Entrance+.
  Expected: Enemy A takes 5 damage (2 HIT + 3 bonus = 5, now 5 HP). Enemy B takes 5 damage (5 HP). Dramatic Entrance+ is exhausted.

- **Hand of Greed** [N] — BGHandOfGreed — Attack, Uncommon, Cost 2
  4 HIT. +3 damage if you have 10 or more Gold.
  *Upgrade: +5 damage if you have 10 or more Gold.*

  - [ ] Sim - [ ] Live — **Test: Basic — deal damage without gold bonus**
  Setup: Player has 3 energy, 5 Gold. Hand of Greed in hand. Enemy has 20 HP, 0 block.
  Actions: Play Hand of Greed targeting enemy.
  Expected: Enemy takes 4 damage (16 HP remaining). Player spent 2 energy.

  - [ ] Sim - [ ] Live — **Test: Gold threshold met — bonus damage**
  Setup: Player has 3 energy, 10 Gold. Hand of Greed in hand. Enemy has 20 HP, 0 block.
  Actions: Play Hand of Greed targeting enemy.
  Expected: Enemy takes 7 damage (4 HIT + 3 bonus = 7, 13 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded — larger gold bonus**
  Setup: Player has 3 energy, 15 Gold. Hand of Greed+ in hand. Enemy has 20 HP, 0 block.
  Actions: Play Hand of Greed+ targeting enemy.
  Expected: Enemy takes 9 damage (4 HIT + 5 bonus = 9, 11 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Exactly 10 gold — threshold is inclusive**
  Setup: Player has 2 energy, 10 Gold. Hand of Greed in hand. Enemy has 20 HP.
  Actions: Play Hand of Greed targeting enemy.
  Expected: Enemy takes 7 damage (bonus applies at exactly 10 Gold).

- **Mayhem** [N] — BGMayhem — Power, Uncommon, Cost 2
  Once per turn: Draw a card. Immediately play it for 0 Energy.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Basic — auto-play a drawn card each turn**
  Setup: Player has 3 energy. Mayhem in hand. Draw pile top card is a Strike (1 cost, 1 HIT). Enemy has 10 HP.
  Actions: Play Mayhem. End turn. Start next turn.
  Expected: Mayhem is placed as a power. At start of next turn, a card is drawn and immediately played for 0 energy. If Strike is auto-played, enemy takes 1 damage.

  - [ ] Sim - [ ] Live — **Test: Upgraded — costs 1 energy instead of 2**
  Setup: Player has 1 energy. Mayhem+ in hand.
  Actions: Play Mayhem+.
  Expected: Mayhem+ is placed as a power. Player spent 1 energy (0 remaining).

  - [ ] Sim - [ ] Live — **Test: Once per turn limit**
  Setup: Player has Mayhem power active. Start of turn. Draw pile has 5 cards.
  Actions: Start turn. Mayhem triggers, draws and plays 1 card automatically.
  Expected: Only 1 card is auto-drawn and auto-played by Mayhem this turn. Remaining cards are drawn normally.

- **Mind Blast** [N] — BGMind Blast — Attack, Uncommon, Cost 2
  X HIT. X is the number of other cards in your hand.
  *Upgrade: X+1 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic — damage equals hand size minus Mind Blast**
  Setup: Player has 3 energy. Hand contains Mind Blast and 4 other cards (5 total). Enemy has 20 HP, 0 block.
  Actions: Play Mind Blast targeting enemy.
  Expected: Enemy takes 4 damage (4 other cards in hand). Player spent 2 energy.

  - [ ] Sim - [ ] Live — **Test: Only card in hand — 0 damage**
  Setup: Player has 2 energy. Hand contains only Mind Blast. Enemy has 10 HP.
  Actions: Play Mind Blast targeting enemy.
  Expected: Enemy takes 0 damage (0 other cards in hand).

  - [ ] Sim - [ ] Live — **Test: Upgraded — X+1 damage**
  Setup: Player has 3 energy. Hand contains Mind Blast+ and 3 other cards (4 total). Enemy has 20 HP.
  Actions: Play Mind Blast+ targeting enemy.
  Expected: Enemy takes 4 damage (3 other cards + 1 bonus = 4).

- **Panacea** [N] — BGPanacea — Skill, Uncommon, Cost 0
  Retain. Remove all WEAK VULN from any player. Exhaust.
  *Upgrade: Retain. Remove all WEAK VULN from all players. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic — remove debuffs from a single player**
  Setup: Player has 3 energy. Panacea in hand. Player has 2 WEAK tokens and 1 VULN token.
  Actions: Play Panacea targeting self.
  Expected: All WEAK and VULN tokens removed from player. Panacea is exhausted. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Retain — stays in hand if not played**
  Setup: Player has 3 energy. Panacea in hand. Player has no debuffs.
  Actions: End turn without playing Panacea.
  Expected: Panacea is retained in hand for the next turn (not discarded).

  - [ ] Sim - [ ] Live — **Test: Upgraded — remove debuffs from all players**
  Setup: Panacea+ in hand. Player has 2 WEAK. Ally has 1 VULN and 1 WEAK.
  Actions: Play Panacea+.
  Expected: All WEAK and VULN removed from both player and ally. Panacea+ is exhausted.

- **Sadistic Nature** [N] — BGSadistic Nature — Power, Uncommon, Cost 0
  Whenever you put a token on an enemy, deal 1 damage to that enemy.
  *Upgrade: Deal 2 damage.*

  - [ ] Sim - [ ] Live — **Test: Basic — damage on debuff application**
  Setup: Player has Sadistic Nature power active. Player has a card that applies WEAK in hand. Enemy has 10 HP, 0 block.
  Actions: Play the WEAK-applying card targeting enemy.
  Expected: Enemy gains 1 WEAK token. Sadistic Nature triggers, dealing 1 damage to enemy (9 HP).

  - [ ] Sim - [ ] Live — **Test: Multiple tokens applied at once**
  Setup: Player has Sadistic Nature power active. Trip (VULN VULN) in hand. Enemy has 10 HP.
  Actions: Play Trip targeting enemy.
  Expected: Enemy gains 2 VULN tokens. Sadistic Nature triggers twice, dealing 1 damage each time (total 2 damage, enemy at 8 HP).

  - [ ] Sim - [ ] Live — **Test: Upgraded — deal 2 damage per token**
  Setup: Player has Sadistic Nature+ power active. A card applying WEAK in hand. Enemy has 10 HP.
  Actions: Play the WEAK-applying card targeting enemy.
  Expected: Enemy gains 1 WEAK token. Sadistic Nature+ triggers, dealing 2 damage to enemy (8 HP).
