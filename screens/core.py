from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Callable
from PIL import ImageFont

@dataclass
class Point:
    x: int
    y: int
    s: int

@dataclass
class Element:
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    click: Callable
    text: str = ''
    index: int = -1

class Screen(ABC):
    @abstractmethod
    def handle_click(self, point: Point):
        pass


class App(ABC):
    @property
    def task_list(self):
        pass

    @property
    def task_timer(self):
        pass

    @property
    def timer_done(self):
        pass

    @abstractmethod
    def request_redraw(self):
        pass


# Drawing on the image
font15 = ImageFont.truetype('font/Roboto-Light.ttf', 15)
font24 = ImageFont.truetype('font/Roboto-Light.ttf', 24)
font48 = ImageFont.truetype('font/Roboto-Black.ttf', 48)

emojiFont = ImageFont.truetype('font/NotoEmoji-Regular.ttf', 24)

SCREEN_WIDTH = 250
SCREEN_HEIGHT = 122

Y4 = SCREEN_HEIGHT // 4
X3 = SCREEN_WIDTH // 3
X2 = SCREEN_WIDTH // 2

def center(e: Element) -> tuple[float, float]:
    return ((e.x_start+e.x_end)/2, (e.y_start+e.y_end)/2)

def within(p: Point, e: Element) -> bool:
    if (p.x >= e.x_start and
        p.x <= e.x_end and
        p.y >= e.y_start and
        p.y <= e.y_end):
        return True
