from typing import List

import folium
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from src.domain.graph import Graph


def visualize_full_graph_with_path(
        g: Graph, polish_df: pd.DataFrame, path_cities: List[str],
        title: str = "", figsize=(12, 10)
) -> None:
    # Rysowanie pełnego grafu + wyróżnienie ścieżki
    G_nx = nx.Graph()
    for idx, row in polish_df.iterrows():
        city = row["city"]
        lat = row["lat"]
        lng = row["lng"]
        G_nx.add_node(city, pos=(lng, lat))

    for city_a, a_id in g.city_to_id.items():
        for b_id, w in g.adjacency_list[a_id].items():
            city_b = g.id_to_city[b_id]
            if not G_nx.has_edge(city_a, city_b):
                G_nx.add_edge(city_a, city_b, weight=w)

    pos = nx.get_node_attributes(G_nx, 'pos')

    plt.figure(figsize=figsize)
    nx.draw_networkx_nodes(G_nx, pos, node_color="lightblue", edgecolors="black", node_size=100)
    nx.draw_networkx_edges(G_nx, pos, edge_color="gray", width=0.3)
    nx.draw_networkx_labels(G_nx, pos, font_size=5)

    if len(path_cities) > 1:
        path_edges = list(zip(path_cities, path_cities[1:]))
        nx.draw_networkx_edges(G_nx, pos, edgelist=path_edges, edge_color="red", width=2)
        nx.draw_networkx_nodes(G_nx, pos, nodelist=path_cities, node_color="orange", node_size=150)

    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()


def visualize_subgraph_with_path(
        g: Graph, polish_df: pd.DataFrame, path_cities: List[str],
        title: str = "", figsize=(8, 6)
) -> None:
    # Rysowanie wyłącznie miast ścieżki + ich krawędzi
    subG_nx = nx.Graph()

    for city in path_cities:
        row = polish_df[polish_df["city"] == city].iloc[0]
        lat, lng = row["lat"], row["lng"]
        subG_nx.add_node(city, pos=(lng, lat))

    for i in range(len(path_cities) - 1):
        city_a = path_cities[i]
        city_b = path_cities[i + 1]
        a_id = g.city_to_id[city_a]
        b_id = g.city_to_id[city_b]
        weight = g.adjacency_list[a_id][b_id]
        subG_nx.add_edge(city_a, city_b, weight=weight)

    pos = nx.get_node_attributes(subG_nx, 'pos')

    plt.figure(figsize=figsize)
    nx.draw(subG_nx, pos, with_labels=True, node_color="orange", edge_color="red",
            width=2, node_size=300, font_size=10)

    for i, city in enumerate(path_cities):
        x, y = pos[city]
        plt.text(x, y, str(i + 1), fontsize=8, color="blue", ha="center", va="center")

    plt.title(title, fontsize=12)
    plt.axis("off")
    plt.show()


def visualize_pafth_on_folium(
        polish_df: pd.DataFrame, path_cities: List[str],
        out_html: str = "path.html"
) -> None:
    # Interaktywna mapa Folium
    if len(path_cities) == 0:
        print("No path cities to visualize.")
        return
    if len(path_cities) == 1:
        single_city = path_cities[0]
        row = polish_df[polish_df["city"] == single_city].iloc[0]
        folium.Map(location=[row["lat"], row["lng"]], zoom_start=6).save(out_html)
        print(f"Only one city to visualize. Map saved to {out_html}")
        return

    first_city = path_cities[0]
    row_first = polish_df[polish_df["city"] == first_city].iloc[0]
    map_center = [row_first["lat"], row_first["lng"]]

    m = folium.Map(location=map_center, zoom_start=6)

    coords = []
    for city in path_cities:
        row = polish_df[polish_df["city"] == city].iloc[0]
        coords.append((row["lat"], row["lng"]))

    for i, city in enumerate(path_cities):
        lat, lng = coords[i]
        folium.Marker(
            location=[lat, lng],
            popup=f"{city} (stop #{i + 1})",
            icon=folium.Icon(color="orange", icon="info-sign"),
        ).add_to(m)

    folium.PolyLine(coords, color="red", weight=4, opacity=0.8).add_to(m)

    m.save(out_html)
    print(f"Interactive Folium map with path saved to '{out_html}'.")
