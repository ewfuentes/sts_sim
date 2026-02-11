# Watcher (BGPurple) — Rare

- **Ragnarok** [Y] — BGRagnarok — Attack, Rare, Cost 3
  1 HIT 1 HIT 1 HIT 1 HIT 1 HIT. Each HIT can have a different target.
  *Upgrade: 1 HIT 1 HIT 1 HIT 1 HIT 1 HIT 1 HIT. (6 hits.)*

  - [ ] Sim - [ ] Live — **Test: 5 hits on a single target**
  Setup: Player in Neutral stance, 3 energy. One enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play Ragnarok, directing all 5 hits at the enemy.
  Expected: Enemy loses 5 HP (5 hits of 1 damage each). Player spends 3 energy.

  - [ ] Sim - [ ] Live — **Test: Hits split across multiple targets**
  Setup: Player in Neutral stance, 3 energy. Enemy A at 10 HP, Enemy B at 10 HP, both 0 block. Player has 0 Strength.
  Actions: Play Ragnarok, directing 3 hits at Enemy A and 2 hits at Enemy B.
  Expected: Enemy A loses 3 HP (down to 7). Enemy B loses 2 HP (down to 8).

  - [ ] Sim - [ ] Live — **Test: Strength adds to each individual hit**
  Setup: Player in Neutral stance, 3 energy, 2 Strength. One enemy at 30 HP, 0 block.
  Actions: Play Ragnarok, all hits on the enemy.
  Expected: Enemy loses 15 HP (5 hits of 1+2=3 damage each).

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 6 hits**
  Setup: Player in Neutral stance, 3 energy, 0 Strength. One enemy at 20 HP, 0 block. Ragnarok is upgraded.
  Actions: Play Ragnarok+, all hits on the enemy.
  Expected: Enemy loses 6 HP (6 hits of 1 damage each).

- **Brilliance** [Y] — BGBrilliance — Attack, Rare, Cost 1
  Deal 2 HIT for each MIRACLE you have.
  *Upgrade: Deal 3 HIT for each MIRACLE you have.*

  - [ ] Sim - [ ] Live — **Test: Damage scales with Miracles**
  Setup: Player in Neutral stance, 3 energy, 3 Miracles. Enemy at 30 HP, 0 block. Player has 0 Strength.
  Actions: Play Brilliance targeting the enemy.
  Expected: Enemy loses 6 HP (3 Miracles x 2 HIT = 6 hits of 1 damage).

  - [ ] Sim - [ ] Live — **Test: No Miracles means no damage**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Enemy at 20 HP, 0 block.
  Actions: Play Brilliance targeting the enemy.
  Expected: Enemy loses 0 HP (0 Miracles x 2 HIT = 0 hits).

  - [ ] Sim - [ ] Live — **Test: Upgraded version with Miracles and Strength**
  Setup: Player in Neutral stance, 3 energy, 2 Miracles, 1 Strength. Enemy at 30 HP, 0 block. Brilliance is upgraded.
  Actions: Play Brilliance+ targeting the enemy.
  Expected: Enemy loses 12 HP (2 Miracles x 3 HIT = 6 hits, each dealing 1+1=2 damage).

- **Blasphemy** [Y] — BGBlasphemy — Skill, Rare, Cost 1
  Your next Attack this turn is played 3 times. Exhaust your draw pile. Exhaust.
  *Upgrade: Retain. Your next Attack this turn is played 3 times. Exhaust your draw pile. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Next Attack plays 3 times**
  Setup: Player in Neutral stance, 3 energy. Hand has Blasphemy and a 2 HIT Attack (cost 1). Enemy at 20 HP, 0 block. Draw pile has 5 cards.
  Actions: Play Blasphemy. Play the 2 HIT Attack targeting the enemy.
  Expected: The Attack is played 3 times. Enemy loses 6 HP (3 plays x 2 HIT = 6 damage). Draw pile is exhausted (all 5 cards removed). Blasphemy is exhausted.

  - [ ] Sim - [ ] Live — **Test: Draw pile is fully exhausted**
  Setup: Player in Neutral stance, 3 energy. Hand has Blasphemy and a 1 HIT Attack. Draw pile has 8 cards. Exhaust pile is empty.
  Actions: Play Blasphemy. Play the 1 HIT Attack.
  Expected: All 8 draw pile cards move to exhaust pile. Blasphemy is also exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded version has Retain**
  Setup: Player in Neutral stance, 3 energy. Hand has Blasphemy+ and 3 other cards. No Attack in hand this turn.
  Actions: End turn without playing Blasphemy+.
  Expected: Blasphemy+ remains in hand (Retain). Other cards without Retain are discarded.

