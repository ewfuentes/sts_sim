"""Live verification tests — compare simulator against the real STS Board Game mod.

These tests require a running Slay the Spire instance with:
1. The Board Game mod loaded
2. CommunicationMod configured with the relay (comms/relay.py)

Run with: pytest tests/live/ -v
Tests auto-skip if the relay is not reachable.
"""
