from solver import Solver
from map import Map
from parsing import Parser, ParsingError


class Simulation:
    pars = Parser()
    solver = None

    def simulate(self):
        try:
            self.pars.parse_file("maps/hard/03_ultimate_challenge.txt")
            # maps/easy/02_simple_fork.txt
            # maps/hard/03_ultimate_challenge.txt
            map = Map(**self.pars.map)
            self.solver = Solver(map)
            parent, distance = self.solver.solve()
        except ParsingError as e:
            print(e)
        else:
            print(parent, distance)