- **Deus Ex Machina** [Y] — BGDeusExMachina — Skill, Rare, Cost 0
  MIRACLE MIRACLE. Exhaust.
  *Upgrade: MIRACLE MIRACLE MIRACLE. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Gain 2 Miracles and exhaust**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles.
  Actions: Play Deus Ex Machina.
  Expected: Player gains 2 Miracles. Card is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version gains 3 Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Deus Ex Machina is upgraded.
  Actions: Play Deus Ex Machina+.
  Expected: Player gains 3 Miracles. Card is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Miracles usable for energy after playing**
  Setup: Player in Neutral stance, 0 energy, 0 Miracles.
  Actions: Play Deus Ex Machina (costs 0). Spend both Miracles.
  Expected: Player gains 2 Miracles. After spending both, player has 2 energy.

- **Omniscience** [Y] — BGOmniscience — Skill, Rare, Cost 3
  Search your draw pile for an Attack or Skill. Play the card twice for 0 Energy and Exhaust it. Shuffle your draw pile. Exhaust.
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Search and play an Attack twice**
  Setup: Player in Neutral stance, 3 energy. Draw pile contains a 3 HIT Attack (cost 2). Enemy at 20 HP, 0 block.
  Actions: Play Omniscience, choosing the 3 HIT Attack from the draw pile.
  Expected: The 3 HIT Attack is played twice for 0 energy. Enemy loses 6 HP (3+3). The Attack is exhausted. Draw pile is shuffled. Omniscience is exhausted. Player spends 3 energy.

  - [ ] Sim - [ ] Live — **Test: Search and play a Skill twice**
  Setup: Player in Neutral stance, 3 energy, 0 block. Draw pile contains a card that gives 3 BLK (cost 1).
  Actions: Play Omniscience, choosing the 3 BLK Skill.
  Expected: The Skill is played twice for 0 energy. Player gains 6 block total. The Skill is exhausted. Draw pile is shuffled. Omniscience is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded version costs 2 energy**
  Setup: Player in Neutral stance, 3 energy. Draw pile contains a 2 HIT Attack. Enemy at 20 HP. Omniscience is upgraded.
  Actions: Play Omniscience+.
  Expected: Player spends 2 energy (instead of 3). The chosen card is played twice and exhausted.

- **Scrawl** [Y] — BGScrawl — Skill, Rare, Cost 1
  Draw 5 cards. Exhaust.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Draw 5 cards and exhaust**
  Setup: Player in Neutral stance, 3 energy. Draw pile has 8 cards. Hand has Scrawl and 1 other card.
  Actions: Play Scrawl.
  Expected: Player draws 5 cards (hand now has 6 cards). Scrawl is exhausted. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version costs 0**
  Setup: Player in Neutral stance, 3 energy. Draw pile has 8 cards. Hand has Scrawl+. Scrawl is upgraded.
  Actions: Play Scrawl+.
  Expected: Player draws 5 cards. Scrawl+ is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Draw pile has fewer than 5 cards**
  Setup: Player in Neutral stance, 3 energy. Draw pile has 3 cards. Discard pile has 5 cards.
  Actions: Play Scrawl.
  Expected: Player draws 3 cards from draw pile, discard pile is shuffled into draw pile, player draws 2 more. Scrawl is exhausted.

