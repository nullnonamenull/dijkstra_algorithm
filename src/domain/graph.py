from typing import Dict


class Graph:

    def __init__(self) -> None:
        self.adjacency_list: Dict[int, Dict[int, float]] = {}
        self.city_to_id: Dict[str, int] = {}
        self.id_to_city: Dict[int, str] = {}
        self.next_id = 0

    def add_city(self, city_name: str) -> int:
        if city_name not in self.city_to_id:
            self.city_to_id[city_name] = self.next_id
            self.id_to_city[self.next_id] = city_name
            self.adjacency_list[self.next_id] = {}
            self.next_id += 1
        return self.city_to_id[city_name]

    def add_edge(self, city_a: str, city_b: str, weight: float) -> None:
        a_id = self.add_city(city_a)
        b_id = self.add_city(city_b)
        self.adjacency_list[a_id][b_id] = weight
        self.adjacency_list[b_id][a_id] = weight
