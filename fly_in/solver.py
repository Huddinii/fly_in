from map import Map, Zone


class Node:
    parent = None

    def __init__(self, name) -> None:
        self.name = name

    def check_valid(self, name: str) -> bool:
        par = self.parent
        while par is not None:
            if name == par.name:
                return False
            par = par.parent
        return True


class Solver:
    def __init__(self, map: Map):
        self.map = map
        self.solutions = []
        self.valid = set()

    def bfs(self):
        hubs = []
        start = Node(self.map.get_start())
        hubs.append(start)
        while len(hubs) > 0:
            hub = hubs[0]
            hubs.pop(0)
            if hub.name == self.map.get_end():
                self.solutions.append(hub)
            else:
                for x in self.map.get_connected(hub.name):
                    if hub.check_valid(x) and not self.map.is_blocked(x):
                        next = Node(x)
                        next.parent = hub
                        hubs.append(next)
        for s in self.solutions:
            while s is not None:
                self.valid.add(s.name)
                s = s.parent

    def dijkstra(self):
        distance = {}
        parent = {}
        q = []
        for h in self.valid:
            distance.update({h: 999})
            parent.update({h: None})
            q.append(h)
        distance[self.map.get_start()] = 0
        while len(q) > 0:
            cur = self.get_smallest(distance, q)
            q.remove(cur)
            for hub in self.map.get_connected(cur):
                if hub in q and self.map.get_zone(hub) is not Zone.BLOCKED:
                    length = distance[cur] + (2 if self.map.get_zone(hub)
                                              == Zone.RESTRICTED else 1)
                    if length < distance[hub]:
                        distance[hub] = length
                        parent[hub] = cur
        return parent, distance

    def solve(self):
        self.bfs()
        return self.dijkstra()

    def get_smallest(self, distance: dict[str, int], q: list[str]) -> str:
        smallest = max(distance, key=distance.get)
        for name in q:
            if distance[name] < distance[smallest]:
                smallest = name
        return smallest