- **Vault** [Y] — BGVault — Skill, Rare, Cost 3
  Discard all cards without Retain. Draw 5 cards. Gain Energy(W) Energy(W) Energy(W). Exhaust.
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Discard non-Retain cards, draw 5, gain 3 energy**
  Setup: Player in Neutral stance, 3 energy. Hand has Vault and 3 non-Retain cards. Draw pile has 8 cards.
  Actions: Play Vault.
  Expected: 3 non-Retain cards discarded. Player draws 5 new cards. Player gains 3 energy. Vault is exhausted. Net energy: 3 - 3 (cost) + 3 (gained) = 3.

  - [ ] Sim - [ ] Live — **Test: Retain cards stay in hand**
  Setup: Player in Neutral stance, 3 energy. Hand has Vault, 2 non-Retain cards, and 1 card with Retain. Draw pile has 8 cards.
  Actions: Play Vault.
  Expected: 2 non-Retain cards discarded. The Retain card stays in hand. Player draws 5 cards. Player gains 3 energy. Hand has 1 Retain card + 5 drawn cards = 6 cards.

  - [ ] Sim - [ ] Live — **Test: Upgraded version costs 2 energy**
  Setup: Player in Neutral stance, 3 energy. Hand has Vault+ and 2 non-Retain cards. Draw pile has 8 cards. Vault is upgraded.
  Actions: Play Vault+.
  Expected: Player spends 2 energy. Non-Retain cards discarded. Player draws 5 cards. Player gains 3 energy. Net energy: 3 - 2 + 3 = 4.

- **Wish** [Y] — BGWish — Skill, Rare, Cost 0
  Choose one: Gain STR, 10 BLK, or MIRACLE MIRACLE MIRACLE MIRACLE. Exhaust.
  *Upgrade: Choose one: Gain STR STR, 15 BLK, or MIRACLE MIRACLE MIRACLE MIRACLE MIRACLE. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Choose Strength**
  Setup: Player in Neutral stance, 3 energy, 0 Strength, 0 block, 0 Miracles.
  Actions: Play Wish, choosing Strength.
  Expected: Player gains 1 Strength. Card is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Choose block**
  Setup: Player in Neutral stance, 3 energy, 0 block.
  Actions: Play Wish, choosing block.
  Expected: Player gains 10 block. Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Choose Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles.
  Actions: Play Wish, choosing Miracles.
  Expected: Player gains 4 Miracles. Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Strength option gives 2 STR**
  Setup: Player in Neutral stance, 3 energy, 0 Strength. Wish is upgraded.
  Actions: Play Wish+, choosing Strength.
  Expected: Player gains 2 Strength. Card is exhausted.

- **Spirit Shield** [Y] — BGSpiritShield — Skill, Rare, Cost 2
  1 BLK for each card in your hand. Exhaust.
  *Upgrade: 1 BLK for each card in your hand. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Block scales with hand size**
  Setup: Player in Neutral stance, 3 energy, 0 block. Hand has Spirit Shield and 4 other cards (5 total).
  Actions: Play Spirit Shield.
  Expected: Player gains 5 block (1 per card in hand, counting Spirit Shield before it leaves). Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Large hand gives more block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Hand has Spirit Shield and 7 other cards (8 total).
  Actions: Play Spirit Shield.
  Expected: Player gains 8 block. Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded version does not exhaust**
  Setup: Player in Neutral stance, 3 energy, 0 block. Hand has Spirit Shield+ and 4 other cards. Spirit Shield is upgraded.
  Actions: Play Spirit Shield+.
  Expected: Player gains 5 block. Card goes to discard pile instead of being exhausted.

- **Judgment** [Y] — BGJudgment — Skill, Rare, Cost 1
  Ethereal. Choose an enemy. If they have 7 HP or less, set their HP to 0.
  *Upgrade: Retain. Choose an enemy. If they have 8 HP or less, set their HP to 0. (No longer Ethereal.)*

  - [ ] Sim - [ ] Live — **Test: Kill enemy at or below 7 HP**
  Setup: Player in Neutral stance, 3 energy. Enemy at 7 HP.
  Actions: Play Judgment targeting the enemy.
  Expected: Enemy HP set to 0 (killed).

  - [ ] Sim - [ ] Live — **Test: No effect on enemy above 7 HP**
  Setup: Player in Neutral stance, 3 energy. Enemy at 8 HP.
  Actions: Play Judgment targeting the enemy.
  Expected: Enemy remains at 8 HP. No damage dealt.

  - [ ] Sim - [ ] Live — **Test: Ethereal causes exhaust if not played**
  Setup: Player in Neutral stance, 3 energy. Hand has Judgment and 4 other cards.
  Actions: End turn without playing Judgment.
  Expected: Judgment is exhausted at end of turn (Ethereal keyword).

  - [ ] Sim - [ ] Live — **Test: Upgraded version kills at 8 HP and has Retain**
  Setup: Player in Neutral stance, 3 energy. Enemy at 8 HP. Judgment is upgraded.
  Actions: End turn without playing Judgment+. Next turn, play Judgment+ targeting the enemy.
  Expected: Judgment+ stays in hand at end of first turn (Retain, no longer Ethereal). On second turn, enemy HP set to 0.

