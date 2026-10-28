from typing import Any
from .solver import Solver
from .parsing import Parser, ParsingError
from pydantic import ValidationError
from .map import Map
from .simulation import Simulation
import pygame


class Game:
    def __init__(self) -> None:
        self.pars: Parser = Parser()
        self.solver: Any = None

    def start_game(self):
        pygame.init()

        clock = pygame.time.Clock()
        # screen = pygame.display.set_mode((1280, 800))
        screen = pygame.display.set_mode((1920, 1080))

        bg = pygame.image.load("assets/Space_Background2.png").convert()
        try:
            open("assets/Space_Background2.png")
        except FileNotFoundError:
            print("err")

        pygame.display.set_caption("Fly In")

        running = True
        while running:
            # screen.fill((255, 255, 255))
            screen.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def load_map(self, file: str) -> None:
        try:
            self.pars.parse_file(file)
            map = Map(**self.pars.map)
            self.solver = Solver(map)
            self.solver.solve()
            path = self.solver.shortest
        except ParsingError as e:
            print(e)
            return (False, e)
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
            return (True, sim)
