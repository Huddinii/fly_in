from map import Map
from parsing import Parser, ParsingError


pars = Parser()
try:
    pars.parse_file("maps/hard/01_maze_nightmare.txt")
    map = Map(**pars.map)
except ParsingError as e:
    print(e)
else:
    print(map)
