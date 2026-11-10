from pydantic import BaseModel, model_validator, Field
from enum import Enum
from typing import Any


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
    color: str | None = Field(default=None, pattern=r"^[a-zA-Z]+$")
    max_drones: int = Field(default=1, gt=0)
    zone: Zone = Zone.NORMAL
    drones: int = 0

    def get_name(self) -> str:
        return self.name


class Connection(BaseModel):
    hub_from: str
    hub_to: str
    capacity: int = Field(default=1, gt=0)
    used: int = 0
    traveling: list[Any] = []

    def get_name(self) -> str:
        return f"Con_{self.hub_from}-{self.hub_to}"


class Map(BaseModel):
    drones: int = Field(gt=0)
    hubs: list[Hub]
    connections: list[Connection]

    @model_validator(mode='after')
    def map_validator(self) -> "Map":
        hub_names = [x.name for x in self.hubs]
        if len(hub_names) != len(set(hub_names)):
            raise ValueError("Invalid Hub: Multiple Hubs with same Name")
        self.validate_cons(hub_names)
        start, end = False, False
        for h in self.hubs:
            if h.start:
                start = True
                h.max_drones = self.drones
                h.drones = self.drones
            if h.end:
                end = True
                h.max_drones = self.drones
            if h.color is not None:
                h.color = h.color.lower()
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

    def validate_cons(self, hub_names: list[str]) -> None:
        for c in self.connections:
            if (c.hub_from not in hub_names
                    or c.hub_to not in hub_names):
                raise ValueError(f"Invalid Connection {c.get_name()}:"
                                 " Trying to connect non existent Hub")
            if (c.hub_from == c.hub_to):
                raise ValueError(f"Invalid Connection {c.get_name()}:"
                                 " Trying to connect to itself")
            for con in self.connections[self.connections.index(c) + 1:
                                        len(self.connections)]:
                if c.hub_from == con.hub_from and c.hub_to == con.hub_to:
                    raise ValueError(f"Invalid Connection {con.get_name()}:"
                                     f" Duplicate Connection {c.get_name()}"
                                     " found")
                if c.hub_from == con.hub_to and c.hub_to == con.hub_from:
                    raise ValueError(f"Invalid Connection {con.get_name()}:"
                                     f" Duplicate Connection {c.get_name()}"
                                     " found")

    def get_start(self) -> Hub:
        return [h for h in self.hubs if h.start][0]

    def get_end(self) -> Hub:
        return [h for h in self.hubs if h.end][0]

    def get_connected(self, name: str) -> list[str]:
        return [x.hub_to for x in self.connections if x.hub_from == name]

    def is_blocked(self, name: str) -> bool:
        for h in self.hubs:
            if h.name == name:
                if h.zone == Zone.BLOCKED:
                    return True
        return False

    def get_zone(self, name: str) -> Zone:
        return [h.zone for h in self.hubs if h.name == name][0]

    def get_hub(self, name: str) -> Hub:
        return [h for h in self.hubs if h.name == name][0]

    def get_connection(self, hub_from: str, hub_to: str) -> Connection:
        return [c for c in self.connections
                if c.hub_from == hub_from and c.hub_to == hub_to][0]

    def has_space(self, hub: Hub) -> bool:
        cons = [x for x in self.connections if x.hub_to == hub.name]
        traveling = 0
        for c in cons:
            traveling += len(c.traveling)
        if traveling < hub.max_drones:
            return True
        return False
