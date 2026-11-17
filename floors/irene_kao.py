"""5th Floor Comics: a bullpen, an ink room, and a gallery.

Three rooms side by side. You come off the WEST elevator into the Bullpen, walk east through the Ink Room
into the Gallery, and get on the EAST elevator. The digit of the door code is on the "original page" plinth
at the top of the Ink Room's ledges.
"""
import math

import pygame

from engine import config as C
from engine.kit import (Bookshelf, CeilingLight, Couch, Crusher, Desk, Easel, FilingCabinet, PatrolBot, Plant,
                        Plinth, Poster, Sign, Window)
from engine.room import Platform, Room

NAME = "5th Floor Comics"              # the name on the elevator panel
AUTHOR = "Irene Kao"                   # your name

INK = (14, 14, 18)                     # the black of inked comic linework
PAPER = (250, 248, 236)                # speech-balloon paper


def comic_wall(base, dot):
    """A halftone comic wall inside an ink frame. Built once in build(), then blitted every frame."""
    surf = pygame.Surface((C.W, C.H))
    surf.fill(base)
    step = 14
    for row, y in enumerate(range(0, C.FLOOR_Y, step)):
        offset = step // 2 if row % 2 else 0
        for x in range(-step, C.W + step, step):
            pygame.draw.circle(surf, dot, (x + offset, y), 2)
    pygame.draw.rect(surf, INK, surf.get_rect(), 8)
    return surf


class Burst:
    """A comic sound-effect burst (POW!, BAM!). x, y is its centre. Decor: only looked at."""

    def __init__(self, x, y, text, fill):
        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        points = []
        for i in range(24):
            r = 58 if i % 2 == 0 else 40
            a = math.pi * 2 * i / 24
            points.append((60 + r * math.cos(a), 60 + r * math.sin(a)))
        pygame.draw.polygon(self.image, fill, points)
        pygame.draw.polygon(self.image, INK, points, 4)
        font = pygame.font.Font(None, 24)
        font.set_bold(True)
        label = font.render(text, True, INK)
        self.image.blit(label, label.get_rect(center=(60, 60)))
        self.pos = (int(x) - 60, int(y) - 60)

    def draw(self, surf):
        surf.blit(self.image, self.pos)


class Bubble:
    """A speech balloon with a tail. x, y is its top-left corner. Decor: only looked at."""

    def __init__(self, x, y, text):
        label = pygame.font.Font(None, 28).render(text, True, INK)
        w, h = label.get_width() + 24, label.get_height() + 16
        self.image = pygame.Surface((w, h + 16), pygame.SRCALPHA)
        body = pygame.Rect(0, 0, w, h)
        pygame.draw.rect(self.image, PAPER, body, border_radius=12)
        pygame.draw.rect(self.image, INK, body, 3, border_radius=12)
        tail = [(w // 3, h - 2), (w // 3 + 14, h - 2), (w // 3 - 6, h + 14)]
        pygame.draw.polygon(self.image, PAPER, tail)
        pygame.draw.lines(self.image, INK, False, [tail[0], tail[2], tail[1]], 3)
        self.image.blit(label, label.get_rect(center=body.center))
        self.pos = (int(x), int(y))

    def draw(self, surf):
        surf.blit(self.image, self.pos)


# --- Room 1: the West elevator is through its left edge ---

class Bullpen(Room):
    title = "Bullpen"

    def build(self):
        self.comic_bg = comic_wall((30, 44, 96), (48, 70, 134))
        self.decor += [
            Sign(330, 46, "THE BULLPEN!", (255, 214, 40)),
            Poster(110, 80, "POW!", (226, 48, 48)),
            Poster(200, 80, "BAM!", (40, 120, 230)),
            Bubble(290, 190, "DEADLINE!"),
            Burst(500, 160, "ZAP!", (255, 214, 40)),
            Window(640, 70, seed=3),
            CeilingLight(480),
        ]
        self.platforms.append(Platform(400, 410, 200))
        self.furniture += [
            Desk(120, C.FLOOR_Y, "inking desk"),
            Desk(430, 410, "pencil desk"),
            Bookshelf(740, C.FLOOR_Y, "back issues"),
            Plant(830, C.FLOOR_Y),
        ]
        self.hazards.append(PatrolBot(360, C.FLOOR_Y, left=260, right=700, speed=80))

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))


# --- Room 2: the digit is on the top ledge ---

class InkRoom(Room):
    title = "Ink Room"

    def build(self):
        self.comic_bg = comic_wall((20, 62, 64), (34, 96, 94))
        self.decor += [
            Sign(360, 46, "INK ROOM!", (120, 240, 210)),
            Poster(560, 80, "ZAP!", (240, 140, 40)),
            Bubble(90, 150, "SHH..."),
            Burst(820, 170, "INK!", (240, 140, 40)),
            CeilingLight(320),
        ]
        # Each ledge is one jump (about 90 px) above the last, so you can climb them in order.
        self.platforms += [
            Platform(90, 410, 200),
            Platform(380, 330, 200),
            Platform(640, 250, 230),
        ]
        self.furniture += [
            Easel(110, 410, "sketch easel"),
            FilingCabinet(430, 330, "ink drawer"),
            Plinth(700, 250, "original page", holds_piece=True),
            Desk(300, C.FLOOR_Y, "light table"),
            Couch(600, C.FLOOR_Y, "reading couch"),
        ]
        self.hazards.append(PatrolBot(180, C.FLOOR_Y, left=90, right=280, speed=80))

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))


# --- Room 3: the East elevator is through its right edge ---

class Gallery(Room):
    title = "Gallery"

    def build(self):
        self.comic_bg = comic_wall((90, 28, 68), (128, 48, 98))
        self.decor += [
            Sign(330, 46, "THE GALLERY!", (255, 240, 120)),
            Poster(120, 80, "END", (200, 70, 60)),
            Window(600, 70, seed=7),
            Burst(820, 150, "WHAM!", (255, 240, 120)),
            CeilingLight(480),
        ]
        self.platforms.append(Platform(300, 410, 180))
        self.furniture += [
            Plinth(120, C.FLOOR_Y, "panel one"),
            Plinth(330, 410, "panel two"),
            Bookshelf(560, C.FLOOR_Y, "bound volumes"),
            Plant(800, C.FLOOR_Y),
        ]
        self.hazards += [
            PatrolBot(260, C.FLOOR_Y, left=220, right=540, speed=70),
            Crusher(700, y_top=180, w=50, h=40),
        ]

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))


ROOMS = [Bullpen, InkRoom, Gallery]     # west to east
