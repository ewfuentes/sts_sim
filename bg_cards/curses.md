# Curses — Special

- **Ascender's Bane** [Y] — BGAscendersBane — Curse, Special, Cost -2
  Unplayable. Ethereal. Can't be removed from your deck.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played from hand**
  Setup: Player has 3 energy. Ascender's Bane in hand.
  Actions: Attempt to play Ascender's Bane.
  Expected: Card cannot be played (cost -2, Unplayable). No effect occurs. Card remains in hand.

  - [ ] Sim - [ ] Live — **Test: Ethereal — exhausts at end of turn if in hand**
  Setup: Player has 3 energy. Ascender's Bane in hand.
  Actions: End turn without playing any cards.
  Expected: Ascender's Bane is exhausted from hand at end of turn (Ethereal keyword).

  - [ ] Sim - [ ] Live — **Test: Cannot be removed from deck**
  Setup: Player has Ascender's Bane in their deck. Player visits a shop or event that offers card removal.
  Actions: Attempt to remove Ascender's Bane from deck.
  Expected: Ascender's Bane cannot be selected for removal. It persists in the deck.

- **Clumsy** [N] — Clumsy — Curse, Special, Cost -2
  Unplayable. Ethereal.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played from hand**
  Setup: Player has 3 energy. Clumsy in hand.
  Actions: Attempt to play Clumsy.
  Expected: Card cannot be played (Unplayable). No effect occurs.

  - [ ] Sim - [ ] Live — **Test: Ethereal — exhausts at end of turn if in hand**
  Setup: Player has Clumsy in hand.
  Actions: End turn.
  Expected: Clumsy is exhausted from hand at end of turn (Ethereal keyword). It goes to exhaust pile.

  - [ ] Sim - [ ] Live — **Test: Drawn into hand — takes up a hand slot**
  Setup: Draw pile contains Clumsy and 4 other cards. Player draws 5 cards at start of turn.
  Actions: Start turn, draw 5 cards.
  Expected: Clumsy occupies 1 of the 5 hand slots. Player effectively has only 4 playable cards.

- **Decay** [Y] — BGDecay — Curse, Special, Cost -2
  Unplayable. End of turn: If this card is in your hand, take 1 damage.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Decay in hand.
  Actions: Attempt to play Decay.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: End of turn damage — takes 1 damage while in hand**
  Setup: Player has 20 HP, 0 block. Decay in hand.
  Actions: End turn with Decay still in hand.
  Expected: Player takes 1 damage (19 HP remaining). Decay is discarded normally (not Ethereal).

  - [ ] Sim - [ ] Live — **Test: Block absorbs end-of-turn damage**
  Setup: Player has 20 HP, 2 block. Decay in hand.
  Actions: End turn with Decay still in hand.
  Expected: Player loses 1 block (1 block remaining, 20 HP). Decay damage is absorbed by block.

- **Doubt** [N] — BGDoubt — Curse, Special, Cost -2
  Unplayable. End of turn: If this card is in your hand, gain WEAK.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Doubt in hand.
  Actions: Attempt to play Doubt.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: End of turn — gain WEAK while in hand**
  Setup: Player has no debuffs. Doubt in hand.
  Actions: End turn with Doubt still in hand.
  Expected: Player gains 1 WEAK token. Doubt is discarded normally.

  - [ ] Sim - [ ] Live — **Test: Stacks with existing WEAK**
  Setup: Player already has 1 WEAK token. Doubt in hand.
  Actions: End turn with Doubt in hand.
  Expected: Player now has 2 WEAK tokens (1 existing + 1 from Doubt).

- **Injury** [Y] — BGInjury — Curse, Special, Cost -2
  Unplayable.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Injury in hand.
  Actions: Attempt to play Injury.
  Expected: Card cannot be played (Unplayable). No effect occurs.

  - [ ] Sim - [ ] Live — **Test: Clogs hand — takes up a card slot**
  Setup: Draw pile contains Injury and 4 other playable cards. Player draws 5 at start of turn.
  Actions: Start turn, draw 5 cards.
  Expected: Injury takes up 1 hand slot. Player has 4 playable cards and 1 dead card.

  - [ ] Sim - [ ] Live — **Test: Not Ethereal — stays in discard after turn ends**
  Setup: Injury in hand. Exhaust pile is empty.
  Actions: End turn.
  Expected: Injury is discarded to discard pile (not exhausted). It will cycle back through the draw pile on future turns.

