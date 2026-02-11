# Watcher (BGPurple) — Common

- **Flurry of Blows** [Y] — BGFlurryOfBlows — Attack, Common, Cost 0
  1 HIT. Deals an additional 1 HIT if you switched Stances this turn.
  *Upgrade: Deals an additional 1 HIT 1 HIT if you switched Stances this turn.*

  - [ ] Sim - [ ] Live — **Test: Flurry of Blows without stance switch deals 1 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. No stance changes this turn.
  Actions: Play Flurry of Blows targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Flurry of Blows with stance switch deals 2 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Hand contains Crescendo and Flurry of Blows.
  Actions: Play Crescendo (enter Wrath, stance switch occurred). Play Flurry of Blows targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). Flurry of Blows deals 1+1=2 HIT, doubled by Wrath = 4 damage.

  - [ ] Sim - [ ] Live — **Test: Upgraded Flurry of Blows with stance switch deals 3 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Flurry of Blows is upgraded. Hand also contains Crescendo.
  Actions: Play Crescendo (enter Wrath). Play Flurry of Blows+ targeting enemy.
  Expected: Enemy loses 6 HP (14 HP remaining). Upgraded deals 1+1+1=3 HIT, doubled by Wrath = 6 damage.

- **Empty Fist** [Y] — BGEmptyFist — Attack, Common, Cost 1
  2 HIT. Enter Neutral.
  *Upgrade: 3 HIT. Enter Neutral.*

  - [ ] Sim - [ ] Live — **Test: Empty Fist from Wrath deals double damage and exits Wrath**
  Setup: Player in Wrath stance, 3 energy. Enemy has 20 HP.
  Actions: Play Empty Fist targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 2 HIT doubled by Wrath = 4 damage. Player enters Neutral stance. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Empty Fist from Calm grants 2 energy and enters Neutral**
  Setup: Player in Calm stance, 3 energy. Enemy has 20 HP.
  Actions: Play Empty Fist targeting enemy.
  Expected: Player leaves Calm (gains 2 energy). Enemy loses 2 HP (18 HP remaining). Player enters Neutral. Player ends with 4 energy (3 - 1 cost + 2 from Calm).

  - [ ] Sim - [ ] Live — **Test: Upgraded Empty Fist deals 3 HIT**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Empty Fist is upgraded.
  Actions: Play Empty Fist+ targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). Player remains in Neutral. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Empty Fist from Neutral stays in Neutral**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP.
  Actions: Play Empty Fist targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player remains in Neutral (no stance change occurs).

- **Consecrate** [Y] — BGConsecrate — Attack, Common, Cost 0
  AOE 1 HIT.
  *Upgrade: AOE 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Consecrate hits all enemies for 1 damage**
  Setup: Player in Neutral stance, 3 energy. Enemy A has 15 HP, Enemy B has 10 HP.
  Actions: Play Consecrate.
  Expected: Enemy A loses 1 HP (14 HP remaining). Enemy B loses 1 HP (9 HP remaining). Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Consecrate in Wrath deals double AOE damage**
  Setup: Player in Wrath stance, 3 energy. Enemy A has 15 HP, Enemy B has 10 HP.
  Actions: Play Consecrate.
  Expected: Enemy A loses 2 HP (13 HP remaining). Enemy B loses 2 HP (8 HP remaining). Wrath doubles the 1 HIT to 2 damage per enemy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Consecrate deals 2 HIT AOE**
  Setup: Player in Neutral stance, 3 energy. Enemy A has 15 HP, Enemy B has 10 HP. Consecrate is upgraded.
  Actions: Play Consecrate+.
  Expected: Enemy A loses 2 HP (13 HP remaining). Enemy B loses 2 HP (8 HP remaining).

