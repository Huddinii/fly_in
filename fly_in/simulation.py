from solver import Solver
from map import Map
from parsing import Parser, ParsingError
from pydantic import ValidationError


class Drone:
    name: str
    location: str
    finished: bool = False
    moved: bool = False
    blocked: bool = False
    clear: bool = False
    allowed: set[str] = set()

    def set_allowed(self, allowed: set[str]):
        self.allowed = self.allowed + allowed


class Simulation:
    pars = Parser()
    solver = None

    def load_map(self):
        try:
            self.pars.parse_file("maps/hard/03_ultimate_challenge.txt")
            # maps/easy/02_simple_fork.txt
            # maps/hard/03_ultimate_challenge.txt
            map = Map(**self.pars.map)
            self.solver = Solver(map)
            path = self.solver.solve()
        except ParsingError as e:
            print(e)
        except ValueError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except RuntimeError as e:
            print(e)
        else:
            print(path)

    def turn(self):
        ...
