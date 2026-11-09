*This project has been created as part of the 42 curriculum by lhutter.*

# Fly-In - Drones are interesting

## Description

The goal of this project is to design an efficient drone routing system that navigates multiple drones through connected zones while minimizing simulation turns and handling movement constraints.
The simulated turns should then be visualized in either the Terminal or in a graphical interface.

### Algorithms used

- BFS (Breadth-first search): Used to test all paths and filter which hubs have a direct connection to the goal and which don't.
- Dijkstra: Used to give weights to the different hubs to find the fastest path to the goal.

### Visual Presentation

In this Project I used Pygame-Ce to create a graphical user interface that includes a Difficulty and Level selector, as well as a simulation of where drones are moving in each turn. 
The color of the hubs is clearly shown in this simulation. This makes it a lot easier to follow what happens in each turn as well as if drones are making illegal moves to hubs that are not connected.

### In and output

Maps are made up of Hubs and Connections, connecting the Hubs. As well as Drones that are supposed to find their path through those connections from the start_hub to the end_hub.

Example of a valid map:
```
# Easy Level 2: Simple fork with two paths
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: path_a 2 1 [color=blue]
hub: path_b 2 -1 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-junction [max_link_capacity=2]
connection: junction-path_a
connection: junction-path_b
connection: path_a-goal
connection: path_b-goal
```
The expected output is made up of one line for each turn. In the lines you can find which drone moved where in this specific turn.
Finally the final number of Turns that all Drones took to reach the goal is output.

Expected output:
```
D1-junction D2-junction 
D1-path_a D2-path_b D3-junction D4-junction 
D1-goal D2-goal D3-path_a D4-path_b 
D3-goal D4-goal 

Turns: 4
```
## Instructions

### Make instructions
From the project root, install dependencies:

```bash
make install
```

The project can be launched with either of the following commands:

```bash
make run

make run MAP=<path/to/map>
```
or

```bash
make debug

make debug MAP=<path/to/map>
```
debug uses the python debugger to allow going through the project step by step.

The project can be cleaned up with:
```bash
make clean
```
The project can be linted using flake8 and mypy or mypy --strict with:
```bash
make lint

make lint-strict
```

### Navigation in the GUI

After starting the project a Graphical user interface opens up.
This can be navigated with:
```
q = quit
h = back
j = down
k = up
l = select
```
During the running simulation two new options appear:
```
p = pause
t = turn
```

## Resources

### Websites
- [Pydantic Docs](https://pydantic.dev/docs/validation/latest/get-started/)
- [OS walk](https://www.geeksforgeeks.org/python/os-walk-python/)
- [Pygame-Ce Docs](https://pyga.me/docs/)
- [Pygame Tutorial](https://www.youtube.com/watch?v=blLLtdv4tvo)
- [Color Swapping in Pygame](https://www.youtube.com/watch?v=MLrDR-Mks8I)
- [Hub Asset](https://wenrexa.itch.io/space-full-assets-pack)
- [Space Background](https://digitalmoons.itch.io/free-space-background)
- [Drone Asset](https://foozlecc.itch.io/void-main-ship)
- [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra's_algorithm)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

### AI Usage
No AI was used in the making of this project.
