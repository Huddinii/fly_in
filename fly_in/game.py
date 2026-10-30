from typing import Any
from .solver import Solver
from .parsing import Parser, ParsingError
from pydantic import ValidationError
from .map import Map
from .simulation import Simulation
from sys import argv
import pygame


class Game:
    def __init__(self) -> None:
        self.pars: Parser = Parser()
        self.solver: Any = None

    def start_game(self) -> None:
        pygame.init()
        pygame.display.set_caption("Fly In")

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1920, 1080))

        bg = pygame.image.load("assets/Space_Background2.png").convert()

        difficulty = None
        difficulties = self.pars.get_dificulty()
        level = None
        levels = None
        running = True
        lock = False
        i = 0

        if len(argv) > 1:
            level = argv[1]

        while running:
            i += 1
            screen.blit(bg, (0, 0))

            if difficulty is None and level is None:
                self.load_difficulty_select(screen, difficulties)
            if difficulty is not None and level is None:
                self.load_level_select()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_h:
                        if level is not None and not lock:
                            lock = True
                            level = None
                        elif difficulty is not None and not lock:
                            lock = True
                            difficulty = None
                if event.type == pygame.KEYUP:
                    lock = False
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
            # if i % 60 == 0:
            #     print("run")
            #     i = 0
            self.show_instructions(screen, level)
            pygame.display.flip()
        pygame.quit()

    def run_sim(self, sim) -> None:
        ...

    def show_instructions(self, screen: pygame.Surface,
                          level: str | None) -> None:
        font = pygame.font.Font(None, size=20)
        pygame.draw.line(screen, "white", (0, 1000), (1920, 1000))
        if level is None:
            texts = []
            texts.append(font.render("q: quit", True, "white"))
            texts.append(font.render("h: back", True, "white"))
            texts.append(font.render("j: down", True, "white"))
            texts.append(font.render("k: up", True, "white"))
            texts.append(font.render("l: select", True, "white"))
            i = 0
            for t in texts:
                screen.blit(t, (20 + (int(i / 2) * 80), 1020 + ((i % 2) * 20)))
                i += 1
        else:
            texts = []
            texts.append(font.render("q: quit", True, "white"))
            texts.append(font.render("h: back", True, "white"))
            texts.append(font.render("p: pause", True, "white"))
            texts.append(font.render("t: turn", True, "white"))
            i = 0
            for t in texts:
                screen.blit(t, (20 + (int(i / 2) * 80), 1020 + ((i % 2) * 20)))
                i += 1

    def load_difficulty_select(self, screen: pygame.Surface, difficulties:
                               tuple[str, list[str]]) -> None:
        fontL = pygame.font.Font(None, size=80)
        fontS = pygame.font.Font(None, size=60)
        texts = []
        select = fontL.render("Select difficulty:", True, "white")
        screen.blit(select, (20, 20))
        for d in difficulties[1]:
            texts.append(fontS.render(d, True, "white"))
        for i in range(len(texts)):
            screen.blit(texts[i], (40, 120 + (100 * i)))

    def load_map(self, file: str) -> None:
        try:
            parsed = self.pars.parse_file(file)
            map = Map(**parsed)
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
