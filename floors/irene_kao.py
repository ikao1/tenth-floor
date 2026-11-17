"""5th Floor Comics: a bullpen, an ink room, and a gallery.

Three rooms side by side. You come off the WEST elevator into the Bullpen, walk east through the Ink Room
into the Gallery, and get on the EAST elevator. The digit of the door code is on the "original page" plinth
at the top of the Ink Room's ledges.

The villains are the kit's patrol bots and crushers in comic-book costumes. When one catches you, you freeze,
POW! and BAM! pop up around you, and then the engine sends you back.
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
WHITE = (255, 255, 255)
YELLOW = (255, 214, 40)
ORANGE = (255, 110, 50)
GOLD = (230, 190, 70)


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


def place(burst, cx, cy):
    """Move a Burst so its centre is at (cx, cy)."""
    burst.pos = (int(cx) - 60, int(cy) - 60)


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


# --- drawing the villains -----------------------------------------------------------------------------
# Costumes are drawn in fractions of the hit-box: (0, 0) is its top-left, (1, 1) its bottom-right.
# Numbers outside 0..1 are fine, so a cape can hang past the box without changing the hit-box.

def _pts(r, pairs):
    return [(round(r.left + fx * r.w), round(r.top + fy * r.h)) for fx, fy in pairs]


def shape(surf, colour, r, pairs, edge=2):
    """A filled polygon with an ink outline (edge=0 for no outline)."""
    pts = _pts(r, pairs)
    pygame.draw.polygon(surf, colour, pts)
    if edge:
        pygame.draw.polygon(surf, INK, pts, edge)


def disc(surf, colour, r, fx, fy, fr, edge=2):
    """A filled circle, fr is its radius as a fraction of the box width (edge=0 for no outline)."""
    centre = (round(r.left + fx * r.w), round(r.top + fy * r.h))
    radius = max(1, round(fr * r.w))
    pygame.draw.circle(surf, colour, centre, radius)
    if edge:
        pygame.draw.circle(surf, INK, centre, radius, edge)


def stroke(surf, colour, r, a, b, width=2):
    pygame.draw.line(surf, colour, _pts(r, [a])[0], _pts(r, [b])[0], width)


def pencil_thug(surf, inner):
    """The Pencil Thug: a scalloped red cape, a dark coat with a red tie, a domino mask and a pencil."""
    r = inner.rect
    shape(surf, (190, 40, 40), r, [(0.05, 0.28), (0.50, 0.22), (0.95, 0.28), (1.18, 0.98), (1.04, 0.90),
                                   (0.86, 1.02), (0.68, 0.92), (0.50, 1.02), (0.32, 0.92), (0.14, 1.02),
                                   (-0.04, 0.90), (-0.18, 0.98)])
    shape(surf, (46, 42, 62), r, [(0.16, 0.44), (0.84, 0.44), (0.98, 0.98), (0.02, 0.98)])
    shape(surf, WHITE, r, [(0.40, 0.44), (0.60, 0.44), (0.50, 0.68)], edge=1)              # shirt V
    shape(surf, (220, 40, 40), r, [(0.46, 0.50), (0.54, 0.50), (0.57, 0.60), (0.50, 0.68), (0.43, 0.60)], edge=1)
    for fy in (0.80, 0.90):
        disc(surf, WHITE, r, 0.5, fy, 0.025, edge=1)                                        # buttons
    disc(surf, (196, 222, 170), r, 0.50, 0.27, 0.23)                                        # head
    shape(surf, (20, 20, 26), r, [(0.30, 0.16), (0.36, 0.04), (0.50, 0.00), (0.62, 0.04), (0.70, 0.14),
                                  (0.58, 0.10), (0.44, 0.10)], edge=1)                      # quiff
    shape(surf, INK, r, [(0.26, 0.22), (0.74, 0.22), (0.66, 0.34), (0.50, 0.30), (0.34, 0.34)], edge=0)  # mask
    disc(surf, WHITE, r, 0.40, 0.26, 0.05, edge=1)
    disc(surf, WHITE, r, 0.60, 0.26, 0.05, edge=1)
    disc(surf, INK, r, 0.41, 0.27, 0.02, edge=0)
    disc(surf, INK, r, 0.61, 0.27, 0.02, edge=0)
    stroke(surf, INK, r, (0.28, 0.17), (0.44, 0.22), 2)                                     # angry brows
    stroke(surf, INK, r, (0.72, 0.17), (0.56, 0.22), 2)
    shape(surf, WHITE, r, [(0.40, 0.39), (0.60, 0.39), (0.58, 0.43), (0.42, 0.43)], edge=1)  # sneer
    # the pencil he's holding
    shape(surf, YELLOW, r, [(0.90, 0.60), (0.96, 0.56), (1.30, 0.22), (1.24, 0.16)], edge=1)
    shape(surf, (70, 70, 80), r, [(1.24, 0.16), (1.30, 0.22), (1.40, 0.10)], edge=1)
    disc(surf, (255, 200, 170), r, 0.93, 0.60, 0.05, edge=1)                                # hand


def inkblot(surf, inner):
    """Inkblot: a purple blob of ink with dripping edges, a monocle and fangs."""
    r = inner.rect
    ink = (96, 40, 150)
    for x0, x1, length in ((0.12, 0.25, 1.02), (0.44, 0.56, 1.10), (0.76, 0.88, 0.98)):
        shape(surf, ink, r, [(x0, 0.70), (x1, 0.70), (x1, length), ((x0 + x1) / 2, length + 0.06), (x0, length)],
              edge=1)
    disc(surf, ink, r, 0.50, 0.40, 0.36, edge=0)                                            # head of ink
    disc(surf, ink, r, 0.50, 0.74, 0.30, edge=0)                                            # body of ink
    pygame.draw.arc(surf, (180, 130, 255), pygame.Rect(r.left + 5, r.top + 4, 14, 14),
                    math.pi * 0.7, math.pi * 1.2, 2)                                        # shine
    disc(surf, WHITE, r, 0.36, 0.34, 0.13)
    disc(surf, WHITE, r, 0.64, 0.34, 0.13)
    disc(surf, YELLOW, r, 0.36, 0.35, 0.07, edge=0)
    disc(surf, YELLOW, r, 0.64, 0.35, 0.07, edge=0)
    stroke(surf, INK, r, (0.36, 0.30), (0.36, 0.40), 1)
    stroke(surf, INK, r, (0.64, 0.30), (0.64, 0.40), 1)
    pygame.draw.circle(surf, GOLD, (round(r.left + 0.64 * r.w), round(r.top + 0.34 * r.h)), 6, 2)   # monocle
    stroke(surf, GOLD, r, (0.70, 0.42), (0.86, 0.66), 1)                                             # chain
    shape(surf, INK, r, [(0.30, 0.54), (0.70, 0.54), (0.60, 0.68), (0.40, 0.68)], edge=1)            # grin
    shape(surf, WHITE, r, [(0.34, 0.54), (0.44, 0.54), (0.39, 0.66)], edge=1)                        # fangs
    shape(surf, WHITE, r, [(0.56, 0.54), (0.66, 0.54), (0.61, 0.66)], edge=1)
    disc(surf, ink, r, 0.90, 0.16, 0.03, edge=0)                                                     # splatters
    disc(surf, ink, r, 0.08, 0.30, 0.02, edge=0)


def framer(cape):
    """The Framer: a top-hatted gentleman in a striped jacket, a handlebar moustache and a monocle."""

    def paint(surf, inner):
        r = inner.rect
        shape(surf, cape, r, [(0.18, 0.34), (0.82, 0.34), (1.16, 1.0), (-0.16, 1.0)])          # cape
        shape(surf, (20, 20, 26), r, [(0.22, 0.44), (0.78, 0.44), (0.86, 0.98), (0.14, 0.98)])   # jacket
        for fx in (0.30, 0.42, 0.58, 0.70):
            stroke(surf, WHITE, r, (fx, 0.50), (fx + (fx - 0.5) * 0.10, 0.96), 1)                 # pinstripes
        shape(surf, WHITE, r, [(0.40, 0.44), (0.60, 0.44), (0.50, 0.64)], edge=1)                  # shirt
        shape(surf, (220, 40, 40), r, [(0.44, 0.48), (0.50, 0.50), (0.44, 0.54)], edge=1)          # bow tie
        shape(surf, (220, 40, 40), r, [(0.56, 0.48), (0.50, 0.50), (0.56, 0.54)], edge=1)
        disc(surf, (236, 200, 160), r, 0.50, 0.26, 0.21)                                            # head
        shape(surf, (20, 20, 26), r, [(0.30, 0.16), (0.70, 0.16), (0.66, -0.06), (0.34, -0.06)], edge=1)  # hat
        shape(surf, (20, 20, 26), r, [(0.14, 0.16), (0.86, 0.16), (0.80, 0.22), (0.20, 0.22)], edge=1)    # brim
        shape(surf, YELLOW, r, [(0.34, 0.08), (0.66, 0.08), (0.66, 0.13), (0.34, 0.13)], edge=0)        # band
        shape(surf, (20, 20, 26), r, [(0.36, 0.34), (0.50, 0.31), (0.64, 0.34), (0.72, 0.29), (0.62, 0.40),
                                      (0.50, 0.37), (0.38, 0.40), (0.28, 0.29)], edge=1)            # moustache
        stroke(surf, INK, r, (0.36, 0.25), (0.46, 0.25), 2)                                         # narrow eyes
        stroke(surf, INK, r, (0.54, 0.25), (0.64, 0.25), 2)
        stroke(surf, INK, r, (0.34, 0.20), (0.46, 0.22), 1)                                         # stern brows
        stroke(surf, INK, r, (0.66, 0.20), (0.54, 0.22), 1)
        pygame.draw.circle(surf, GOLD, (round(r.left + 0.62 * r.w), round(r.top + 0.25 * r.h)), 4, 1)  # monocle
        stroke(surf, GOLD, r, (0.66, 0.30), (0.84, 0.58), 1)                                        # chain

    return paint


def anvil(surf, inner):
    """The Anvil: a riveted steel block on a piston, with a fanged, scowling face and hazard stripes."""
    r = inner.rect
    piston = pygame.Rect(r.centerx - 5, inner.y_top - 40, 10, max(0, r.top - inner.y_top + 40))
    pygame.draw.rect(surf, (90, 92, 100), piston)
    pygame.draw.rect(surf, INK, piston, 1)
    for y in range(inner.y_top - 34, r.top - 2, 9):
        pygame.draw.circle(surf, (170, 170, 180), (r.centerx, y), 2)                              # bolts
    pygame.draw.rect(surf, (128, 130, 142), r, border_radius=4)
    pygame.draw.rect(surf, (96, 70, 70), (r.left, r.bottom - 9, r.w, 9))                          # rust band
    for x in range(r.left, r.right, 12):
        pygame.draw.line(surf, YELLOW, (x, r.bottom - 1), (x + 7, r.bottom - 9), 3)               # hazard stripes
    pygame.draw.line(surf, (200, 200, 210), (r.left + 3, r.top + 3), (r.right - 4, r.top + 3), 2)  # shine
    pygame.draw.rect(surf, INK, r, 2, border_radius=4)
    stroke(surf, INK, r, (0.68, 0.10), (0.78, 0.30), 1)                                           # crack
    stroke(surf, INK, r, (0.78, 0.30), (0.74, 0.40), 1)
    for fx, fy in ((0.12, 0.20), (0.88, 0.20), (0.12, 0.62), (0.88, 0.62)):
        disc(surf, (176, 176, 186), r, fx, fy, 0.035, edge=1)                                     # rivets
    shape(surf, INK, r, [(0.14, 0.18), (0.44, 0.30), (0.44, 0.36), (0.14, 0.26)], edge=0)          # brows
    shape(surf, INK, r, [(0.86, 0.18), (0.56, 0.30), (0.56, 0.36), (0.86, 0.26)], edge=0)
    disc(surf, WHITE, r, 0.28, 0.44, 0.07)                                                        # eyes
    disc(surf, WHITE, r, 0.72, 0.44, 0.07)
    disc(surf, INK, r, 0.30, 0.46, 0.03, edge=0)
    disc(surf, INK, r, 0.70, 0.46, 0.03, edge=0)
    shape(surf, (70, 14, 14), r, [(0.22, 0.60), (0.78, 0.60), (0.72, 0.78), (0.28, 0.78)], edge=1)  # mouth
    for fx in (0.30, 0.46, 0.60):
        shape(surf, WHITE, r, [(fx, 0.60), (fx + 0.09, 0.60), (fx + 0.045, 0.74)], edge=1)        # fangs


def draw_fx_for(room, surf):
    """The sound effects go over the player. Each room calls this from draw_foreground."""
    for h in room.hazards:
        if isinstance(h, Villain):
            h.draw_fx(surf)


class Villain:
    """A kit hazard (a PatrolBot or a Crusher) in a comic-book costume.

    Its movement and hit-box come from the kit part inside. When it catches you, the fight plays out like a
    1960s TV episode: you freeze, POW! and BAM! pop up over you, and only then does the engine send you back.
    """

    HIT_TIME = 1.2                      # seconds of sound effects before you're sent back

    def __init__(self, inner, paint):
        self.inner = inner
        self.rect = inner.rect
        self.paint = paint              # paint(surf, inner) draws the costume
        self.pow = Burst(0, 0, "POW!", YELLOW)
        self.bam = Burst(0, 0, "BAM!", ORANGE)
        self.hit_left = 0.0
        self.pin = (0.0, 0.0)
        self.player = None

    def update(self, dt, room, player):
        self.player = player
        if self.hit_left > 0:
            self.hit_left -= dt
            self.rect = pygame.Rect(0, 0, 0, 0)      # no collision while the sound effects play
            self.freeze(player)
            if self.hit_left <= 0:
                self.rect = player.rect              # touching now: the engine sends you back
            return
        self.inner.update(dt, room, player)
        self.rect = self.inner.rect
        # The engine takes dt off the player's safe time after this runs, then checks it. Check the same way,
        # or the frame the safe time runs out would send the player back with no POW! and BAM!.
        if player.safe - dt <= 0 and self.rect.colliderect(player.rect):
            cx, cy = player.rect.center
            place(self.pow, cx - 60, cy - 70)
            place(self.bam, cx + 60, cy - 40)
            self.pin = (player.x, player.y)
            self.hit_left = self.HIT_TIME
            self.rect = pygame.Rect(0, 0, 0, 0)

    def freeze(self, player):
        player.x, player.y = self.pin                # you're frozen in place
        player.vx = player.vy = 0.0
        player.searching = None

    def draw(self, surf):
        # The player moves after update() and before they're drawn, so hold them in place again here.
        if self.hit_left > 0 and self.player is not None:
            self.freeze(self.player)
        self.paint(surf, self.inner)

    def draw_fx(self, surf):
        if self.hit_left <= 0:
            return
        elapsed = self.HIT_TIME - self.hit_left
        if elapsed >= 0.0:
            self.pow.draw(surf)
        if elapsed >= 0.25:
            self.bam.draw(surf)


# --- Room 1: the West elevator is through its left edge ---

class Bullpen(Room):
    title = "Bullpen"

    def build(self):
        self.comic_bg = comic_wall((30, 44, 96), (48, 70, 134))
        self.decor += [
            Sign(330, 46, "THE BULLPEN!", YELLOW),
            Poster(110, 80, "POW!", (226, 48, 48)),
            Poster(200, 80, "BAM!", (40, 120, 230)),
            Bubble(290, 190, "DEADLINE!"),
            Bubble(470, 250, "HA HA!"),
            Burst(500, 160, "ZAP!", YELLOW),
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
        self.hazards.append(Villain(PatrolBot(360, C.FLOOR_Y, left=260, right=700, speed=80), pencil_thug))

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))

    def draw_foreground(self, surf):
        draw_fx_for(self, surf)


# --- Room 2: the digit is on the top ledge ---

class InkRoom(Room):
    title = "Ink Room"

    def build(self):
        self.comic_bg = comic_wall((20, 62, 64), (34, 96, 94))
        self.decor += [
            Sign(360, 46, "INK ROOM!", (120, 240, 210)),
            Poster(560, 80, "ZAP!", (240, 140, 40)),
            Bubble(90, 150, "SHH..."),
            Bubble(200, 330, "MWAHAHA!"),
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
        self.hazards.append(Villain(PatrolBot(180, C.FLOOR_Y, left=90, right=280, speed=80), inkblot))

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))

    def draw_foreground(self, surf):
        draw_fx_for(self, surf)


# --- Room 3: the East elevator is through its right edge ---

class Gallery(Room):
    title = "Gallery"

    def build(self):
        self.comic_bg = comic_wall((90, 28, 68), (128, 48, 98))
        self.decor += [
            Sign(330, 46, "THE GALLERY!", (255, 240, 120)),
            Sign(60, 230, "TO BE CONTINUED...", (255, 240, 120), size=22),
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
            Villain(PatrolBot(260, C.FLOOR_Y, left=220, right=540, speed=70), framer((40, 110, 200))),
            Villain(Crusher(700, y_top=180, w=50, h=40), anvil),
        ]

    def draw_background(self, surf):
        surf.blit(self.comic_bg, (0, 0))

    def draw_foreground(self, surf):
        draw_fx_for(self, surf)


ROOMS = [Bullpen, InkRoom, Gallery]     # west to east
