from solver import Solver
from map import Map, Hub, Connection, Zone
from parsing import Parser, ParsingError
from pydantic import ValidationError
from time import sleep


class Drone:
    moved: bool = False
    blocked: bool = False
    traveling: bool = False
    clear: bool = False

    def __init__(self, name: str, location: Hub | Connection) -> None:
        self.name = name
        self.location = location
        self.valid: set[str] = set()
        self.distance: dict[str, int]

    def set_valid(self, valid: set[str]) -> None:
        self.valid = self.valid | valid

    def set_distance(self, distance: dict[str, int]) -> None:
        self.distance = distance

    def set_shortest(self, shortest: list[str]) -> None:
        self.shortest = shortest

    def check_available(self, map: Map) -> bool:
        if self.traveling or self.clear or self.blocked or self.moved:
            return False
        return True

    def move(self, map: Map) -> bool:
        if self.traveling:
            self.traveling = False
            self.location.used -= 1
            self.location.traveling.remove(self)
            self.location = map.get_hub(self.location.hub_to)
            self.location.drones += 1
            if self.location.name == map.get_end():
                self.clear = True
            self.moved = True
            return True
        cons = [x for x in map.get_connected(self.location.name)
                if x in self.valid]
        while len(cons) > 0:
            next = None
            for h in cons:
                if h in self.shortest:
                    next = h
                    break
            if next is None:
                next = min({k: v for (k, v) in self.distance.items()
                           if k in cons}, key=self.distance.get)
            hub = map.get_hub(next)
            if hub.zone != Zone.RESTRICTED:
                space = False
                capacity = False
                if hub.drones < hub.max_drones:
                    space = True
                con = map.get_connection(self.location.name, hub.name)
                if con.used < con.capacity:
                    capacity = True
                if space and capacity:
                    if hub.name == map.get_end():
                        self.clear = True
                    con.used += 1
                    self.location.drones -= 1
                    hub.drones += 1
                    self.location = hub
                    self.moved = True
                    return True
            else:
                space = map.has_space(hub)
                capacity = False
                con = map.get_connection(self.location.name, hub.name)
                if con.used < con.capacity:
                    capacity = True
                if space and capacity:
                    self.location.drones -= 1
                    con.used += 1
                    con.traveling.append(self)
                    self.location = con
                    self.moved = True
                    self.traveling = True
                    return True
            cons.remove(next)
        self.blocked = True
        return False


class Game:
    def __init__(self):
        self.pars = Parser()
        self.solver = None

    def load_map(self, map: str):
        try:
            self.pars.parse_file(map)
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
        # except RuntimeError as e:
        #     print(e)
        else:
            dist = self.solver.distance
            valid = self.solver.valid
            sim = Simulation(map, path, dist, valid)
            sim.start()


class Simulation:
    turns: int = 0

    def __init__(self, map: Map, shortest: list[str],
                 distance: dict[str, int], valid: set[str]):
        self.drones: list[Drone]
        self.map = map
        self.shortest = shortest
        self.distance = distance
        self.valid = valid

    def start(self):
        self.drones = [Drone(f"D{x}", self.map.get_start())
                       for x in range(1, self.map.drones + 1)]
        for d in self.drones:
            d.set_valid(set(self.valid))
            d.set_distance(self.distance)
            d.set_shortest(self.shortest)
        while not self.map_completed():
            self.turn()
        print(f"\nTurns: {self.turns}")

    def turn(self):
        self.turns += 1
        d = self.get_farthest()
        while d is not None:
            if d.move(self.map):
                print(f"{d.name}-{d.location.get_name()}", end=' ')
            d = self.get_farthest()
        self.turn_reset()
        print()

    def turn_reset(self):
        for d in self.drones:
            d.moved = False
            d.blocked = False
        for c in self.map.connections:
            c.used = 0

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
        dist = -1
        drone = None
        for d in self.drones:
            if d.blocked or d.moved or d.clear:
                continue
            if d.traveling:
                new = self.distance[d.location.hub_to]
            else:
                new = self.distance[d.location.name]
            if (new > dist):
                drone = d
                dist = new
        return drone
