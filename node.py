class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.resources = set()
        self.neighbors = set()
        self.cache = {}

    def __repr__(self):
        return f"Node({self.id})"