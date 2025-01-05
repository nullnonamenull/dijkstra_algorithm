from src.domain.graph import Graph


def test_add_city():
    g = Graph()
    city_id = g.add_city("TestCity")
    assert city_id == 0
    assert g.city_to_id["TestCity"] == 0
    assert g.id_to_city[0] == "TestCity"


def test_add_edge():
    g = Graph()
    g.add_edge("CityA", "CityB", 100.0)
    assert "CityA" in g.city_to_id
    assert "CityB" in g.city_to_id

    a_id = g.city_to_id["CityA"]
    b_id = g.city_to_id["CityB"]
    assert g.adjacency_list[a_id][b_id] == 100.0
    assert g.adjacency_list[b_id][a_id] == 100.0