- **Pain** [Y] — BGPain — Curse, Special, Cost -2
  Unplayable. End of turn: If 2 or fewer cards are in your hand, lose 1 HP.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Pain in hand.
  Actions: Attempt to play Pain.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: End of turn — lose HP when hand has 2 or fewer cards**
  Setup: Player has 20 HP. Hand contains Pain and 1 other card (2 cards total).
  Actions: End turn.
  Expected: Player loses 1 HP (19 HP remaining). Condition met: 2 or fewer cards in hand.

  - [ ] Sim - [ ] Live — **Test: No HP loss when hand has more than 2 cards**
  Setup: Player has 20 HP. Hand contains Pain and 3 other cards (4 cards total).
  Actions: End turn.
  Expected: Player does not lose HP (still 20 HP). Condition not met: more than 2 cards in hand.

  - [ ] Sim - [ ] Live — **Test: Only Pain in hand — triggers**
  Setup: Player has 20 HP. Hand contains only Pain (1 card).
  Actions: End turn.
  Expected: Player loses 1 HP (19 HP). 1 card is fewer than 2, condition is met.

- **Parasite** [N] — BGParasite — Curse, Special, Cost -2
  Unplayable. If this card is removed from your deck, lose 2 HP.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Parasite in hand.
  Actions: Attempt to play Parasite.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: Removing from deck causes HP loss**
  Setup: Player has 20 HP. Parasite is in player's deck. Player visits a card removal event.
  Actions: Remove Parasite from deck.
  Expected: Parasite is removed from deck. Player loses 2 HP (18 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Clogs hand — no passive effect during combat**
  Setup: Player has 20 HP. Parasite in hand. No other effects active.
  Actions: End turn with Parasite in hand.
  Expected: No damage taken, no debuffs applied. Parasite is simply discarded. Its only penalty is on deck removal.

- **Regret** [N] — BGRegret — Curse, Special, Cost -2
  Unplayable. Retain.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Regret in hand.
  Actions: Attempt to play Regret.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: Retain — stays in hand every turn**
  Setup: Player has Regret in hand. Turn 1.
  Actions: End turn 1. Start turn 2.
  Expected: Regret is retained in hand (not discarded). It persists in hand at start of turn 2, taking up a hand slot every turn.

  - [ ] Sim - [ ] Live — **Test: Permanently clogs one hand slot until combat ends**
  Setup: Player has Regret in hand. Turn 1. Player draws 5 cards per turn.
  Actions: End turn 1. Draw 5 cards at start of turn 2.
  Expected: Regret is retained. Player has Regret + 5 newly drawn cards = 6 cards in hand (or hand-size-limited). Regret continues to occupy a slot.

- **Shame** [N] — BGShame — Curse, Special, Cost -2
  Unplayable. End of turn: If this card is in your hand, lose 1 BLK.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Shame in hand.
  Actions: Attempt to play Shame.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: End of turn — lose 1 block while in hand**
  Setup: Player has 3 block. Shame in hand.
  Actions: End turn with Shame in hand.
  Expected: Player loses 1 block (2 block remaining). Shame is discarded.

  - [ ] Sim - [ ] Live — **Test: No block to lose — no negative block**
  Setup: Player has 0 block. Shame in hand.
  Actions: End turn with Shame in hand.
  Expected: Player remains at 0 block. Block does not go negative. Shame is discarded.

- **Writhe** [N] — BGWrithe — Curse, Special, Cost 1
  When played, Exhaust.

  - [ ] Sim - [ ] Live — **Test: Basic — play to exhaust and remove from combat**
  Setup: Player has 3 energy. Writhe in hand.
  Actions: Play Writhe.
  Expected: Player spends 1 energy. Writhe is exhausted (removed from combat). No other effect occurs.

  - [ ] Sim - [ ] Live — **Test: Not enough energy — cannot play**
  Setup: Player has 0 energy. Writhe in hand.
  Actions: Attempt to play Writhe.
  Expected: Cannot play Writhe (requires 1 energy). Card stays in hand.

  - [ ] Sim - [ ] Live — **Test: Discarded if not played — returns to draw pile**
  Setup: Player has 3 energy. Writhe in hand.
  Actions: End turn without playing Writhe.
  Expected: Writhe is discarded to discard pile. It will return in future draws (not exhausted since it was not played).
