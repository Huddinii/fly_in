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


class Map(BaseModel):
    drones: int
    hubs: list[Hub]
    connections: list[Connection]
    positions: list[Drone]

    @model_validator(mode='after')
    def map_validator(self) -> "Map":
        hub_names = [x.name for x in self.hubs]
        for c in self.connections:
            if (c.hub_from not in hub_names
                    or c.hub_to not in hub_names):
                raise ValueError(f"Invalid Connection {c}:"
                                 " Trying to connect non existent Hub")
        start, end = False
        for h in self.hubs:
            if h.start:
                start = True
            if h.end:
                end = True
        if not start:
            raise ValueError("There is no Start Hub in the Map")
        if not end:
            raise ValueError("There is no End Hub in the Map")
        for i in range(1, self.drones + 1):
            self.positions.append({"name": f"d{i}"})
        return self
