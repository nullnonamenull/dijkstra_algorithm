import pandas as pd

from src.services.builder import build_full_polish_graph


def test_build_full_polish_graph():
    data = {
        "city": ["Warsaw", "Kraków"],
        "lat": [52.2297, 50.0647],
        "lng": [21.0122, 19.9450],
        "country": ["Poland", "Poland"]
    }
    df = pd.DataFrame(data)
    g = build_full_polish_graph(df)
    assert len(g.city_to_id) == 2
    assert len(g.adjacency_list) == 2
