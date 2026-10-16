from map import Map, Solver
from parsing import Parser, ParsingError


pars = Parser()
try:
    pars.parse_file("maps/easy/02_simple_fork.txt")
    map = Map(**pars.map)
    solve = Solver(map)
    solve.bfs()
except ParsingError as e:
    print(e)
else:
    print(solve.valid)
