import logging
from typing import Tuple

import pygame

"""
Window is a unique singular parent for all graphics.
Window can have multiple areas. In order to draw to a certain area you need to select it.
Area types:
    1. None (default) - draw directly to the window, no scaling.
    2. Fixed - no scaling, but has offset and borders.
    3. Scaled - has scaling, offset and borders.
"""


class YaDrawArea:
    def __init__(self, width, height):
        self.x0 = 0
        self.y0 = 0
        self.w = width
        self.h = height
        self.xc = 0
        self.yc = 0
        self.xs = 1
        self.ys = 1

    def get_area_parameters(self):
        return self.x0, self.y0, self.w, self.h, self.xc, self.yc, self.xs, self.ys


class YaDrawWindow:
    """
    Main YaDraw class. Represent a single window.
    Only one window is supported for now.
    """
    def __init__(self, auto=True):
        self.screen = None
        self.areas = None
        self.area_index = None
        self.main_loop_running = None
        self.init_completed = False

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 800])
        self.areas = [YaDrawArea(self.screen.get_width(), self.screen.get_height())]
        self.area_index = 0
        self.main_loop_running = True
        self.init_completed = True

    def __del__(self):
        pygame.quit()

    def _get_selected_area_parameters(self):
        return self.areas[self.area_index].get_area_parameters()

    def select_area(self, area_index):
        if area_index < 0 or area_index >= len(self.areas):
            logging.error(f"Cannot select area {area_index}")
            return self
        self.area_index = area_index
        return self

    def circle(self, center: Tuple[float, float], radius: float, color: Tuple[int, int, int] = (0, 0, 0)):
        x0, y0, w, h, xc, yc, xs, ys = self._get_selected_area_parameters()
        if xs != ys:
            logging.warning("Circle: different x and y scales. Using x scale.")
            ys = xs
        pygame.draw.circle(self.screen,
                           color=color,
                           center=[x0 + xc + xs * center[0], y0 + yc + ys * center[1]],
                           radius=xs * radius)

    def fill(self, color: Tuple[int, int, int] = (0, 0, 0)):
        self.screen.fill(color)

    @staticmethod
    def flip():
        pygame.display.flip()

    def start_main_loop(self):
        logging.warning("Starting init")
        self.init()

        logging.warning("Starting main loop")
        self.main_loop_running = True
        while self.main_loop_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    logging.warning("pygame.MOUSEBUTTONUP message received.")
                if event.type == pygame.QUIT:
                    logging.warning("pygame.QUIT message received.")
                    self.main_loop_running = False

        logging.warning("Exiting main loop")
        # self.screen = pygame.display.set_mode(self.screen.get_size(), flags=pygame.HIDDEN)
