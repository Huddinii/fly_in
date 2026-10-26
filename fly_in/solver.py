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
    solutions = []
    valid = set()
    distance = {}
    shortest = []

    def __init__(self, map: Map):
        self.map = map

    def bfs(self) -> None:
        hubs = []
        start = Node(self.map.get_start().name)
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
        parent = {}
        q = []
        for h in self.valid:
            self.distance.update({h: 999})
            parent.update({h: None})
            q.append(h)
        self.distance[self.map.get_start().name] = 0
        while len(q) > 0:
            cur = self.get_smallest(self.distance, q)
            q.remove(cur)
            for hub in self.map.get_connected(cur):
                if hub in q and self.map.get_zone(hub) is not Zone.BLOCKED:
                    z = self.map.get_zone(hub)
                    match z:
                        case Zone.RESTRICTED:
                            dist = 5
                        case Zone.NORMAL:
                            dist = 3
                        case Zone.PRIORITY:
                            dist = 1
                    length = self.distance[cur] + dist
                    if length < self.distance[hub]:
                        self.distance[hub] = length
                        parent[hub] = cur
        path = self.map.get_end()
        self.shortest.append(path)
        while (p := parent[path]) is not None:
            self.shortest.append(p)
            path = p
        self.shortest.reverse()

    def solve(self):
        self.bfs()
        if len(self.solutions) == 0:
            raise RuntimeError("No valid Path found")
        return self.dijkstra()

    def get_smallest(self, distance: dict[str, int], q: list[str]) -> str:
        smallest = max(distance, key=distance.get)
        for name in q:
            if distance[name] < distance[smallest]:
                smallest = name
        return smallest
