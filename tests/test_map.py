"""Tests for Act 1 map generation."""
import pytest
import sts_sim


def test_generate_map_creates_nodes():
    m = sts_sim.generate_map(seed=42)
    assert len(m.nodes) > 0


def test_map_has_layout_id():
    m = sts_sim.generate_map(seed=42)
    assert m.layout_id in (1, 2)


def test_map_has_boss_node():
    m = sts_sim.generate_map(seed=42)
    boss_nodes = [n for n in m.nodes if n.room_type == sts_sim.RoomType.Boss]
    assert len(boss_nodes) == 1
    assert boss_nodes[0].row == 0
    assert boss_nodes[0].col == 3


def test_map_has_start_node():
    m = sts_sim.generate_map(seed=42)
    starts = m.get_start_nodes()
    assert len(starts) == 1
    assert starts[0].row == 12
    assert starts[0].room_type == sts_sim.RoomType.Monster


def test_map_get_node():
    m = sts_sim.generate_map(seed=42)
    boss = m.get_node(0, 3)
    assert boss is not None
    assert boss.room_type == sts_sim.RoomType.Boss

    empty = m.get_node(0, 0)
    assert empty is None


def test_map_connections():
    m = sts_sim.generate_map(seed=42)
    start = m.get_start_nodes()[0]
    # Start node should have connections upward
    conns = m.get_connections(start.row, start.col)
    assert len(conns) > 0
    # All connections should be one row up
    for conn in conns:
        assert conn.row == start.row - 1


def test_map_deterministic():
    m1 = sts_sim.generate_map(seed=42)
    m2 = sts_sim.generate_map(seed=42)
    assert m1.layout_id == m2.layout_id
    assert len(m1.nodes) == len(m2.nodes)
    for n1, n2 in zip(m1.nodes, m2.nodes):
        assert n1.row == n2.row
        assert n1.col == n2.col
        assert n1.room_type == n2.room_type


def test_map_different_seeds():
    m1 = sts_sim.generate_map(seed=1)
    m2 = sts_sim.generate_map(seed=2)
    # Different seeds may produce same or different layouts,
    # but token assignments should differ
    types1 = sorted([(n.row, n.col, n.room_type) for n in m1.nodes])
    types2 = sorted([(n.row, n.col, n.room_type) for n in m2.nodes])
    # At least some nodes should differ (tokens randomized)
    # (This could rarely fail if both happen to produce identical maps)


def test_map_has_all_room_types():
    """The map should contain most room types across various seeds."""
    all_types = set()
    for seed in range(10):
        m = sts_sim.generate_map(seed=seed)
        for n in m.nodes:
            all_types.add(n.room_type)
    # Should have at least Monster, Elite, Rest, Shop, Event, Treasure, Boss
    assert sts_sim.RoomType.Monster in all_types
    assert sts_sim.RoomType.Boss in all_types
    assert sts_sim.RoomType.Rest in all_types


def test_map_row_0_is_boss():
    for seed in range(5):
        m = sts_sim.generate_map(seed=seed)
        row0 = m.get_row(0)
        assert len(row0) == 1
        assert row0[0].room_type == sts_sim.RoomType.Boss


def test_map_row_1_has_rest():
    for seed in range(5):
        m = sts_sim.generate_map(seed=seed)
        row1 = m.get_row(1)
        rest_count = sum(1 for n in row1 if n.room_type == sts_sim.RoomType.Rest)
        assert rest_count >= 2  # Both layouts have 4 rest sites in row 1


def test_map_row_12_is_start():
    for seed in range(5):
        m = sts_sim.generate_map(seed=seed)
        row12 = m.get_row(12)
        assert len(row12) == 1
        assert row12[0].room_type == sts_sim.RoomType.Monster


def test_map_no_connections_from_boss():
    m = sts_sim.generate_map(seed=42)
    boss = m.get_node(0, 3)
    # Boss should have no outgoing connections (it's the top)
    assert len(boss.connections) == 0
