from pydantic import BaseModel


class Hub(BaseModel):
    name: str
    x: int
    y: int
    start: bool = False
    end: bool = False
    color: str | None = None
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


if __name__ == "__main__":
    obj = {"drones": "4", "hubs":
           [{"name": "test1",
             "x": "1",
             "y": "2"}],
           "connections": []}
    map = Map(**obj)
    print(map)
