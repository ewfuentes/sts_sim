# Status — Special

- **Burn** [Y] — BGBurn — Status, Special, Cost -2
  Unplayable. At the end of your turn, take 1 damage.
  *Upgrade: Take 2 damage.*

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Burn in hand.
  Actions: Attempt to play Burn.
  Expected: Card cannot be played (Unplayable, cost -2).

  - [ ] Sim - [ ] Live — **Test: End of turn — take 1 damage**
  Setup: Player has 20 HP, 0 block. Burn in hand.
  Actions: End turn with Burn in hand.
  Expected: Player takes 1 damage (19 HP remaining). Burn is discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Burn — take 2 damage at end of turn**
  Setup: Player has 20 HP, 0 block. Burn+ in hand.
  Actions: End turn with Burn+ in hand.
  Expected: Player takes 2 damage (18 HP remaining). Burn+ is discarded.

  - [ ] Sim - [ ] Live — **Test: Block absorbs Burn damage**
  Setup: Player has 20 HP, 3 block. Burn in hand.
  Actions: End turn with Burn in hand.
  Expected: Player loses 1 block (2 block remaining, 20 HP). Burn damage is absorbed by block.

- **Dazed** [Y] — BGDazed — Status, Special, Cost -2
  Unplayable. Ethereal.

  - [ ] Sim - [ ] Live — **Test: Unplayable — cannot be played**
  Setup: Player has 3 energy. Dazed in hand.
  Actions: Attempt to play Dazed.
  Expected: Card cannot be played (Unplayable).

  - [ ] Sim - [ ] Live — **Test: Ethereal — exhausts at end of turn if in hand**
  Setup: Player has Dazed in hand.
  Actions: End turn.
  Expected: Dazed is exhausted from hand at end of turn (Ethereal keyword). It goes to exhaust pile and cannot be drawn again.

  - [ ] Sim - [ ] Live — **Test: Clogs hand — reduces effective hand size**
  Setup: Draw pile contains Dazed and 4 playable cards. Player draws 5 at start of turn.
  Actions: Start turn, draw 5 cards.
  Expected: Player has 4 playable cards and 1 Dazed. Dazed takes up a hand slot but cannot be played.

- **Slimed** [Y] — BGSlimed — Status, Special, Cost 1
  Exhaust.

  - [ ] Sim - [ ] Live — **Test: Basic — play to exhaust**
  Setup: Player has 3 energy. Slimed in hand.
  Actions: Play Slimed.
  Expected: Player spends 1 energy. Slimed is exhausted (removed from combat). No other effect.

  - [ ] Sim - [ ] Live — **Test: Not enough energy — cannot play**
  Setup: Player has 0 energy. Slimed in hand.
  Actions: Attempt to play Slimed.
  Expected: Cannot play Slimed (requires 1 energy). Card stays in hand.

  - [ ] Sim - [ ] Live — **Test: Discarded if not played — cycles through deck**
  Setup: Player has 3 energy. Slimed in hand.
  Actions: End turn without playing Slimed.
  Expected: Slimed is discarded to discard pile. It will be shuffled back into draw pile and drawn again in future turns (only exhausted when played).

- **Void** [Y] — BGVoidCard — Status, Special, Cost 1
  Exhaust. When you draw this card, you must immediately pay Energy to Exhaust it, if able.

  - [ ] Sim - [ ] Live — **Test: Draw with energy — auto-exhausts and costs energy**
  Setup: Player has 2 energy. Void is on top of draw pile.
  Actions: Draw a card (Void is drawn).
  Expected: Void is immediately exhausted. Player loses 1 energy (1 remaining). Void does not remain in hand.

  - [ ] Sim - [ ] Live — **Test: Draw with no energy — stays in hand**
  Setup: Player has 0 energy. Void is on top of draw pile.
  Actions: Draw a card (Void is drawn).
  Expected: Player cannot pay 1 energy. Void stays in hand. Player can play it manually later for 1 energy to exhaust it.

  - [ ] Sim - [ ] Live — **Test: Manually play from hand — exhaust**
  Setup: Player has 1 energy. Void is already in hand (was drawn with 0 energy earlier).
  Actions: Play Void.
  Expected: Player spends 1 energy. Void is exhausted.

  - [ ] Sim - [ ] Live — **Test: Drawn at start of turn — auto-exhausts from starting energy**
  Setup: Player has 3 energy at start of turn. Draw pile has Void and 4 other cards.
  Actions: Start turn, draw 5 cards.
  Expected: When Void is drawn, it is immediately exhausted and player loses 1 energy (2 remaining). Player draws 4 playable cards into hand.

- **Desync** [N] — BGDesync — Status, Special, Cost -2
  An error has occurred. One of your other mods is not compatible with The Board Game.

  - [ ] Sim - [ ] Live — **Test: Card exists as error indicator — unplayable**
  Setup: Player has 3 energy. Desync in hand.
  Actions: Attempt to play Desync.
  Expected: Card cannot be played (Unplayable, cost -2). This card indicates a mod compatibility issue.

  - [ ] Sim - [ ] Live — **Test: Clogs hand — takes up a hand slot**
  Setup: Draw pile contains Desync and 4 other cards. Player draws 5 at start of turn.
  Actions: Start turn, draw 5 cards.
  Expected: Desync occupies 1 hand slot. Player has 4 playable cards. Desync cannot be played or interacted with.
