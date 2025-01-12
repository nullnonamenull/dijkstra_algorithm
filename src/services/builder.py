import pandas as pd
from geopy.distance import geodesic

from src.domain.graph import Graph


def build_full_polish_graph(polish_df: pd.DataFrame) -> Graph:
    g = Graph()
    city_names = polish_df["city"].tolist()

    for i in range(len(city_names)):
        for j in range(i + 1, len(city_names)):
            city_a = city_names[i]
            city_b = city_names[j]

            row_a = polish_df[polish_df["city"] == city_a].iloc[0]
            row_b = polish_df[polish_df["city"] == city_b].iloc[0]

            lat_a, lng_a = row_a["lat"], row_a["lng"]
            lat_b, lng_b = row_b["lat"], row_b["lng"]

            dist_km = geodesic((lat_a, lng_a), (lat_b, lng_b)).km
            g.add_edge(city_a, city_b, dist_km)

    return g
