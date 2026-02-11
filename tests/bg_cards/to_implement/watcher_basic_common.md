# Tests Not Implemented as Live Tests

These test scenarios from the markdown specs require features not available
in the single-card-play live test framework (multi-turn sequences, end-of-turn
verification, specific die roll control, multi-step miracle spending, or
scry choice handling).

## API Notes

- `sim.set_stance()` does not exist in the simulator API. Stances must be
  entered by playing stance-changing cards (Crescendo for Wrath,
  Tranquility/Vigilance for Calm). Live tests use the same approach by
  including the stance card in hand and playing it first.

## Watcher Basic

All basic card tests are implemented as both sim and live tests. Stance-dependent
tests use Crescendo/Tranquility/Vigilance to set up the required stance before
playing the card under test.

## Watcher Common

### Flying Sleeves: Retains in hand at end of turn
- **Reason:** Requires `end_player_turn` to verify the card stays in hand while
  other non-Retain cards are discarded. The live test framework does not support
  multi-turn sequences (ending a turn triggers enemy actions, draw, etc. which
  are not deterministic in a live game scenario).
- **Sim test:** Implemented in `test_watcher_common.py::test_flying_sleeves_retain`

### Protect: Retains in hand at end of turn
- **Reason:** Same as Flying Sleeves retain -- requires `end_player_turn` to
  verify retain behavior. Not feasible without multi-turn live test support.
- **Sim test:** Implemented in `test_watcher_common.py::test_protect_retain`

### Tranquility: Retains in hand at end of turn
- **Reason:** Same as above retain tests. Requires end-of-turn verification.
- **Sim test:** Implemented in `test_watcher_common.py::test_tranquility_retain`

### Crescendo: Retains in hand at end of turn
- **Reason:** Same as above retain tests. Requires end-of-turn verification.
- **Sim test:** Implemented in `test_watcher_common.py::test_crescendo_retain`

### Just Lucky: High die roll (4-6) deals damage and blocks
- **Reason:** The live test framework sets `die=1` by default in `set_scenario`.
  Testing the high-roll path (die 4-6) would require modifying the die value in
  `set_scenario` to 4, 5, or 6. The current test only covers the low-roll path
  (die=1). A separate live test with `die=5` in the set_scenario payload could
  be added once die control is exposed.
- **Sim test:** Implemented in `test_watcher_common.py::test_just_lucky_high_roll`
  (uses `sim.set_die_value(5)`)

### Just Lucky: Upgraded low roll deals 2 HIT and scries 2
- **Reason:** Same as above -- could be tested live with die=1 (which is a low
  roll), but the scry verification is limited in live tests.
- **Sim test:** Implemented in `test_watcher_common.py::test_just_lucky_upgraded_low_roll`

### Third Eye: Scry discards cards to discard pile
- **Reason:** Testing specific scry choices (which cards to discard during scry)
  requires handling the scry choice screen in the live game. The auto-confirm
  in `_wait_for_play_resolution` confirms the scry without specific choices.
  The sim auto-discards status cards but does not expose explicit scry choice.
- **Sim test:** Implemented in `test_watcher_common.py::test_third_eye_scry_discards`

### Miracle tokens: Spending miracles for energy
- **Reason:** In the live BG mod game, Miracles are actual cards added to hand
  that must be played individually. In the simulator, miracles are tracked via
  `MiracleCount` power and spent automatically when energy is insufficient.
  Testing the full Collect -> spend Miracle -> play Eruption chain in live
  requires identifying and playing the generated Miracle cards from hand, which
  needs card-finding logic for generated cards not in the original hand setup.
- **Sim test:** Implemented in `test_watcher_common.py::test_miracle_gives_energy`
  and `test_collect_then_use_miracles`

### Collect followed by using Miracles for energy
- **Reason:** Same as above -- the multi-step Collect -> Miracle -> Eruption
  chain involves generated cards that need to be found and played in the live
  game. The live Miracle cards have different card IDs from the setup cards.
- **Sim test:** Implemented in `test_watcher_common.py::test_collect_then_use_miracles`
