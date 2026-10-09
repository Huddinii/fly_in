from pydantic import BaseModel, Optional


class Hub(BaseModel):
    name: str
    x: int
    y: int
    start: bool = False
    end: bool = False
    color: Optional[str] = None
    max_drones: int = 1
    zone: str = "normal"


class Connection(BaseModel):
    hub_from: str
    hub_to: str
    capacity: int = 1


class Map(BaseModel):
    drones: int
    hubs: list[Hub]
    connections: list[Connection]
