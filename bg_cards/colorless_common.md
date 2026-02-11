# Colorless — Common

- **Blind** [N] — BGBlind — Skill, Common, Cost 0
  WEAK. Exhaust.
  *Upgrade: WEAK WEAK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic — apply WEAK and exhaust**
  Setup: Player has 3 energy. Blind in hand. Enemy has no debuffs.
  Actions: Play Blind targeting enemy.
  Expected: Enemy gains 1 WEAK token. Blind is exhausted (moved to exhaust pile). Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded — apply double WEAK and exhaust**
  Setup: Player has 3 energy. Blind+ in hand. Enemy has no debuffs.
  Actions: Play Blind+ targeting enemy.
  Expected: Enemy gains 2 WEAK tokens. Blind+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Exhaust interaction — card is removed from combat after play**
  Setup: Player has Blind in hand. Discard pile is empty. Exhaust pile is empty.
  Actions: Play Blind targeting enemy. End turn. Start next turn.
  Expected: Blind is in exhaust pile, not in draw pile or discard pile. It cannot be drawn again.

- **Finesse** [N] — BGFinesse — Skill, Common, Cost 0
  1 BLK. Draw 1 card. Exhaust.
  *Upgrade: 1 BLK. Draw 1 card. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic — gain block, draw, and exhaust**
  Setup: Player has 0 block, 3 energy. Finesse in hand. Draw pile has at least 1 card.
  Actions: Play Finesse.
  Expected: Player gains 1 block. Player draws 1 card. Finesse is exhausted. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded — no longer exhausts**
  Setup: Player has 0 block, 3 energy. Finesse+ in hand. Draw pile has at least 1 card.
  Actions: Play Finesse+.
  Expected: Player gains 1 block. Player draws 1 card. Finesse+ goes to discard pile (not exhaust pile).

  - [ ] Sim - [ ] Live — **Test: Empty draw pile — draw triggers shuffle**
  Setup: Player has Finesse in hand. Draw pile is empty. Discard pile has 3 cards.
  Actions: Play Finesse.
  Expected: Player gains 1 block. Discard pile is shuffled into draw pile, then player draws 1 card. Finesse is exhausted.

- **Flash of Steel** [N] — BGFlash of Steel — Attack, Common, Cost 0
  1 HIT. Draw 1 card. Exhaust.
  *Upgrade: 1 HIT. Draw 1 card. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic — deal damage, draw, and exhaust**
  Setup: Player has 3 energy. Flash of Steel in hand. Enemy has 10 HP, 0 block. Draw pile has at least 1 card.
  Actions: Play Flash of Steel targeting enemy.
  Expected: Enemy takes 1 damage (9 HP remaining). Player draws 1 card. Flash of Steel is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded — no longer exhausts**
  Setup: Player has 3 energy. Flash of Steel+ in hand. Enemy has 10 HP. Draw pile has at least 1 card.
  Actions: Play Flash of Steel+ targeting enemy.
  Expected: Enemy takes 1 damage. Player draws 1 card. Flash of Steel+ goes to discard pile (not exhaust pile).

  - [ ] Sim - [ ] Live — **Test: Damage against enemy with block**
  Setup: Player has Flash of Steel in hand. Enemy has 10 HP, 1 block. Draw pile has 1 card.
  Actions: Play Flash of Steel targeting enemy.
  Expected: Enemy loses 1 block (0 block remaining, 10 HP). Player draws 1 card. Flash of Steel is exhausted.

- **Good Instincts** [N] — BGGood Instincts — Skill, Common, Cost 0
  1 BLK to any player.
  *Upgrade: 2 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Basic — gain block on self**
  Setup: Player has 0 block, 3 energy. Good Instincts in hand.
  Actions: Play Good Instincts targeting self.
  Expected: Player gains 1 block. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Target another player**
  Setup: Player has 0 block, 3 energy. Good Instincts in hand. Ally player has 0 block.
  Actions: Play Good Instincts targeting ally.
  Expected: Ally gains 1 block. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded — double block**
  Setup: Player has 0 block, 3 energy. Good Instincts+ in hand.
  Actions: Play Good Instincts+ targeting self.
  Expected: Player gains 2 block.

- **Impatience** [N] — BGImpatience — Skill, Common, Cost 0
  Draw 2 cards.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic — draw 2 cards**
  Setup: Player has 3 energy, 1 card in hand (Impatience). Draw pile has 5 cards.
  Actions: Play Impatience.
  Expected: Player draws 2 cards (now has 2 cards in hand). Player spent 0 energy. Impatience is in discard pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded — draw 3 cards**
  Setup: Player has 3 energy, 1 card in hand (Impatience+). Draw pile has 5 cards.
  Actions: Play Impatience+.
  Expected: Player draws 3 cards (now has 3 cards in hand).

  - [ ] Sim - [ ] Live — **Test: Draw pile has fewer cards than draw amount**
  Setup: Player has Impatience in hand. Draw pile has 1 card. Discard pile has 3 cards.
  Actions: Play Impatience.
  Expected: Player draws 1 card from draw pile. Discard pile is shuffled into draw pile. Player draws 1 more card. Total 2 cards drawn.

