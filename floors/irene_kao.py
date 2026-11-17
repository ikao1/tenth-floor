"""5th Floor Comics: a bullpen, an ink room, and a gallery.

Three rooms side by side. You come off the WEST elevator into the Bullpen, walk east through the Ink Room
into the Gallery, and get on the EAST elevator. The digit of the door code is on the "original page" plinth
at the top of the Ink Room's ledges.
"""
from engine import config as C
from engine.kit import (Bookshelf, CeilingLight, Couch, Crusher, Desk, Easel, FilingCabinet, PatrolBot, Plant,
                        Plinth, Poster, Sign, Window)
from engine.room import Platform, Room

NAME = "5th Floor Comics"              # the name on the elevator panel
AUTHOR = "Irene Kao"                       # your name


# --- Room 1: the West elevator is through its left edge ---

class Bullpen(Room):
    title = "Bullpen"

    def build(self):
        self.decor += [
            Sign(330, 46, "THE BULLPEN", (255, 210, 60)),
            Poster(110, 80, "POW", (220, 60, 60)),
            Poster(200, 80, "BAM", (60, 120, 220)),
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


# --- Room 2: the digit is on the top ledge ---

class InkRoom(Room):
    title = "Ink Room"

    def build(self):
        self.decor += [
            Sign(360, 46, "INK ROOM", (120, 220, 200)),
            Poster(560, 80, "ZAP", (240, 140, 40)),
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


# --- Room 3: the East elevator is through its right edge ---

class Gallery(Room):
    title = "Gallery"

    def build(self):
        self.decor += [
            Sign(330, 46, "THE GALLERY", (255, 120, 170)),
            Poster(120, 80, "THE END", (200, 70, 60)),
            Window(600, 70, seed=7),
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


ROOMS = [Bullpen, InkRoom, Gallery]     # west to east
