"""Compare simulator CombatState vs live game state from CommunicationMod.

Used to verify that the Rust simulator matches the actual STS Board Game mod.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import sts_sim
from comms.game_state import CombatState as LiveCombatState, Power as LivePower


@dataclass
class Mismatch:
    field: str
    expected: object
    actual: object
    detail: str = ""

    def __str__(self):
        s = f"MISMATCH {self.field}: expected={self.expected}, actual={self.actual}"
        if self.detail:
            s += f" ({self.detail})"
        return s


@dataclass
class VerifyResult:
    matches: bool
    mismatches: list[Mismatch] = field(default_factory=list)

    def __str__(self):
        if self.matches:
            return "OK: all fields match"
        lines = [f"FAILED: {len(self.mismatches)} mismatch(es)"]
        for m in self.mismatches:
            lines.append(f"  - {m}")
        return "\n".join(lines)


def verify_combat_state(
    sim_state: sts_sim.CombatState,
    live_state: LiveCombatState,
) -> VerifyResult:
    """Compare simulator combat state against live game state.

    Args:
        sim_state: CombatState from the Rust/PyO3 simulator.
        live_state: CombatState parsed from CommunicationMod JSON.

    Returns:
        VerifyResult with match status and list of mismatches.
    """
    mismatches: list[Mismatch] = []

    # Player HP
    if sim_state.player.hp != live_state.player.current_hp:
        mismatches.append(Mismatch("player.hp", sim_state.player.hp, live_state.player.current_hp))

    # Player max HP
    if sim_state.player.max_hp != live_state.player.max_hp:
        mismatches.append(Mismatch("player.max_hp", sim_state.player.max_hp, live_state.player.max_hp))

    # Player block
    if sim_state.player.block != live_state.player.block:
        mismatches.append(Mismatch("player.block", sim_state.player.block, live_state.player.block))

    # Player energy
    if sim_state.player.energy != live_state.player.energy:
        mismatches.append(Mismatch("player.energy", sim_state.player.energy, live_state.player.energy))

    # Player powers
    _verify_powers(mismatches, "player", sim_state.player, live_state.player.powers)

    # Monsters
    sim_monsters = sim_state.get_monsters()
    live_monsters = [m for m in live_state.monsters if not m.is_gone]

    if len(sim_monsters) != len(live_monsters):
        mismatches.append(Mismatch(
            "monster_count",
            len(sim_monsters),
            len(live_monsters),
        ))
    else:
        for i, (sm, lm) in enumerate(zip(sim_monsters, live_monsters)):
            prefix = f"monster[{i}]({lm.name})"

            if sm.hp != lm.current_hp:
                mismatches.append(Mismatch(f"{prefix}.hp", sm.hp, lm.current_hp))

            if sm.block != lm.block:
                mismatches.append(Mismatch(f"{prefix}.block", sm.block, lm.block))

            _verify_powers(mismatches, prefix, sm, lm.powers)

    # Hand size
    sim_hand = sim_state.get_hand()
    if len(sim_hand) != len(live_state.hand):
        mismatches.append(Mismatch("hand_size", len(sim_hand), len(live_state.hand)))

    # Draw pile size
    if len(sim_state.player.draw_pile) != len(live_state.draw_pile):
        mismatches.append(Mismatch(
            "draw_pile_size",
            len(sim_state.player.draw_pile),
            len(live_state.draw_pile),
        ))

    # Discard pile size
    if len(sim_state.player.discard_pile) != len(live_state.discard_pile):
        mismatches.append(Mismatch(
            "discard_pile_size",
            len(sim_state.player.discard_pile),
            len(live_state.discard_pile),
        ))

    # Die roll — check for BGTheDiePower in player powers
    die_power = live_state.player.get_power("BGTheDiePower")
    if die_power is not None:
        sim_die = sim_state.die.last_roll if hasattr(sim_state.die, "last_roll") else None
        if sim_die is not None and sim_die != die_power.amount:
            mismatches.append(Mismatch("die_roll", sim_die, die_power.amount))

    return VerifyResult(matches=len(mismatches) == 0, mismatches=mismatches)


def _verify_powers(
    mismatches: list[Mismatch],
    prefix: str,
    sim_creature,
    live_powers: list[LivePower],
):
    """Compare powers between simulator creature and live power list."""
    # Map CommunicationMod power IDs to our PowerType names
    POWER_ID_MAP = {
        "Strength": "Strength",
        "Vulnerable": "Vulnerable",
        "Weak": "Weak",
        "Ritual": "Ritual",
        "Curl Up": "CurlUp",
        "Dexterity": "Dexterity",
        "Thorns": "Thorns",
        "Metallicize": "Metallicize",
        "Barricade": "Barricade",
        "Rage": "Rage",
        "Feel No Pain": "FeelNoPain",
        "Dark Embrace": "DarkEmbrace",
        "Rupture": "Rupture",
        "Combust": "Combust",
        "Evolve": "Evolve",
        "Fire Breathing": "FireBreathing",
        "Anger": "Anger",
        "Entangled": "Entangled",
        "Artifact": "Artifact",
        "Spore Cloud": "SporeCloud",
        "Juggernaut": "Juggernaut",
        "Demon Form": "DemonForm",
        "Corruption": "Corruption",
        "Double Tap": "DoubleTap",
        "No Draw": "NoDraw",
    }

    sim_powers = sim_creature.get_powers_dict()

    for lp in live_powers:
        power_name = POWER_ID_MAP.get(lp.power_id, lp.power_id)
        sim_amount = sim_powers.get(power_name, 0)
        if sim_amount != lp.amount:
            mismatches.append(Mismatch(
                f"{prefix}.power({lp.power_id})",
                sim_amount,
                lp.amount,
                f"sim has {sim_amount}, live has {lp.amount}",
            ))


def verify_and_print(
    sim_state: sts_sim.CombatState,
    live_state: LiveCombatState,
) -> VerifyResult:
    """Verify and print results to stdout."""
    result = verify_combat_state(sim_state, live_state)
    print(result)
    return result