- **Cut Through Fate** [Y] — BGCutThroughFate — Attack, Common, Cost 1
  1 HIT. Scry 2. Draw 1 card.
  *Upgrade: 2 HIT. Scry 3. Draw 1 card.*

  - [ ] Sim - [ ] Live — **Test: Cut Through Fate deals damage, scries, and draws**
  Setup: Player in Neutral stance, 3 energy, 4 cards in hand. Enemy has 20 HP. Draw pile has 5 cards.
  Actions: Play Cut Through Fate targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player scries 2 (looks at top 2 cards of draw pile, may discard any). Player draws 1 card (hand size goes to 4). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Cut Through Fate deals 2 damage and scries 3**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Cut Through Fate is upgraded. Draw pile has 5 cards.
  Actions: Play Cut Through Fate+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player scries 3. Player draws 1 card.

  - [ ] Sim - [ ] Live — **Test: Cut Through Fate in Wrath doubles damage**
  Setup: Player in Wrath stance, 3 energy. Enemy has 20 HP. Draw pile has 5 cards.
  Actions: Play Cut Through Fate targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 1 HIT doubled by Wrath = 2 damage. Player scries 2. Player draws 1 card.

- **Just Lucky** [Y] — BGJustLucky — Attack, Common, Cost 0
  [1] [2] [3] 1 HIT Scry 1. [4] [5] [6] 1 HIT 1 BLK.
  *Upgrade: [1] [2] [3] 2 HIT Scry 2. [4] [5] [6] 2 HIT 1 BLK.*

  - [ ] Sim - [ ] Live — **Test: Just Lucky rolls low (1-3) deals damage and scries**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Die roll result is 2. Draw pile has 5 cards.
  Actions: Play Just Lucky targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player scries 1. Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Just Lucky rolls high (4-6) deals damage and blocks**
  Setup: Player in Neutral stance, 3 energy, 0 block. Enemy has 20 HP. Die roll result is 5.
  Actions: Play Just Lucky targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player gains 1 block. Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Just Lucky rolls low deals 2 HIT and scries 2**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Just Lucky is upgraded. Die roll result is 1. Draw pile has 5 cards.
  Actions: Play Just Lucky+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player scries 2.

  - [ ] Sim - [ ] Live — **Test: Just Lucky in Wrath doubles damage on either roll**
  Setup: Player in Wrath stance, 3 energy, 0 block. Enemy has 20 HP. Die roll result is 4.
  Actions: Play Just Lucky targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 1 HIT doubled by Wrath = 2 damage. Player gains 1 block.

- **Flying Sleeves** [Y] — BGFlyingSleeves — Attack, Common, Cost 1
  Retain. 1 HIT 1 HIT.
  *Upgrade: Retain. 1 HIT 1 HIT 1 HIT.*

  - [ ] Sim - [ ] Live — **Test: Flying Sleeves deals 2 damage in two hits**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP.
  Actions: Play Flying Sleeves targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 2 separate HIT instances of 1 damage each. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Flying Sleeves retains in hand at end of turn**
  Setup: Player in Neutral stance, 3 energy. Hand contains Flying Sleeves and 4 other cards.
  Actions: End turn without playing Flying Sleeves.
  Expected: Flying Sleeves stays in hand for next turn. Other non-Retain cards are discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Flying Sleeves deals 3 damage in three hits**
  Setup: Player in Neutral stance, 3 energy. Enemy has 20 HP. Flying Sleeves is upgraded.
  Actions: Play Flying Sleeves+ targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). 3 separate HIT instances of 1 damage each.

  - [ ] Sim - [ ] Live — **Test: Flying Sleeves with Strength benefits on each HIT**
  Setup: Player in Neutral stance, 3 energy, 2 Strength. Enemy has 20 HP.
  Actions: Play Flying Sleeves targeting enemy.
  Expected: Enemy loses 6 HP (14 HP remaining). Each HIT deals 1 base + 2 Strength = 3 damage, across 2 hits = 6 total.

