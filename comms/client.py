"""Python client for connecting to the CommunicationMod relay.

Connects to the TCP relay (relay.py) and provides high-level methods
for interacting with a running Slay the Spire instance.
"""

import json
import socket
import time
from typing import Optional

from comms.game_state import parse_game_state, GameState

HOST = "localhost"
PORT = 38281
RECV_BUF = 65536


class Client:
    """TCP client for CommunicationMod relay."""

    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self._sock: Optional[socket.socket] = None
        self._buf = ""
        self.last_raw: Optional[dict] = None
        self.last_state: Optional[GameState] = None
        self.ready_for_command = False
        self.in_game = False
        self.last_error: Optional[str] = None

    def connect(self, timeout: float = 10.0, retry_interval: float = 0.5):
        """Connect to the relay, retrying until timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                self._sock = sock
                self._buf = ""
                return
            except ConnectionRefusedError:
                time.sleep(retry_interval)
        raise ConnectionError(f"Could not connect to relay at {self.host}:{self.port} within {timeout}s")

    def disconnect(self):
        """Disconnect from the relay."""
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def _recv_line(self, timeout: Optional[float] = None) -> str:
        """Receive one newline-delimited message from relay."""
        if self._sock is None:
            raise ConnectionError("Not connected")
        if timeout is not None:
            self._sock.settimeout(timeout)
        else:
            self._sock.settimeout(None)
        while "\n" not in self._buf:
            data = self._sock.recv(RECV_BUF)
            if not data:
                raise ConnectionError("Relay disconnected")
            self._buf += data.decode("utf-8")
        line, self._buf = self._buf.split("\n", 1)
        return line

    def send_command(self, cmd: str):
        """Send a command string to CommunicationMod via relay."""
        if self._sock is None:
            raise ConnectionError("Not connected")
        self._sock.sendall((cmd + "\n").encode("utf-8"))

    def wait_for_state(self, timeout: Optional[float] = 30.0) -> GameState:
        """Wait for next game state message and parse it.

        Returns parsed GameState. Updates internal state tracking.
        """
        line = self._recv_line(timeout=timeout)
        raw = json.loads(line)
        self.last_raw = raw

        self.last_error = raw.get("error")
        self.ready_for_command = raw.get("ready_for_command", False)
        self.in_game = raw.get("in_game", False)

        if self.last_error is None and self.in_game and "game_state" in raw:
            self.last_state = parse_game_state(raw["game_state"], raw.get("available_commands", []))
            return self.last_state

        return self.last_state

    # --- Convenience methods ---

    def play_card(self, card_index: int, target_index: Optional[int] = None):
        """Play a card from hand. Indices are 0-based (converted to 1-based for CommunicationMod)."""
        if target_index is not None:
            self.send_command(f"play {card_index + 1} {target_index}")
        else:
            self.send_command(f"play {card_index + 1}")

    def end_turn(self):
        """End the current turn."""
        self.send_command("end")

    def choose(self, index: int):
        """Choose an option by index."""
        self.send_command(f"choose {index}")

    def proceed(self):
        """Proceed / confirm on current screen."""
        self.send_command("proceed")

    def start_game(self, character: str = "BG_IRONCLAD", ascension: int = 0, seed: Optional[str] = None):
        """Start a new game. Defaults to Board Game Ironclad."""
        cmd = f"start {character} {ascension}"
        if seed is not None:
            cmd += f" {seed}"
        self.send_command(cmd)

    def signal_ready(self):
        """Send the ready signal (typically done by relay, but available for direct use)."""
        self.send_command("ready")

    def request_state(self):
        """Request current game state."""
        self.send_command("state")

    def set_state(self, state: dict):
        """Set game state directly (debug/testing). Hidden from available_commands."""
        self.send_command(f"set {json.dumps(state)}")

    def abandon(self):
        """Abandon the current run. Returns to main menu via death screen."""
        self.send_command("abandon")
