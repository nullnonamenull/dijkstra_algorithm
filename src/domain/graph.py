from typing import Dict


class Graph:
    """
    A custom Graph class for storing weighted edges (city to city) in an adjacency list
    and running Dijkstra's algorithm. Each node is identified by an integer.
    """

    def __init__(self) -> None:
        self.adjacency_list: Dict[int, Dict[int, float]] = {}
        self.city_to_id: Dict[str, int] = {}
        self.id_to_city: Dict[int, str] = {}
        self.next_id = 0

    def add_city(self, city_name: str) -> int:
        """
        Add city to graph if not already present; return its ID.
        If the city is new, create an empty adjacency dictionary for it.
        """
        if city_name not in self.city_to_id:
            self.city_to_id[city_name] = self.next_id
            self.id_to_city[self.next_id] = city_name
            self.adjacency_list[self.next_id] = {}
            self.next_id += 1
        return self.city_to_id[city_name]

    def add_edge(self, city_a: str, city_b: str, weight: float) -> None:
        """
        Add an undirected edge between two city names with the given weight.
        If either city does not exist, it will be created.
        """
        a_id = self.add_city(city_a)
        b_id = self.add_city(city_b)
        self.adjacency_list[a_id][b_id] = weight
        self.adjacency_list[b_id][a_id] = weight
