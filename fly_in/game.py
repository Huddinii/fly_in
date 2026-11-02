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
        levels: Any = None
        sim = None
        running = True
        focus = 0
        i = 0

        if len(argv) > 1:
            level = argv[1]

        while running:
            i += 1
            screen.blit(bg, (0, 0))

            if difficulty is None and level is None:
                self.load_select(screen, difficulties, focus)
            if difficulty is not None and level is None:
                self.load_select(screen, levels, focus)
            if level is not None and sim is None:
                success, out = self.load_map(level)
                if success:
                    sim = out
                else:
                    self.display_err(screen, out)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q:
                            running = False
                        case pygame.K_h:
                            if level is not None:
                                level = None
                            elif difficulty is not None:
                                difficulty = None
                            focus = 0
                        case pygame.K_j:
                            if difficulty is None:
                                if focus < len(difficulties[1]) - 1:
                                    focus += 1
                                else:
                                    focus = 0
                            else:
                                if focus < len(levels[1]) - 1:
                                    focus += 1
                                else:
                                    focus = 0
                        case pygame.K_k:
                            if difficulty is None:
                                if focus > 0:
                                    focus -= 1
                                else:
                                    focus = len(difficulties[1]) - 1
                            else:
                                if focus > 0:
                                    focus -= 1
                                else:
                                    focus = len(levels[1]) - 1
                        case pygame.K_l:
                            if difficulty is None:
                                difficulty = (difficulties[0]
                                              + '/' + difficulties[1][focus])
                                levels = self.pars.get_maps(difficulty)
                                focus = 0
                            elif level is None:
                                level = (levels[0] + '/' + levels[1][focus])
                                focus = 0
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
            # if i % 60 == 0:
            #     print("run")
            #     i = 0
            self.show_instructions(screen, level)
            pygame.display.flip()
        pygame.quit()

    def run_sim(self, sim: Simulation) -> None:
        ...

    def show_instructions(self, screen: pygame.surface.Surface,
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

    def load_select(self, screen: pygame.surface.Surface, choices:
                    tuple[str, list[str]], focus: int) -> None:
        fontL = pygame.font.Font(None, size=80)
        fontS = pygame.font.Font(None, size=60)
        texts = []
        if choices[0].find('/') == -1:
            select = fontL.render("Select difficulty:", True, "white")
        else:
            select = fontL.render("Select level:", True, "white")
        screen.blit(select, (20, 20))
        for i in range(len(choices[1])):
            if focus == i:
                texts.append(fontS.render(choices[1][i], True, "blue"))
            else:
                texts.append(fontS.render(choices[1][i], True, "white"))
        for i in range(len(texts)):
            screen.blit(texts[i], (40, 120 + (100 * i)))

    def load_map(self, file: str) -> tuple[bool, Any]:
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
            return (False, e)
        except ValidationError as e:
            print(e)
            return (False, e)
        except RuntimeError as e:
            print(e)
            return (False, e)
        else:
            dist = self.solver.distance
            valid = self.solver.valid
            sim = Simulation(map, path, dist, valid)
            sim.start()
            return (True, sim)

    def display_err(self, screen: pygame.surface.Surface, err: str) -> None:
        fontL = pygame.font.Font(None, size=80)
        fontS = pygame.font.Font(None, size=60)
        select = fontL.render("Error:", True, "white")
        errmsg = fontS.render(err, True, "white")
        screen.blit(select, (20, 20))
        screen.blit(errmsg, (40, 120))
