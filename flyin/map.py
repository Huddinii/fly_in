class Hub:
    zone = "normal"
    color = None
    max_drones = 1
    def __init__(self, x: int, y: int, start: bool = False,
                 end: bool = False, meta: list[str] | None = None):
        self.x = x
        self.y = y
        self.start = start
        self.end = end
        self.meta = meta


class Connection:
    def __init__(self, hub_from: str, hub_to: str, capacity: int = 1):
        self.hub_from = hub_from
        self.hub_to = hub_to
        self.capacity = capacity


class Map:
    def __init__(self, hubs: list[Hub], connections: list[Connection],
                 drones: int):
        self.hubs = hubs
        self.connections = connections
        self.drones = drones
