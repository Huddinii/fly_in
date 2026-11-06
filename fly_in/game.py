from typing import Any
from .solver import Solver
from .parsing import Parser, ParsingError
from pydantic import ValidationError
from .map import Map, Hub, Connection
from .simulation import Simulation
from sys import argv
from math import floor
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
        font = pygame.font.Font(None, size=60)

        difficulty = None
        difficulties = self.pars.get_dificulty()
        level = None
        levels: Any = None
        sim = None
        running = True
        paused = False
        finished = False
        focus = 0
        i = 0

        if len(argv) > 1:
            level = argv[1]

        while running:
            if not paused:
                i += 1
            screen.blit(bg, (0, 0))

            if paused:
                p = font.render("Paused", True, "white")
                screen.blit(p, (1740, 20))
            if difficulty is None and level is None and len(difficulties) > 0:
                self.load_select(screen, difficulties, focus)
            if difficulty is not None and level is None and len(levels) > 0:
                self.load_select(screen, levels, focus)
            if level is not None and sim is None:
                success, out = self.load_map(level)
                if success:
                    sim = out
                else:
                    self.display_err(screen, out)
            if sim is not None:
                self.display_sim(screen, sim, i)
                if i % 120 == 0 and not sim.map_completed():
                    sim.turn()
                if not finished and sim.map_completed():
                    print(f"\nTurns: {sim.turns}")
                    finished = True

            for event in pygame.event.get():
                match event.type:
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_q:
                                running = False
                            case pygame.K_h:
                                if level is not None:
                                    level = None
                                elif difficulty is not None:
                                    difficulty = None
                                if sim is not None:
                                    sim = None
                                    finished = False
                                focus = 0
                            case pygame.K_j:
                                if difficulty is None:
                                    if (len(difficulties) > 0 and
                                            focus < len(difficulties[1]) - 1):
                                        focus += 1
                                    else:
                                        focus = 0
                                else:
                                    if (len(levels) > 0 and
                                            focus < len(levels[1]) - 1):
                                        focus += 1
                                    else:
                                        focus = 0
                            case pygame.K_k:
                                if difficulty is None:
                                    if focus > 0:
                                        focus -= 1
                                    else:
                                        if (len(difficulties) > 0 and
                                                len(difficulties[1]) > 0):
                                            focus = len(difficulties[1]) - 1
                                else:
                                    if focus > 0:
                                        focus -= 1
                                    else:
                                        if (len(levels) > 0 and
                                                len(levels[1]) > 0):
                                            focus = len(levels[1]) - 1
                            case pygame.K_l:
                                if (difficulty is None
                                    and len(difficulties) > 0
                                        and len(difficulties[1]) > 0):
                                    difficulty = (difficulties[0] + '/' +
                                                  difficulties[1][focus])
                                    levels = self.pars.get_maps(difficulty)
                                    focus = 0
                                elif (level is None and levels is not None
                                      and len(levels) > 0
                                      and len(levels[1]) > 0):
                                    level = (levels[0] + '/' +
                                             levels[1][focus])
                                    focus = 0
                            case pygame.K_p:
                                if not paused:
                                    paused = True
                                else:
                                    paused = False
                            case pygame.K_t:
                                if sim is not None and not sim.map_completed():
                                    sim.turn()
                    case pygame.QUIT:
                        running = False
            clock.tick(60)
            self.show_instructions(screen, level)
            pygame.display.flip()
        pygame.quit()

    def display_sim(self, screen: pygame.surface.Surface,
                    sim: Simulation, i: int) -> None:
        font = pygame.font.Font(None, size=60)
        turns = font.render(f"Turn: {sim.turns}", True, "White")
        screen.blit(turns, (20, 20))
        hubimg = pygame.image.load("assets/B10.png").convert()
        min_y = min([x.y for x in sim.map.hubs])
        max_y = max([x.y for x in sim.map.hubs])
        max_x = max([x.x for x in sim.map.hubs])
        diff_y = max_y + min_y / 2 if max_y + min_y != 0 else 0
        if [x.x for x in sim.map.hubs if x.end is True][0] >= 19:
            hubimg = pygame.transform.scale(hubimg,
                                            (hubimg.get_width() / 3,
                                             hubimg.get_height() / 3))
        elif [x.x for x in sim.map.hubs if x.end is True][0] >= 9:
            hubimg = pygame.transform.scale(hubimg,
                                            (hubimg.get_width() / 2,
                                             hubimg.get_height() / 2))
        start_x = (960 - ((hubimg.get_width() * 1.75 * max_x) / 2)
                   - (hubimg.get_width() / 2))
        start_y = (500 - (hubimg.get_height() / 2)
                   - (diff_y * hubimg.get_height()))
        hubimg.set_colorkey((0, 0, 0))
        hubs = []
        for hub in sim.map.hubs:
            pos_x = start_x + ((hubimg.get_width() * 1.75) * hub.x)
            pos_y = start_y + ((hubimg.get_height() * 1.75) * hub.y)
            hubs.append((hub, pos_x, pos_y))
        for con in sim.map.connections:
            hub_from = [x[0] for x in hubs if x[0].name == con.hub_from][0]
            hub_to = [x[0] for x in hubs if x[0].name == con.hub_to][0]
            if hub_from.x == hub_to.x and hub_from.y < hub_to.y:
                from_pos = [(x[1] + (hubimg.get_width() / 2),
                             x[2] + hubimg.get_height())
                            for x in hubs if x[0].name == con.hub_from][0]
                to_pos = [((x[1] + hubimg.get_height() / 2),
                           x[2])
                          for x in hubs if x[0].name == con.hub_to][0]
            elif hub_from.x == hub_to.x and hub_from.y > hub_to.y:
                from_pos = [(x[1] + (hubimg.get_width() / 2),
                             x[2])
                            for x in hubs if x[0].name == con.hub_from][0]
                to_pos = [(x[1] + (hubimg.get_height() / 2),
                           x[2] + hubimg.get_height())
                          for x in hubs if x[0].name == con.hub_to][0]
            elif hub_from.x > hub_to.x:
                from_pos = [(x[1],
                             x[2] + (hubimg.get_height() / 2))
                            for x in hubs if x[0].name == con.hub_from][0]
                to_pos = [(x[1] + hubimg.get_width(),
                           x[2] + (hubimg.get_height() / 2))
                          for x in hubs if x[0].name == con.hub_to][0]
            else:
                from_pos = [(x[1] + hubimg.get_width(),
                             x[2] + (hubimg.get_height() / 2))
                            for x in hubs if x[0].name == con.hub_from][0]
                to_pos = [(x[1],
                           x[2] + (hubimg.get_height() / 2))
                          for x in hubs if x[0].name == con.hub_to][0]
            pygame.draw.aaline(screen, "cyan", from_pos, to_pos, 2)
        for h in hubs:
            screen.blit(self.set_color(hubimg, h[0].color, i), (h[1], h[2]))
        self.display_drones(screen, sim, hubs, hubimg.get_size())

    def display_drones(self, screen: pygame.surface.Surface, sim: Simulation,
                       hubs: list[Any], size: tuple[int, int]) -> None:
        droneimg = pygame.image.load("assets/Drone.png")
        droneimg = pygame.transform.scale(droneimg, (size[0] / 2, size[1] / 2))
        droneimg = pygame.transform.rotate(droneimg, 270)
        font = pygame.font.Font(None, size=20)
        pos: dict[str, int] = {}
        for d in sim.drones:
            d_name = font.render(f"[{d.name}]", True, "White")
            if (type(d.location) is Hub and not d.location.end
                    and not d.location.start):
                if d.location.name not in pos.keys():
                    pos.update({d.location.name: 0})
                else:
                    pos[d.location.name] += 1
                hub = [x for x in hubs if x[0] == d.location][0]
                posx = hub[1]
                posy = hub[2]
                offsetx = (droneimg.get_height()
                           * floor(pos[d.location.name] / 2))
                offsety = ((droneimg.get_width() + 20)
                           * (pos[d.location.name] % 2))
                screen.blit(droneimg, (posx + offsetx, posy + offsety))
                screen.blit(d_name, (posx + offsetx, posy + offsety - 20))
            if type(d.location) is Connection:
                hub_from = [x for x in hubs
                            if x[0].name == d.location.hub_from][0]
                hub_to = [x for x in hubs if x[0].name == d.location.hub_to][0]
                posx1 = hub_from[1]
                posx2 = hub_to[1]
                posy1 = hub_from[2]
                posy2 = hub_to[2]
                posx = posx2 - ((posx2 - posx1 - (size[0] / 2)) / 2)
                posy = posy2 - ((posy2 - posy1 - (size[1] / 2)) / 2)
                screen.blit(droneimg, (posx, posy))
                screen.blit(d_name, (posx, posy - 20))

    def set_color(self, img: pygame.surface.Surface,
                  color: str | None, i: int) -> pygame.surface.Surface:
        if color == "rainbow":
            i = i % 180
            colors = ["red", "green", "blue"]
            color = colors[int(i / 60)]
        imgcpy = pygame.Surface(img.get_size())
        try:
            if color is not None:
                imgcpy.fill(color)
        except ValueError:
            imgcpy.fill("white")
        img.set_colorkey("white")
        imgcpy.set_colorkey((0, 0, 0,))
        imgcpy.blit(img, (0, 0))
        return imgcpy

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
            return (False, e)
        except ValidationError as e:
            return (False, e.errors()[0]['msg'].replace("Value error,", ""))
        except RuntimeError as e:
            return (False, e)
        else:
            dist = self.solver.distance
            valid = self.solver.valid
            sim = Simulation(map, path, dist, valid)
            return (True, sim)

    def display_err(self, screen: pygame.surface.Surface, err: str) -> None:
        fontL = pygame.font.Font(None, size=80)
        fontS = pygame.font.Font(None, size=60)
        select = fontL.render("Error:", True, "white")
        errmsg = fontS.render(str(err), True, "white")
        screen.blit(select, (20, 20))
        screen.blit(errmsg, (40, 120))
