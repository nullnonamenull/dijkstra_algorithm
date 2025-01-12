from src.services.builder import build_full_polish_graph
from src.services.dijkstra_service import dijkstra, reconstruct_path
from src.services.visualization import (
    visualize_full_graph_with_path,
    visualize_subgraph_with_path,
    visualize_path_on_folium
)
from src.utils.data_loader import load_csv


def main():
    file_path = "../data/worldcities.csv"
    df = load_csv(file_path)
    polish_df = df[df["country"] == "Poland"].copy()

    full_graph = build_full_polish_graph(polish_df)

    cities_to_visit = [
        "Warsaw", "Białystok", "Gdańsk", "Szczecin", "Poznań", "Wrocław", "Katowice", "Kraków", "Lublin", "Rzeszów"
    ]

    full_path = []
    total_distance = 0.0

    for i in range(len(cities_to_visit) - 1):
        source_city = cities_to_visit[i]
        target_city = cities_to_visit[i + 1]

        distances, predecessors = dijkstra(full_graph, source_city)
        segment_path = reconstruct_path(full_graph, source_city, target_city, predecessors)
        segment_distance = distances[full_graph.city_to_id[target_city]]

        if i == 0:
            full_path.extend(segment_path)
        else:
            full_path.extend(segment_path[1:])

        total_distance += segment_distance

    print(f"Shortest path visiting {len(cities_to_visit)} cities: {' -> '.join(full_path)}")
    print(f"Total distance: {total_distance:.2f} km")

    visualize_full_graph_with_path(
        full_graph,
        polish_df,
        full_path,
        title="Shortest Path Visiting 10 Polish Cities"
    )

    visualize_subgraph_with_path(
        full_graph,
        polish_df,
        full_path,
        title="Subgraph of Shortest Path (Visited Cities)"
    )

    visualize_path_on_folium(
        polish_df,
        full_path,
        out_html="polish_cities_path.html"
    )


if __name__ == "__main__":
    main()
