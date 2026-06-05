from collections import deque
import random
import yaml
from node import Node


class P2PNetwork:
    def __init__(self):
        self.nodes = {}
        self.min_neighbors = 0
        self.max_neighbors = float("inf")

    def add_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)

    def add_resource(self, node_id, resource):
        self.nodes[node_id].resources.add(resource)

    def add_edge(self, node1, node2):
        if node1 == node2:
            raise ValueError("Não são permitidos laços")

        self.nodes[node1].neighbors.add(node2)
        self.nodes[node2].neighbors.add(node1)

    def load_config(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.min_neighbors = config["min_neighbors"]
        self.max_neighbors = config["max_neighbors"]

        for node_id in config["resources"]:
            self.add_node(node_id)

        for node_id, resources in config["resources"].items():
            for resource in resources:
                self.add_resource(node_id, resource)

        for node1, node2 in config["edges"]:
            self.add_edge(node1, node2)

    def is_connected(self):
        if not self.nodes:
            return True

        start = next(iter(self.nodes))

        visited = {start}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            for neighbor in self.nodes[current].neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == len(self.nodes)

    def validate(self):
        if not self.is_connected():
            raise ValueError("Rede desconectada")

        for node in self.nodes.values():
            degree = len(node.neighbors)

            if degree < self.min_neighbors:
                raise ValueError(
                    f"{node.id} possui poucos vizinhos"
                )

            if degree > self.max_neighbors:
                raise ValueError(
                    f"{node.id} possui muitos vizinhos"
                )

            if not node.resources:
                raise ValueError(
                    f"{node.id} não possui recursos"
                )

        return True

    def flooding(self, start_node, resource_id, ttl):
        queue = deque([(start_node, ttl)])

        visited = set()
        involved = set()

        messages = 0

        while queue:
            current, current_ttl = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            involved.add(current)

            node = self.nodes[current]

            if resource_id in node.resources:
                return {
                    "found": True,
                    "owner": current,
                    "messages": messages,
                    "nodes_involved": len(involved),
                    "visited_nodes": involved
                }

            if current_ttl <= 0:
                continue

            for neighbor in node.neighbors:
                messages += 1
                queue.append(
                    (neighbor, current_ttl - 1)
                )

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "visited_nodes": involved
        }

    def random_walk(self, start_node, resource_id, ttl):
        current = start_node

        involved = {current}
        messages = 0

        while ttl >= 0:
            node = self.nodes[current]

            if resource_id in node.resources:
                return {
                    "found": True,
                    "owner": current,
                    "messages": messages,
                    "nodes_involved": len(involved),
                    "visited_nodes": involved
                }

            if ttl == 0 or not node.neighbors:
                break

            current = random.choice(
                list(node.neighbors)
            )

            involved.add(current)

            messages += 1
            ttl -= 1

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "visited_nodes": involved
        }

    def update_cache(
        self,
        involved_nodes,
        resource_id,
        owner
    ):
        for node_id in involved_nodes:
            self.nodes[node_id].cache[
                resource_id
            ] = owner

    def informed_flooding(
        self,
        start_node,
        resource_id,
        ttl
    ):
        start = self.nodes[start_node]

        if resource_id in start.cache:
            return {
                "found": True,
                "owner": start.cache[resource_id],
                "messages": 0,
                "nodes_involved": 1,
                "visited_nodes": {start_node},
                "cache_hit": True
            }

        result = self.flooding(
            start_node,
            resource_id,
            ttl
        )

        if result["found"]:
            self.update_cache(
                result["visited_nodes"],
                resource_id,
                result["owner"]
            )

        result["cache_hit"] = False

        return result

    def informed_random_walk(
        self,
        start_node,
        resource_id,
        ttl
    ):
        start = self.nodes[start_node]

        if resource_id in start.cache:
            return {
                "found": True,
                "owner": start.cache[resource_id],
                "messages": 0,
                "nodes_involved": 1,
                "visited_nodes": {start_node},
                "cache_hit": True
            }

        result = self.random_walk(
            start_node,
            resource_id,
            ttl
        )

        if result["found"]:
            self.update_cache(
                result["visited_nodes"],
                resource_id,
                result["owner"]
            )

        result["cache_hit"] = False

        return result

    def search(
        self,
        node_id,
        resource_id,
        ttl,
        algo
    ):
        if algo == "flooding":
            return self.flooding(
                node_id,
                resource_id,
                ttl
            )

        elif algo == "random_walk":
            return self.random_walk(
                node_id,
                resource_id,
                ttl
            )

        elif algo == "informed_flooding":
            return self.informed_flooding(
                node_id,
                resource_id,
                ttl
            )

        elif algo == "informed_random_walk":
            return self.informed_random_walk(
                node_id,
                resource_id,
                ttl
            )

        raise ValueError(
            f"Algoritmo inválido: {algo}"
        )