- **Madness** [N] — BGMadness — Skill, Common, Cost 0
  The next card you play this turn costs 0. Exhaust.
  *Upgrade: The next card you play this turn costs 0. Retain. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic — next card costs 0**
  Setup: Player has 1 energy. Hand contains Madness and a card that costs 2 energy.
  Actions: Play Madness. Play the 2-cost card.
  Expected: Madness is exhausted. The 2-cost card is played for 0 energy. Player still has 1 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Effect only applies to the very next card**
  Setup: Player has 1 energy. Hand contains Madness, a 1-cost card (A), and a 2-cost card (B).
  Actions: Play Madness. Play card A. Attempt to play card B.
  Expected: Madness exhausted. Card A played for 0 energy. Card B costs its normal 2 energy and cannot be played (only 1 energy left).

  - [ ] Sim - [ ] Live — **Test: Upgraded — retains if not played**
  Setup: Player has 3 energy. Hand contains Madness+ and 2 other cards.
  Actions: End turn without playing Madness+.
  Expected: Madness+ is retained in hand for next turn (not discarded). It is not exhausted since it was not played.

- **Purity** [N] — BGPurity — Skill, Common, Cost 0
  Exhaust up to 3 cards from your hand.
  *Upgrade: Exhaust up to 5 cards from your hand.*

  - [ ] Sim - [ ] Live — **Test: Basic — exhaust cards from hand**
  Setup: Player has 3 energy. Hand contains Purity, Card A, Card B, Card C, Card D.
  Actions: Play Purity. Choose Card A, Card B, Card C to exhaust.
  Expected: Cards A, B, C are moved to exhaust pile. Player spent 0 energy. Player hand contains Card D. Purity is in discard pile.

  - [ ] Sim - [ ] Live — **Test: Exhaust fewer than maximum**
  Setup: Player has 3 energy. Hand contains Purity and Card A.
  Actions: Play Purity. Choose Card A to exhaust (1 of up to 3).
  Expected: Card A is exhausted. Purity is in discard pile. Player hand is empty.

  - [ ] Sim - [ ] Live — **Test: Upgraded — exhaust up to 5**
  Setup: Player has 3 energy. Hand contains Purity+ and 5 other cards.
  Actions: Play Purity+. Choose all 5 cards to exhaust.
  Expected: All 5 chosen cards are moved to exhaust pile. Player hand is empty.

- **Swift Strike** [N] — BGSwift Strike — Attack, Common, Cost 0
  1 HIT. You may switch rows with another player.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic — deal damage and optionally switch rows**
  Setup: Player has 3 energy, is in front row. Swift Strike in hand. Enemy has 10 HP.
  Actions: Play Swift Strike targeting enemy. Choose to switch rows with an ally in back row.
  Expected: Enemy takes 1 damage (9 HP). Player moves to back row, ally moves to front row.

  - [ ] Sim - [ ] Live — **Test: Decline row switch**
  Setup: Player is in front row. Swift Strike in hand. Enemy has 10 HP.
  Actions: Play Swift Strike targeting enemy. Choose not to switch rows.
  Expected: Enemy takes 1 damage. Player remains in front row.

  - [ ] Sim - [ ] Live — **Test: Upgraded — deal 2 damage**
  Setup: Player has 3 energy. Swift Strike+ in hand. Enemy has 10 HP, 0 block.
  Actions: Play Swift Strike+ targeting enemy.
  Expected: Enemy takes 2 damage (8 HP remaining).

- **Thinking Ahead** [N] — BGThinking Ahead — Skill, Common, Cost 0
  Draw 2 cards. Then put a card from your hand on top of your draw pile. Exhaust.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic — draw 2, put 1 back, exhaust**
  Setup: Player has 3 energy. Hand contains Thinking Ahead. Draw pile has cards [X, Y, Z] (X on top).
  Actions: Play Thinking Ahead. Draw 2 cards (X and Y). Choose card X to put on top of draw pile.
  Expected: Player drew 2 cards, put 1 back on top of draw pile. Draw pile top card is X. Thinking Ahead is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded — draw 3 instead of 2**
  Setup: Player has 3 energy. Hand contains Thinking Ahead+. Draw pile has 5 cards.
  Actions: Play Thinking Ahead+. Draw 3 cards. Choose 1 card to put on top of draw pile.
  Expected: Player draws 3 cards, puts 1 back on top of draw pile. Net gain of 2 cards in hand. Thinking Ahead+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Card put back is the first drawn next turn**
  Setup: Player has Thinking Ahead in hand. Draw pile has [A, B, C, D, E].
  Actions: Play Thinking Ahead. Draw A and B. Put B on top of draw pile. End turn.
  Expected: Thinking Ahead is exhausted. On next turn, B is the first card drawn from draw pile.

- **Trip** [N] — BGTrip — Skill, Common, Cost 0
  VULN VULN. Exhaust.
  *Upgrade: VULN VULN VULN. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic — apply 2 VULN and exhaust**
  Setup: Player has 3 energy. Trip in hand. Enemy has no debuffs.
  Actions: Play Trip targeting enemy.
  Expected: Enemy gains 2 VULN tokens. Trip is exhausted. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded — apply 3 VULN**
  Setup: Player has 3 energy. Trip+ in hand. Enemy has no debuffs.
  Actions: Play Trip+ targeting enemy.
  Expected: Enemy gains 3 VULN tokens. Trip+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Stacking VULN on already-vulnerable enemy**
  Setup: Player has Trip in hand. Enemy already has 1 VULN token.
  Actions: Play Trip targeting enemy.
  Expected: Enemy now has 3 VULN tokens total (1 existing + 2 from Trip). Trip is exhausted.