- **Worship** [Y] — BGWorship — Skill, Rare, Cost -1
  Gain X+1 MIRACLE. Exhaust.
  *Upgrade: Retain. Gain X+1 MIRACLE. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Spend all energy for Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles.
  Actions: Play Worship (X=3, spending all 3 energy).
  Expected: Player gains 4 Miracles (X+1 = 3+1). Card is exhausted. Player has 0 energy.

  - [ ] Sim - [ ] Live — **Test: Spend 0 energy still gives 1 Miracle**
  Setup: Player in Neutral stance, 0 energy, 0 Miracles.
  Actions: Play Worship (X=0).
  Expected: Player gains 1 Miracle (0+1). Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded version has Retain**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Worship is upgraded. Hand has Worship+ and 3 other cards.
  Actions: End turn without playing Worship+.
  Expected: Worship+ remains in hand next turn (Retain). Other non-Retain cards are discarded.

- **Omega** [Y] — BGOmega — Power, Rare, Cost 3
  End of turn: Deal 5 damage to any row.
  *Upgrade: Deal 6 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: Deal 5 damage at end of turn**
  Setup: Player in Neutral stance, 3 energy. Enemy row has 2 enemies at 20 HP each.
  Actions: Play Omega. End turn.
  Expected: At end of turn, 5 damage is dealt to the chosen enemy row (each enemy in that row takes 5 damage).

  - [ ] Sim - [ ] Live — **Test: Triggers every turn**
  Setup: Player in Neutral stance, 3 energy. Omega active. Enemy at 20 HP.
  Actions: End turn. Start next turn. End turn.
  Expected: Enemy takes 5 damage at end of first turn (down to 15) and 5 damage at end of second turn (down to 10).

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 6 damage**
  Setup: Player in Neutral stance, 3 energy. Omega+ active. Enemy at 20 HP.
  Actions: End turn.
  Expected: Enemy takes 6 damage (down to 14) at end of turn.

- **Deva Form** [Y] — BGDevaForm — Power, Rare, Cost 3
  Start of turn: MIRACLE.
  *Upgrade: Start of turn: MIRACLE MIRACLE.*

  - [ ] Sim - [ ] Live — **Test: Gain Miracle at start of each turn**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles.
  Actions: Play Deva Form. End turn. Start next turn.
  Expected: At start of next turn, player gains 1 Miracle.

  - [ ] Sim - [ ] Live — **Test: Accumulates Miracles over multiple turns**
  Setup: Player in Neutral stance. Deva Form active. 0 Miracles.
  Actions: End turn. Start turn 2. End turn. Start turn 3.
  Expected: Player gains 1 Miracle at start of turn 2 (total 1), and 1 Miracle at start of turn 3 (total 2, assuming none were spent).

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 2 Miracles per turn**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Deva Form is upgraded.
  Actions: Play Deva Form+. End turn. Start next turn.
  Expected: At start of next turn, player gains 2 Miracles.

- **Devotion** [Y] — BGDevotion — Power, Rare, Cost 1
  Start of turn: Gain MIRACLE and draw 1 card. Exhaust this card after 3 turns.
  *Upgrade: Exhaust after 4 turns.*

  - [ ] Sim - [ ] Live — **Test: Gain Miracle and draw each turn**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Draw pile has 10+ cards.
  Actions: Play Devotion. End turn. Start next turn.
  Expected: At start of next turn, player gains 1 Miracle and draws 1 extra card (6 total including the base 5).

  - [ ] Sim - [ ] Live — **Test: Exhausts after 3 turns**
  Setup: Player in Neutral stance. Devotion active, played this turn.
  Actions: End turn 1, start turn 2 (trigger 1). End turn 2, start turn 3 (trigger 2). End turn 3, start turn 4 (trigger 3).
  Expected: Devotion triggers at start of turns 2, 3, and 4 (granting Miracle + draw each). After the 3rd trigger, Devotion exhausts and no longer provides benefits.

  - [ ] Sim - [ ] Live — **Test: Upgraded version lasts 4 turns**
  Setup: Player in Neutral stance, 3 energy. Devotion is upgraded.
  Actions: Play Devotion+. Progress through 4 turn starts.
  Expected: Devotion+ triggers 4 times (giving Miracle + draw each), then exhausts after the 4th trigger.

