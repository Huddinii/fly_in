from pydantic import BaseModel, model_validator, Field
from enum import Enum


class Zone(Enum):
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'


class Hub(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9_]+$")
    x: int
    y: int
    start: bool = False
    end: bool = False
    color: str | None = None
    max_drones: int = 1
    zone: Zone = Zone.NORMAL
    drones: int = 0


class Connection(BaseModel):
    hub_from: str
    hub_to: str
    capacity: int = 1
    used: int = 0

    def __str__(self) -> str:
        return f"{self.hub_from}-{self.hub_to}"


class Drone(BaseModel):
    name: str
    location: str | None = None
    moved: bool = False
    blocked: bool = False
    clear: bool = False


class Map(BaseModel):
    drones: int
    hubs: list[Hub]
    connections: list[Connection]
    positions: list[Drone] = []

    @model_validator(mode='after')
    def map_validator(self) -> "Map":
        hub_names = [x.name for x in self.hubs]
        for c in self.connections:
            if (c.hub_from not in hub_names
                    or c.hub_to not in hub_names):
                raise ValueError(f"Invalid Connection {c}:"
                                 " Trying to connect non existent Hub")
        start, end = False, False
        for h in self.hubs:
            if h.start:
                start = True
            if h.end:
                end = True
        if not start:
            raise ValueError("There is no Start Hub in the Map")
        if not end:
            raise ValueError("There is no End Hub in the Map")
        for i in range(len(self.hubs)):
            x, y = self.hubs[i].x, self.hubs[i].y
            for j in range(i + 1, len(self.hubs)):
                if x == self.hubs[j].x and y == self.hubs[j].y:
                    raise ValueError("Multiple Hubs with same coordinates:"
                                     f" x = {x}, y = {y}")
        for i in range(1, self.drones + 1):
            self.positions.append({"name": f"d{i}"})
        return self

    def get_start(self) -> str:
        for h in self.hubs:
            if h.start:
                return h.name

    def get_end(self) -> str:
        for h in self.hubs:
            if h.end:
                return h.name

    def get_connected(self, name: str):
        return [x.hub_to for x in self.connections if x.hub_from == name]

    def is_blocked(self, name: str):
        for h in self.hubs:
            if h.name == name:
                if h.zone == Zone.BLOCKED:
                    return True
                return False

    def get_zone(self, name: str):
        for hub in self.hubs:
            if hub.name == name:
                return hub.zone


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
        for h in self.map.hubs:
            distance.update({h.name: 999})
            parent.update({h.name: None})
            q.append(h.name)
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

    def get_smallest(self, distance: dict[str, int], q: list[str]) -> str:
        smallest = max(distance, key=distance.get)
        for name in q:
            if distance[name] < distance[smallest]:
                smallest = name
        return smallest
