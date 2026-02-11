# Tests Not Implemented as Live Tests

These test scenarios from the markdown specs require features not available
in the single-card-play live test framework (multi-turn sequences, negative
playability checks, or complex auto-play interactions).

## Ironclad Basic

### Defend: Block from Defend is removed at start of next turn
- **Reason:** Requires `end_player_turn` followed by observing the next turn's
  block reset. The live test framework does not support multi-turn sequences
  (ending a turn triggers enemy actions, draw, etc. which are not deterministic
  in a live game scenario).

## Ironclad Common

### Clash: Clash cannot be played when hand contains non-Attack cards
- **Reason:** This is a negative test (verifying a card *cannot* be played).
  The live framework's `play_card_both` would attempt to play the card, which
  either fails silently or causes an error state in the BG mod. There is no
  clean way to assert "card was not played" via the current helper API.
  Additionally, the simulator comment notes the Clash restriction may not be
  fully implemented yet.

### Flex: Base Flex grants temporary Strength and exhausts (multi-card sequence)
- **Reason:** The full scenario requires playing Flex, then playing Strike in
  the same turn. While this could work with two sequential `play_card_both`
  calls, the test also requires verifying end-of-turn STR loss, which needs
  `end_player_turn` support in the live framework.

### Flex: Flex Strength is lost at end of turn
- **Reason:** Requires `end_player_turn` to observe the temporary Strength
  being removed. Not feasible without multi-turn live test support.

### Flex: Upgraded Flex does not exhaust
- **Reason:** The key assertion (Flex+ goes to discard, not exhaust) could
  be tested live with a single play, but the spec also requires verifying
  end-of-turn STR loss. The discard-vs-exhaust part is partially testable.

### Wild Strike: Dazed card pollutes future draws
- **Reason:** Requires ending the turn and starting the next turn to observe
  that the Dazed card from Wild Strike appears in future draws. Multi-turn
  sequence not supported.

### Seeing Red: Seeing Red allows playing expensive card afterward
- **Reason:** Requires playing two cards in sequence (Seeing Red then Bash).
  While mechanically possible with two `play_card_both` calls, the test
  pattern diverges from the standard single-play-per-test structure. The
  individual energy gain from Seeing Red is already tested in the live suite.

### Havoc: Havoc with a Power card does not exhaust it
- **Reason:** Havoc auto-plays the drawn card via intermediate choice screens.
  When the drawn card is a Power (Inflame), verifying it was NOT exhausted
  requires checking that Inflame applied its effect and is not in the exhaust
  pile. The auto-target resolution for Havoc with non-targeted Powers may
  produce inconsistent intermediate screens in the BG mod.

### Havoc: Havoc with empty draw pile
- **Reason:** Havoc with an empty draw pile triggers reshuffle before auto-play.
  The combination of reshuffle + auto-play + intermediate choice screens
  makes the live game state difficult to predict deterministically.

### Warcry: Warcry with only 1 card in draw pile
- **Reason:** Requires reshuffle during the draw phase of Warcry. The
  interaction between draw, reshuffle, and the put-back choice screen
  may produce non-deterministic intermediate states in the BG mod.