- **Establishment** [Y] — BGEstablishment — Power, Rare, Cost 1
  Start of turn: Cards you Retained last turn cost 1 less Energy(W) this turn.
  *Upgrade: Cost 2 less Energy(W) this turn.*

  - [ ] Sim - [ ] Live — **Test: Retained card costs 1 less**
  Setup: Player in Neutral stance, 3 energy. Establishment active. Hand has a cost-2 Retain card.
  Actions: End turn (card is Retained). Start next turn.
  Expected: The Retained card now costs 1 energy (reduced from 2).

  - [ ] Sim - [ ] Live — **Test: Cost cannot go below 0**
  Setup: Player in Neutral stance, 3 energy. Establishment active. Hand has a cost-1 Retain card.
  Actions: End turn (card is Retained). Start next turn.
  Expected: The Retained card now costs 0 energy (reduced from 1, minimum 0).

  - [ ] Sim - [ ] Live — **Test: Upgraded version reduces by 2**
  Setup: Player in Neutral stance, 3 energy. Establishment+ active. Hand has a cost-3 Retain card.
  Actions: End turn (card is Retained). Start next turn.
  Expected: The Retained card now costs 1 energy (reduced from 3 by 2).

- **Conjure Blade** [Y] — BGConjureBlade — Power, Rare, Cost -1
  Your starter Strikes deal X+1 extra damage.
  *Upgrade: X+2 extra damage.*

  - [ ] Sim - [ ] Live — **Test: Strikes deal extra damage**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Hand has a starter Strike (1 HIT).
  Actions: Play Conjure Blade (X=3, spending all 3 energy). Play the Strike.
  Expected: Conjure Blade grants Strikes +4 extra damage (X+1 = 3+1). Strike deals 1+4 = 5 damage. Enemy loses 5 HP.

  - [ ] Sim - [ ] Live — **Test: Spend 0 energy gives +1 extra damage**
  Setup: Player in Neutral stance, 0 energy. Enemy at 20 HP. Hand has a starter Strike.
  Actions: Play Conjure Blade (X=0). Play the Strike using a Miracle for energy.
  Expected: Strikes deal +1 extra damage (0+1). Strike deals 1+1 = 2 damage.

  - [ ] Sim - [ ] Live — **Test: Upgraded version gives X+2 extra damage**
  Setup: Player in Neutral stance, 2 energy. Enemy at 20 HP, 0 block. Hand has a starter Strike. Conjure Blade is upgraded.
  Actions: Play Conjure Blade+ (X=2). Play the Strike.
  Expected: Strikes deal +4 extra damage (X+2 = 2+2). Strike deals 1+4 = 5 damage.

- **Talk to the Hand** [N] — BGTalkToTheHand — Attack, Rare, Cost 2
  2 HIT. 1 BLK for each MIRACLE you have.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Deal damage and gain block from Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 block, 3 Miracles. Enemy at 20 HP, 0 block.
  Actions: Play Talk to the Hand targeting the enemy.
  Expected: Enemy loses 2 HP. Player gains 3 block (1 per Miracle).

  - [ ] Sim - [ ] Live — **Test: No Miracles means no block**
  Setup: Player in Neutral stance, 3 energy, 0 block, 0 Miracles. Enemy at 20 HP, 0 block.
  Actions: Play Talk to the Hand targeting the enemy.
  Expected: Enemy loses 2 HP. Player gains 0 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 3 HIT with Miracle block**
  Setup: Player in Neutral stance, 3 energy, 0 block, 2 Miracles. Enemy at 20 HP, 0 block. Talk to the Hand is upgraded.
  Actions: Play Talk to the Hand+ targeting the enemy.
  Expected: Enemy loses 3 HP. Player gains 2 block (1 per Miracle).
