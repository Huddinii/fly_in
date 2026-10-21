from solver import Solver
from map import Map
from parsing import Parser, ParsingError
from pydantic import ValidationError


class Drone:
    finished: bool = False
    moved: bool = False
    blocked: bool = False
    clear: bool = False
    valid: set[str] = set()

    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

    def set_valid(self, valid: set[str]):
        self.valid = self.valid + valid

    def check_available(self, map: Map):
        ...

    def move(self, map: Map):
        ...


class Game:
    pars = Parser()
    solver = None

    def load_map(self):
        try:
            self.pars.parse_file("maps/hard/03_ultimate_challenge.txt")
            # maps/easy/02_simple_fork.txt
            # maps/hard/03_ultimate_challenge.txt
            map = Map(**self.pars.map)
            self.solver = Solver(map)
            self.solver.solve()
            path = self.solver.shortest
        except ParsingError as e:
            print(e)
        except ValueError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except RuntimeError as e:
            print(e)
        else:
            dist = self.solver.distance
            valid = self.solver.valid
            sim = Simulation(map, path, dist, valid)
            sim.start()
            print(path)


class Simulation:
    drones: list[Drone]
    turns: int = 0

    def __init__(self, map: Map, shortest: list[str],
                 distance: dict[str, int], valid: set[str]):
        self.map = map
        self.shortest = shortest
        self.distance = distance
        self.valid = valid

    def start(self):
        self.drones = [Drone(f"D{x}", self.map.get_start())
                       for x in range(1, self.map.drones + 1)]
        for d in self.drones:
            d.set_valid(self.valid)
        while self.map_completed():
            self.turn()
        print(f"Turns: {self.turns}")

    def turn(self):
        self.turns += 1
        while not self.turn_completed():
            d = self.drones[self.get_farthest()]
            d.move(self.map)
            print(f"{d.name}-{d.location}")

    def map_completed(self):
        for d in self.drones:
            if d.clear is False:
                return False
        return True

    def turn_completed(self):
        for d in self.drones:
            if d.moved is False:
                return False
        return True

    def get_farthest(self) -> int:
        i = 0
        drone = self.drones[i]
        while drone.moved:
            i += 1
            drone = self.drones[i]
        dist = self.distance[drone.location]
        for d in self.drones:
            if d.blocked or d.moved or d.clear:
                continue
            if ((new := self.distance[d.location]) > dist and
                    d.check_available(self.map)):
                drone = d
                dist = new
        return self.drones.index(drone)
