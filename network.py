from collections import deque
import random
import yaml
from node import Node


class P2PNetwork:
    def __init__(self):
        self.nodes = {}
        self.min_neighbors = 0
        self.max_neighbors = float("inf")
        self.num_nodes = 0

    def add_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)

    def add_resource(self, node_id, resource):
        self.nodes[node_id].resources.add(resource)

    def add_edge(self, node1, node2):
        if node1 == node2:
            raise ValueError(f"Não são permitidos laços (aresta de {node1} para si mesmo)")
        self.nodes[node1].neighbors.add(node2)
        self.nodes[node2].neighbors.add(node1)

    def load_config(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.num_nodes = config.get("num_nodes", 0)
        self.min_neighbors = config.get("min_neighbors", 0)
        self.max_neighbors = config.get("max_neighbors", float("inf"))

        # Re-initialize nodes
        self.nodes = {}

        # Load resources
        resources_dict = config.get("resources", {})
        if not resources_dict:
            resources_dict = {}

        for node_id, res_val in resources_dict.items():
            node_id_str = str(node_id).strip()
            self.add_node(node_id_str)
            if isinstance(res_val, str):
                resources = [r.strip() for r in res_val.split(",") if r.strip()]
            elif isinstance(res_val, list):
                resources = [str(r).strip() for r in res_val if str(r).strip()]
            else:
                resources = []
            
            for resource in resources:
                self.add_resource(node_id_str, resource)

        # Load edges
        edges_list = config.get("edges", [])
        if not edges_list:
            edges_list = []

        for edge in edges_list:
            if isinstance(edge, str):
                parts = [p.strip() for p in edge.split(",") if p.strip()]
                if len(parts) != 2:
                    raise ValueError(f"Aresta inválida no arquivo de configuração: {edge}")
                n1, n2 = parts
            elif isinstance(edge, list) or isinstance(edge, tuple):
                if len(edge) != 2:
                    raise ValueError(f"Aresta inválida no arquivo de configuração: {edge}")
                n1, n2 = str(edge[0]).strip(), str(edge[1]).strip()
            else:
                raise ValueError(f"Formato de aresta inválido no arquivo de configuração: {edge}")

            if n1 == n2:
                raise ValueError(f"Não são permitidos laços (aresta de {n1} para si mesmo)")

            if n1 not in self.nodes:
                self.add_node(n1)
            if n2 not in self.nodes:
                self.add_node(n2)

            self.add_edge(n1, n2)

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
        if not self.nodes:
            raise ValueError("A rede não possui nós cadastrados")

        if len(self.nodes) != self.num_nodes:
            raise ValueError(f"O número de nós na rede ({len(self.nodes)}) difere do parâmetro num_nodes ({self.num_nodes})")

        if not self.is_connected():
            raise ValueError("A rede está particionada (desconectada)")

        for node in self.nodes.values():
            degree = len(node.neighbors)

            if degree < self.min_neighbors:
                raise ValueError(f"O nó {node.id} possui menos vizinhos ({degree}) do que o limite min_neighbors ({self.min_neighbors})")

            if degree > self.max_neighbors:
                raise ValueError(f"O nó {node.id} possui mais vizinhos ({degree}) do que o limite max_neighbors ({self.max_neighbors})")

            if not node.resources:
                raise ValueError(f"O nó {node.id} não possui recursos")

        return True

    def flooding(self, start_node, resource_id, ttl):
        if start_node not in self.nodes:
            raise ValueError(f"O nó inicial '{start_node}' não existe na rede.")

        queue = deque([(start_node, ttl, None)])
        visited = set()
        parents = {start_node: None}
        messages = 0
        involved = set()

        if resource_id in self.nodes[start_node].resources:
            involved.add(start_node)
            return {
                "found": True,
                "owner": start_node,
                "messages": 0,
                "nodes_involved": len(involved),
                "path": [start_node]
            }

        found_node = None
        while queue:
            current, current_ttl, parent = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            involved.add(current)

            node = self.nodes[current]

            if resource_id in node.resources:
                found_node = current
                break

            if current_ttl <= 0:
                continue

            for neighbor in node.neighbors:
                if neighbor != parent:
                    messages += 1
                    if neighbor not in parents:
                        parents[neighbor] = current
                    queue.append((neighbor, current_ttl - 1, current))

        if found_node:
            path = []
            curr = found_node
            while curr is not None:
                path.append(curr)
                curr = parents[curr]
            path.reverse()

            # Cache the path back to the initiator
            for i in range(len(path) - 1):
                self.nodes[path[i]].cache[resource_id] = path[i+1]

            response_messages = len(path) - 1
            total_messages = messages + response_messages

            return {
                "found": True,
                "owner": found_node,
                "messages": total_messages,
                "nodes_involved": len(involved),
                "path": path
            }
        else:
            return {
                "found": False,
                "owner": None,
                "messages": messages,
                "nodes_involved": len(involved),
                "path": []
            }

    def informed_flooding(self, start_node, resource_id, ttl):
        if start_node not in self.nodes:
            raise ValueError(f"O nó inicial '{start_node}' não existe na rede.")

        queue = deque([(start_node, ttl, None)])
        visited = set()
        parents = {start_node: None}
        messages = 0
        involved = set()

        if resource_id in self.nodes[start_node].resources:
            involved.add(start_node)
            return {
                "found": True,
                "owner": start_node,
                "messages": 0,
                "nodes_involved": len(involved),
                "path": [start_node]
            }

        found_node = None
        while queue:
            current, current_ttl, parent = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            involved.add(current)

            node = self.nodes[current]

            if resource_id in node.resources:
                found_node = current
                break

            if current_ttl <= 0:
                continue

            # Informed decision
            cached_hop = node.cache.get(resource_id)
            if cached_hop and cached_hop in node.neighbors and cached_hop != parent:
                messages += 1
                if cached_hop not in parents:
                    parents[cached_hop] = current
                queue.append((cached_hop, current_ttl - 1, current))
            else:
                for neighbor in node.neighbors:
                    if neighbor != parent:
                        messages += 1
                        if neighbor not in parents:
                            parents[neighbor] = current
                        queue.append((neighbor, current_ttl - 1, current))

        if found_node:
            path = []
            curr = found_node
            while curr is not None:
                path.append(curr)
                curr = parents[curr]
            path.reverse()

            for i in range(len(path) - 1):
                self.nodes[path[i]].cache[resource_id] = path[i+1]

            response_messages = len(path) - 1
            total_messages = messages + response_messages

            return {
                "found": True,
                "owner": found_node,
                "messages": total_messages,
                "nodes_involved": len(involved),
                "path": path
            }
        else:
            return {
                "found": False,
                "owner": None,
                "messages": messages,
                "nodes_involved": len(involved),
                "path": []
            }

    def random_walk(self, start_node, resource_id, ttl):
        if start_node not in self.nodes:
            raise ValueError(f"O nó inicial '{start_node}' não existe na rede.")

        current = start_node
        path = [current]
        involved = {current}
        messages = 0

        if resource_id in self.nodes[current].resources:
            return {
                "found": True,
                "owner": current,
                "messages": 0,
                "nodes_involved": len(involved),
                "path": path
            }

        prev = None
        current_ttl = ttl
        while current_ttl > 0:
            node = self.nodes[current]
            neighbors = list(node.neighbors)

            if not neighbors:
                break

            if prev in neighbors and len(neighbors) > 1:
                neighbors.remove(prev)

            next_node = random.choice(neighbors)
            messages += 1
            prev = current
            current = next_node
            path.append(current)
            involved.add(current)
            current_ttl -= 1

            if resource_id in self.nodes[current].resources:
                response_messages = len(path) - 1
                total_messages = messages + response_messages

                for i in range(len(path) - 1):
                    self.nodes[path[i]].cache[resource_id] = path[i+1]

                return {
                    "found": True,
                    "owner": current,
                    "messages": total_messages,
                    "nodes_involved": len(involved),
                    "path": path
                }

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "path": []
        }

    def informed_random_walk(self, start_node, resource_id, ttl):
        if start_node not in self.nodes:
            raise ValueError(f"O nó inicial '{start_node}' não existe na rede.")

        current = start_node
        path = [current]
        involved = {current}
        messages = 0

        if resource_id in self.nodes[current].resources:
            return {
                "found": True,
                "owner": current,
                "messages": 0,
                "nodes_involved": len(involved),
                "path": path
            }

        prev = None
        current_ttl = ttl
        while current_ttl > 0:
            node = self.nodes[current]
            neighbors = list(node.neighbors)

            if not neighbors:
                break

            cached_hop = node.cache.get(resource_id)
            if cached_hop and cached_hop in neighbors and cached_hop != prev:
                next_node = cached_hop
            else:
                if prev in neighbors and len(neighbors) > 1:
                    neighbors.remove(prev)
                next_node = random.choice(neighbors)

            messages += 1
            prev = current
            current = next_node
            path.append(current)
            involved.add(current)
            current_ttl -= 1

            if resource_id in self.nodes[current].resources:
                response_messages = len(path) - 1
                total_messages = messages + response_messages

                for i in range(len(path) - 1):
                    self.nodes[path[i]].cache[resource_id] = path[i+1]

                return {
                    "found": True,
                    "owner": current,
                    "messages": total_messages,
                    "nodes_involved": len(involved),
                    "path": path
                }

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "path": []
        }