- **Empty Body** [Y] — BGEmptyBody — Skill, Common, Cost 1
  2 BLK. Enter Neutral.
  *Upgrade: 3 BLK. Enter Neutral.*

  - [ ] Sim - [ ] Live — **Test: Empty Body grants 2 block and enters Neutral**
  Setup: Player in Wrath stance, 3 energy, 0 block.
  Actions: Play Empty Body.
  Expected: Player gains 2 block. Player enters Neutral stance. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Empty Body from Calm grants energy and enters Neutral**
  Setup: Player in Calm stance, 3 energy, 0 block.
  Actions: Play Empty Body.
  Expected: Player leaves Calm (gains 2 energy). Player gains 2 block. Player enters Neutral. Player ends with 4 energy (3 - 1 cost + 2 from Calm).

  - [ ] Sim - [ ] Live — **Test: Upgraded Empty Body grants 3 block**
  Setup: Player in Wrath stance, 3 energy, 0 block. Empty Body is upgraded.
  Actions: Play Empty Body+.
  Expected: Player gains 3 block. Player enters Neutral stance. Player spends 1 energy (2 remaining).

- **Protect** [Y] — BGProtect — Skill, Common, Cost 2
  Retain. 3 BLK to any player.
  *Upgrade: Retain. 4 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Protect grants 3 block**
  Setup: Player in Neutral stance, 3 energy, 0 block.
  Actions: Play Protect targeting self.
  Expected: Player gains 3 block. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Protect retains in hand at end of turn**
  Setup: Player in Neutral stance, 3 energy, 0 block. Hand contains Protect and 4 other cards.
  Actions: End turn without playing Protect.
  Expected: Protect stays in hand for next turn. Other non-Retain cards are discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Protect grants 4 block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Protect is upgraded.
  Actions: Play Protect+ targeting self.
  Expected: Player gains 4 block. Player spends 2 energy (1 remaining).

- **Halt** [Y] — BGHalt — Skill, Common, Cost 0
  1 BLK. +1 BLK if you're in Wrath.
  *Upgrade: 1 BLK. +2 BLK if you're in Wrath.*

  - [ ] Sim - [ ] Live — **Test: Halt in Neutral grants 1 block**
  Setup: Player in Neutral stance, 3 energy, 0 block.
  Actions: Play Halt.
  Expected: Player gains 1 block. Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Halt in Wrath grants 2 block**
  Setup: Player in Wrath stance, 3 energy, 0 block.
  Actions: Play Halt.
  Expected: Player gains 2 block (1 base + 1 Wrath bonus). Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Halt in Wrath grants 3 block**
  Setup: Player in Wrath stance, 3 energy, 0 block. Halt is upgraded.
  Actions: Play Halt+.
  Expected: Player gains 3 block (1 base + 2 Wrath bonus). Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Halt in Calm grants only 1 block**
  Setup: Player in Calm stance, 3 energy, 0 block.
  Actions: Play Halt.
  Expected: Player gains 1 block. Wrath bonus does not apply since player is in Calm.

- **Third Eye** [Y] — BGThirdEye — Skill, Common, Cost 1
  2 BLK. Scry 3.
  *Upgrade: 3 BLK. Scry 5.*

  - [ ] Sim - [ ] Live — **Test: Third Eye grants 2 block and scries 3**
  Setup: Player in Neutral stance, 3 energy, 0 block. Draw pile has 5 cards.
  Actions: Play Third Eye.
  Expected: Player gains 2 block. Player scries 3 (looks at top 3 cards of draw pile, may discard any). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Third Eye grants 3 block and scries 5**
  Setup: Player in Neutral stance, 3 energy, 0 block. Third Eye is upgraded. Draw pile has 6 cards.
  Actions: Play Third Eye+.
  Expected: Player gains 3 block. Player scries 5 (looks at top 5 cards of draw pile, may discard any). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Third Eye scry discards cards to discard pile**
  Setup: Player in Neutral stance, 3 energy, 0 block. Draw pile top 3 cards are Strike, Defend, Eruption. Discard pile is empty.
  Actions: Play Third Eye. During scry, choose to discard Strike and Eruption.
  Expected: Player gains 2 block. Strike and Eruption move to discard pile. Defend remains on top of draw pile.

