import pytest

from src.domain.graph import Graph
from src.services.dijkstra_service import dijkstra, reconstruct_path


def test_dijkstra_basic():
    g = Graph()
    g.add_edge("A", "B", 1.0)
    g.add_edge("B", "C", 2.0)
    g.add_edge("A", "C", 3.5)

    distances, predecessors = dijkstra(g, "A")
    assert distances[g.city_to_id["C"]] == 3.0  # A->B->C = 1.0 + 2.0


def test_reconstruct_path():
    g = Graph()
    g.add_edge("A", "B", 1.0)
    g.add_edge("B", "C", 2.0)
    distances, predecessors = dijkstra(g, "A")
    path = reconstruct_path(g, "A", "C", predecessors)
    assert path == ["A", "B", "C"]


def test_missing_city():
    g = Graph()
    g.add_city("A")
    # dijkstra na miasto, którego nie ma
    with pytest.raises(ValueError):
        dijkstra(g, "XYZ")
