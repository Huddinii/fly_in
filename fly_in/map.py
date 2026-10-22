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


class Map(BaseModel):
    drones: int
    hubs: list[Hub]
    connections: list[Connection]

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

    def get_hub(self, name: str):
        for hub in self.hubs:
            if hub.name == name:
                return hub

    def get_connection(self, hub_from: str, hub_to: str):
        for c in self.connections:
            if c.hub_from == hub_from and c.hub_to == hub_to:
                return c