- **Tranquility** [Y] — BGTranquility — Skill, Common, Cost 1
  Retain. Enter Calm. Exhaust.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Tranquility enters Calm and exhausts**
  Setup: Player in Neutral stance, 3 energy.
  Actions: Play Tranquility.
  Expected: Player enters Calm stance. Tranquility is exhausted (moved to exhaust pile, not discard pile). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Tranquility retains in hand at end of turn**
  Setup: Player in Neutral stance, 3 energy. Hand contains Tranquility and 4 other cards.
  Actions: End turn without playing Tranquility.
  Expected: Tranquility stays in hand for next turn. Other non-Retain cards are discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Tranquility costs 0 energy**
  Setup: Player in Neutral stance, 3 energy. Tranquility is upgraded.
  Actions: Play Tranquility+.
  Expected: Player enters Calm stance. Tranquility is exhausted. Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Tranquility from Wrath exits Wrath and enters Calm**
  Setup: Player in Wrath stance, 3 energy.
  Actions: Play Tranquility.
  Expected: Player leaves Wrath and enters Calm stance. Tranquility is exhausted. Player spends 1 energy (2 remaining).

- **Crescendo** [Y] — BGCrescendo — Skill, Common, Cost 1
  Retain. Enter Wrath. Exhaust.
  *Upgrade: Retain. Enter Wrath. Draw 1 card. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Crescendo enters Wrath and exhausts**
  Setup: Player in Neutral stance, 3 energy.
  Actions: Play Crescendo.
  Expected: Player enters Wrath stance. Crescendo is exhausted. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Crescendo from Calm grants 2 energy on exit and enters Wrath**
  Setup: Player in Calm stance, 3 energy.
  Actions: Play Crescendo.
  Expected: Player leaves Calm (gains 2 energy). Player enters Wrath. Crescendo is exhausted. Player ends with 4 energy (3 - 1 cost + 2 from Calm).

  - [ ] Sim - [ ] Live — **Test: Upgraded Crescendo draws 1 card**
  Setup: Player in Neutral stance, 3 energy, 4 cards in hand. Crescendo is upgraded. Draw pile has 5 cards.
  Actions: Play Crescendo+.
  Expected: Player enters Wrath. Player draws 1 card (hand size goes to 4). Crescendo is exhausted. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Crescendo retains in hand at end of turn**
  Setup: Player in Neutral stance, 3 energy. Hand contains Crescendo and 4 other cards.
  Actions: End turn without playing Crescendo.
  Expected: Crescendo stays in hand for next turn. Other non-Retain cards are discarded.

- **Collect** [Y] — BGCollect — Skill, Common, Cost -1
  MIRACLE MIRACLE. Exhaust.
  *Upgrade: MIRACLE MIRACLE MIRACLE. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Collect generates 2 miracles and exhausts**
  Setup: Player in Neutral stance, 3 energy, 4 cards in hand.
  Actions: Play Collect.
  Expected: Player gains 2 Miracle tokens added to hand (hand size goes to 5). Collect is exhausted. Costs 0 energy (Cost -1 means free).

  - [ ] Sim - [ ] Live — **Test: Upgraded Collect generates 3 miracles**
  Setup: Player in Neutral stance, 3 energy, 3 cards in hand. Collect is upgraded.
  Actions: Play Collect+.
  Expected: Player gains 3 Miracle tokens added to hand (hand size goes to 5). Collect is exhausted.

  - [ ] Sim - [ ] Live — **Test: Miracle tokens can be spent for 1 energy each**
  Setup: Player in Neutral stance, 0 energy. Hand contains 2 Miracle tokens and a Strike (cost 1).
  Actions: Spend 1 Miracle token (gain 1 energy). Play Strike targeting enemy.
  Expected: Player gains 1 energy from Miracle. Miracle is exhausted. Strike is played dealing 1 HP to enemy. Player ends with 0 energy, 1 Miracle remaining in hand.

  - [ ] Sim - [ ] Live — **Test: Collect followed by using Miracles for energy**
  Setup: Player in Neutral stance, 0 energy, hand contains Collect and Eruption (cost 2). Enemy has 20 HP.
  Actions: Play Collect (gain 2 Miracles). Spend both Miracles (gain 2 energy). Play Eruption targeting enemy.
  Expected: Player gains 2 Miracles, then spends both for 2 energy total. Eruption deals 2 HP to enemy (18 HP remaining). Player enters Wrath. Collect and both Miracles are exhausted.
