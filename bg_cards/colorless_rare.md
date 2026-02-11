# Colorless — Rare

- **Apotheosis** [N] — BGApotheosis — Skill, Rare, Cost 2
  Your starter Strikes deal +1 damage. Your starter Defends gain +1 Block.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Basic — buff starter cards**
  Setup: Player has 3 energy. Apotheosis in hand. Deck contains starter Strike (1 HIT) and starter Defend (1 BLK).
  Actions: Play Apotheosis. Then play starter Strike targeting enemy. Then play starter Defend.
  Expected: Apotheosis costs 2 energy. Starter Strike now deals 2 damage (1 HIT + 1 bonus). Starter Defend now grants 2 block (1 BLK + 1 bonus).

  - [ ] Sim - [ ] Live — **Test: Upgraded — costs 1 energy**
  Setup: Player has 1 energy. Apotheosis+ in hand.
  Actions: Play Apotheosis+.
  Expected: Apotheosis+ costs 1 energy (reduced from 2). Player has 0 energy remaining. Starter Strikes and Defends are buffed.

  - [ ] Sim - [ ] Live — **Test: Only affects starter cards, not non-starter attacks/skills**
  Setup: Player has 3 energy. Apotheosis in hand. Deck contains a starter Strike and a non-starter attack card (e.g., Carnage, 3 HIT).
  Actions: Play Apotheosis. Play starter Strike. Play non-starter attack.
  Expected: Starter Strike deals +1 damage. Non-starter attack deals its normal damage (no bonus).

- **Apparition** [N] — BGGhostly — Skill, Rare, Cost 1
  Ethereal. You can't lose more than 1 HP this turn. Exhaust.
  *Upgrade: You can't lose more than 1 HP this turn. Exhaust. (No longer Ethereal.)*

  - [ ] Sim - [ ] Live — **Test: Basic — cap damage taken at 1 HP**
  Setup: Player has 20 HP, 0 block, 3 energy. Apparition in hand. Enemy intends to deal 8 damage.
  Actions: Play Apparition. End turn. Enemy attacks for 8 damage.
  Expected: Player takes only 1 damage (19 HP remaining). Apparition is exhausted.

  - [ ] Sim - [ ] Live — **Test: Ethereal — exhausts if not played**
  Setup: Player has 3 energy. Apparition in hand.
  Actions: End turn without playing Apparition.
  Expected: Apparition is exhausted from hand at end of turn (Ethereal keyword).

  - [ ] Sim - [ ] Live — **Test: Upgraded — no longer Ethereal**
  Setup: Player has 3 energy. Apparition+ in hand.
  Actions: End turn without playing Apparition+.
  Expected: Apparition+ is discarded normally at end of turn (not exhausted, since it is no longer Ethereal).

  - [ ] Sim - [ ] Live — **Test: Multiple hits in one turn still capped**
  Setup: Player has 20 HP, 0 block. Apparition played this turn. Enemy A intends 5 damage, Enemy B intends 3 damage.
  Actions: End turn. Enemy A attacks for 5, Enemy B attacks for 3.
  Expected: Player loses at most 1 HP total this turn (19 HP remaining). All excess damage is prevented.

- **Master of Strategy** [N] — BGMaster of Strategy — Skill, Rare, Cost 0
  Draw 3 cards.
  *Upgrade: Draw 4 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic — draw 3 cards for free**
  Setup: Player has 3 energy. Master of Strategy in hand. Draw pile has 5 cards.
  Actions: Play Master of Strategy.
  Expected: Player draws 3 cards. Player spent 0 energy. Master of Strategy goes to discard pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded — draw 4 cards**
  Setup: Player has 3 energy. Master of Strategy+ in hand. Draw pile has 5 cards.
  Actions: Play Master of Strategy+.
  Expected: Player draws 4 cards. Player spent 0 energy.

  - [ ] Sim - [ ] Live — **Test: Draw pile smaller than draw amount triggers reshuffle**
  Setup: Player has Master of Strategy in hand. Draw pile has 1 card. Discard pile has 5 cards.
  Actions: Play Master of Strategy.
  Expected: Player draws 1 card from draw pile. Discard pile is shuffled into draw pile. Player draws 2 more cards. Total 3 cards drawn.

- **Panache** [N] — BGPanache — Power, Rare, Cost 0
  End of turn: If your hand is empty, deal 3 damage to any row.
  *Upgrade: Deal 5 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: Basic — trigger on empty hand at end of turn**
  Setup: Player has Panache power active. Player plays all cards, hand is empty at end of turn. Enemy row has enemies with 10 HP each.
  Actions: Play all cards in hand. End turn.
  Expected: Panache triggers, dealing 3 damage to a chosen enemy row.

  - [ ] Sim - [ ] Live — **Test: Hand not empty — no trigger**
  Setup: Player has Panache power active. Player has 1 card remaining in hand at end of turn.
  Actions: End turn with 1 card still in hand.
  Expected: Panache does not trigger. No damage is dealt.

  - [ ] Sim - [ ] Live — **Test: Upgraded — deal 5 damage**
  Setup: Player has Panache+ power active. Player's hand is empty at end of turn. Enemy row has enemies with 10 HP.
  Actions: End turn with empty hand.
  Expected: Panache+ triggers, dealing 5 damage to a chosen enemy row.

- **The Bomb** [N] — BGThe Bomb — Skill, Rare, Cost 2
  At the end of 3 turns, deal 10 damage to ALL enemies, then Exhaust this card.
  *Upgrade: Deal 12 damage.*

  - [ ] Sim - [ ] Live — **Test: Basic — detonates after 3 turns**
  Setup: Player has 3 energy, turn 1. The Bomb in hand. Enemy A has 20 HP, Enemy B has 15 HP.
  Actions: Play The Bomb (turn 1). End turn 1. End turn 2. End turn 3.
  Expected: At end of turn 3 (3 turns after playing), The Bomb deals 10 damage to ALL enemies. Enemy A takes 10 damage (10 HP). Enemy B takes 10 damage (5 HP). The Bomb is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded — deal 12 damage**
  Setup: Player has 3 energy. The Bomb+ in hand. Enemy has 20 HP.
  Actions: Play The Bomb+. End 3 turns.
  Expected: At end of 3rd turn, The Bomb+ deals 12 damage to ALL enemies. Enemy has 8 HP remaining. The Bomb+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Does not trigger before 3 turns**
  Setup: Player has 3 energy. The Bomb in hand. Enemy has 20 HP.
  Actions: Play The Bomb. End turn 1. End turn 2.
  Expected: After 2 turns, The Bomb has not yet detonated. Enemy still has 20 HP. The Bomb is still active (not yet exhausted).
