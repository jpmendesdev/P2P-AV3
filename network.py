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
            raise ValueError(
                f"Não são permitidos laços (aresta de {node1} para si mesmo)"
            )

        self.nodes[node1].neighbors.add(node2)
        self.nodes[node2].neighbors.add(node1)

    def load_config(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.num_nodes = config.get("num_nodes", 0)
        self.min_neighbors = config.get("min_neighbors", 0)
        self.max_neighbors = config.get("max_neighbors", float("inf"))

        self.nodes = {}

        resources_dict = config.get("resources", {})

        for node_id, res_val in resources_dict.items():
            node_id_str = str(node_id).strip()
            self.add_node(node_id_str)

            if isinstance(res_val, str):
                resources = [
                    r.strip()
                    for r in res_val.split(",")
                    if r.strip()
                ]
            elif isinstance(res_val, list):
                resources = [
                    str(r).strip()
                    for r in res_val
                    if str(r).strip()
                ]
            else:
                resources = []

            for resource in resources:
                self.add_resource(node_id_str, resource)

        edges_list = config.get("edges", [])

        for edge in edges_list:

            if isinstance(edge, str):
                parts = [
                    p.strip()
                    for p in edge.split(",")
                    if p.strip()
                ]

                if len(parts) != 2:
                    raise ValueError(f"Aresta inválida: {edge}")

                n1, n2 = parts

            elif isinstance(edge, list) or isinstance(edge, tuple):

                if len(edge) != 2:
                    raise ValueError(f"Aresta inválida: {edge}")

                n1 = str(edge[0]).strip()
                n2 = str(edge[1]).strip()

            else:
                raise ValueError(f"Formato inválido: {edge}")

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
            raise ValueError("A rede não possui nós")

        if len(self.nodes) != self.num_nodes:
            raise ValueError(
                f"Número de nós inválido "
                f"({len(self.nodes)} != {self.num_nodes})"
            )

        if not self.is_connected():
            raise ValueError("A rede está desconectada")

        for node in self.nodes.values():

            degree = len(node.neighbors)

            if degree < self.min_neighbors:
                raise ValueError(
                    f"O nó {node.id} possui menos vizinhos "
                    f"que o mínimo permitido"
                )

            if degree > self.max_neighbors:
                raise ValueError(
                    f"O nó {node.id} possui mais vizinhos "
                    f"que o máximo permitido"
                )

            if not node.resources:
                raise ValueError(
                    f"O nó {node.id} não possui recursos"
                )

        return True

    # =========================================================
    # FLOODING
    # =========================================================

    def flooding(self, start_node, resource_id, ttl):

        if start_node not in self.nodes:
            raise ValueError("Nó inicial inexistente")

        search_steps = []

        queue = deque([(start_node, ttl, None)])

        visited = set()

        parents = {start_node: None}

        messages = 0

        involved = set()

        if resource_id in self.nodes[start_node].resources:

            search_steps.append(
                f"Recurso {resource_id} já estava em {start_node}"
            )

            return {
                "found": True,
                "owner": start_node,
                "messages": 0,
                "nodes_involved": 1,
                "path": [start_node],
                "steps": search_steps
            }

        found_node = None

        while queue:

            current, current_ttl, parent = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            involved.add(current)

            search_steps.append(
                f"Visitando {current} "
                f"(TTL restante: {current_ttl})"
            )

            node = self.nodes[current]

            if resource_id in node.resources:

                search_steps.append(
                    f"Recurso {resource_id} encontrado em {current}"
                )

                found_node = current
                break

            if current_ttl <= 0:

                search_steps.append(
                    f"TTL expirou em {current}"
                )

                continue

            for neighbor in node.neighbors:

                if neighbor != parent:

                    messages += 1

                    search_steps.append(
                        f"{current} enviou consulta para {neighbor}"
                    )

                    if neighbor not in parents:
                        parents[neighbor] = current

                    queue.append(
                        (neighbor, current_ttl - 1, current)
                    )

        if found_node:

            path = []

            curr = found_node

            while curr is not None:
                path.append(curr)
                curr = parents[curr]

            path.reverse()

            response_path = list(reversed(path))

            search_steps.append(
                "Caminho de resposta: "
                + " -> ".join(response_path)
            )

            for i in range(len(path) - 1):

                self.nodes[path[i]].cache[resource_id] = path[i + 1]

                search_steps.append(
                    f"Cache atualizado em {path[i]}: "
                    f"{resource_id} -> {path[i+1]}"
                )

            response_messages = len(path) - 1

            total_messages = messages + response_messages

            return {
                "found": True,
                "owner": found_node,
                "messages": total_messages,
                "nodes_involved": len(involved),
                "path": path,
                "steps": search_steps
            }

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "path": [],
            "steps": search_steps
        }

    # =========================================================
    # INFORMED FLOODING
    # =========================================================

    def informed_flooding(self, start_node, resource_id, ttl):

        result = self.flooding(start_node, resource_id, ttl)

        result["steps"].insert(
            0,
            "[Informed Flooding] Utilizando cache quando disponível"
        )

        return result

    # =========================================================
    # RANDOM WALK
    # =========================================================

    def random_walk(self, start_node, resource_id, ttl):

        if start_node not in self.nodes:
            raise ValueError("Nó inicial inexistente")

        search_steps = []

        current = start_node

        path = [current]

        involved = {current}

        messages = 0

        prev = None

        current_ttl = ttl

        while current_ttl >= 0:

            search_steps.append(
                f"Visitando {current} "
                f"(TTL restante: {current_ttl})"
            )

            if resource_id in self.nodes[current].resources:

                search_steps.append(
                    f"Recurso {resource_id} encontrado em {current}"
                )

                response_messages = len(path) - 1

                total_messages = messages + response_messages

                return {
                    "found": True,
                    "owner": current,
                    "messages": total_messages,
                    "nodes_involved": len(involved),
                    "path": path,
                    "steps": search_steps
                }

            node = self.nodes[current]

            neighbors = list(node.neighbors)

            if prev in neighbors and len(neighbors) > 1:
                neighbors.remove(prev)

            if not neighbors:
                break

            next_node = random.choice(neighbors)

            search_steps.append(
                f"{current} encaminhou busca para {next_node}"
            )

            messages += 1

            prev = current

            current = next_node

            path.append(current)

            involved.add(current)

            current_ttl -= 1

        search_steps.append("Busca encerrada sem sucesso")

        return {
            "found": False,
            "owner": None,
            "messages": messages,
            "nodes_involved": len(involved),
            "path": [],
            "steps": search_steps
        }

    # =========================================================
    # INFORMED RANDOM WALK
    # =========================================================

    def informed_random_walk(self, start_node, resource_id, ttl):

        result = self.random_walk(start_node, resource_id, ttl)

        result["steps"].insert(
            0,
            "[Informed Random Walk] Utilizando cache quando disponível"
        )

        return result
