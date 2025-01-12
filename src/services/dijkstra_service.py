import heapq
from typing import Dict, Union, Tuple, List

from src.domain.graph import Graph


def dijkstra(graph: Graph, source_city: str) -> Tuple[Dict[int, float], Dict[int, Union[int, None]]]:
    if source_city not in graph.city_to_id:
        raise ValueError(f"Source city '{source_city}' not found in graph.")

    source_id = graph.city_to_id[source_city]

    distances = {node_id: float("inf") for node_id in graph.adjacency_list.keys()}
    predecessors = {node_id: None for node_id in graph.adjacency_list.keys()}
    distances[source_id] = 0.0

    pq = [(0.0, source_id)]

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        if current_dist > distances[current_vertex]:
            continue

        for neighbor, weight in graph.adjacency_list[current_vertex].items():
            alt = current_dist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                predecessors[neighbor] = current_vertex
                heapq.heappush(pq, (alt, neighbor))

    return distances, predecessors


def reconstruct_path(
        graph: Graph, source_city: str, target_city: str,
        predecessors: Dict[int, Union[int, None]]
) -> List[str]:
    if target_city not in graph.city_to_id:
        raise ValueError(f"Target city '{target_city}' not found in graph.")

    source_id = graph.city_to_id[source_city]
    target_id = graph.city_to_id[target_city]

    path_ids = []
    current = target_id
    while current is not None:
        path_ids.append(current)
        current = predecessors[current]

    path_ids.reverse()

    if not path_ids or path_ids[0] != source_id:
        raise ValueError(f"No path from '{source_city}' to '{target_city}' found.")

    return [graph.id_to_city[node_id] for node_id in path_ids]
