import logging
import threading
import time

import attrs
from typing import Tuple, List, Union

import pygame

from misc.logging_config import log_function


@attrs.define(kw_only=True)
class YaDrawArea:
    x0: int = attrs.field(init=True, default=0)  # Top left corner on the screen
    y0: int = attrs.field(init=True, default=0)  # Top left corner on the screen
    w: int = attrs.field(init=True, default=800)  # Width/Height
    h: int = attrs.field(init=True, default=800)  # Width/Height
    xc: int = attrs.field(init=True, default=0)  # Coord of zero-point on the surface
    yc: int = attrs.field(init=True, default=0)  # Coord of zero-point on the surface
    xs: float = attrs.field(init=True, default=1)  # Scale
    ys: float = attrs.field(init=True, default=1)  # Scale
    surface: pygame.Surface = attrs.field(init=False, default=None)

    @log_function
    def __attrs_post_init__(self):
        self.surface = pygame.Surface((self.w, self.h))

    """ Any thread public methods """

    @log_function
    def circle(self, center: Tuple[float, float], radius: float, color: Tuple[int, int, int] = (0, 0, 0)):
        if self.xs != self.ys:
            logging.error("Unimplemented: Circle: different x and y scales.")
            return
        pygame.draw.circle(self.surface,
                           color=color,
                           center=[self.xc + self.xs * center[0], self.yc + self.ys * center[1]],
                           radius=self.xs * radius)

    @log_function
    def rect(self, rect: Tuple[float, float, float, float], width: int = 0, color: Tuple[int, int, int] = (0, 0, 0)):
        """ width=0 -> solid fill; width!=0 -> only border """
        pygame.draw.rect(self.surface, color=color, rect=pygame.Rect(rect), width=width)

    @log_function
    def fill(self, color: Tuple[int, int, int] = (0, 0, 0)):
        self.surface.fill(color)

    """ GUI thread public methods """

    @log_function
    def on_event(self, event: pygame.event):
        ...

    @log_function
    def on_redraw(self):
        ...


@attrs.define(kw_only=True)
class YaDrawAreaCatalogEntry:
    area: YaDrawArea = attrs.field(init=True)
    messages_to_intercept: Tuple[int] = attrs.field(init=True, default=[])

    def is_screen_coord_in_area(self, x, y):
        left = self.area.x0
        right = self.area.x0 + self.area.w
        top = self.area.y0
        bottom = self.area.y0 + self.area.h

        if left <= x <= right and top <= y <= bottom:
            return True
        return False


@attrs.define(kw_only=True)
class YaDrawWindow(YaDrawArea):
    """
    Main YaDraw class. Represents a single window.
    Only one window is supported.
    """
    screen: pygame.Surface = attrs.field(init=False, default=None)  # Main screen handler
    areas: List[YaDrawAreaCatalogEntry] = attrs.field(init=True, default=[])
    continue_running_main_loop: bool = attrs.field(init=False, default=False)
    main_loop_thread: Union[threading.Thread, None] = attrs.field(init=False, default=None)
    auto_update_s: float = attrs.field(init=True, default=None)
    gui_initialized: bool = attrs.field(init=False, default=False)

    @log_function
    def __attrs_post_init__(self):
        super(YaDrawWindow, self).__attrs_post_init__()
        self._start_main_loop()

    @log_function
    def __del__(self):
        if self.main_loop_thread is not None:
            logging.error('Forcefully joining gui thread')
            self.main_loop_thread.join()
            self.main_loop_thread = None
            logging.info('Forcefully joined gui thread')

    """ Any thread public methods """

    @log_function
    def invoke_redraws_for_all_areas(self):
        self.on_redraw()
        for area in self.areas:
            area.on_redraw()

    @log_function
    def update(self):
        self.screen.blit(self.surface, (self.x0, self.y0))
        for area in self.areas:
            self.screen.blit(area.surface, (area.x0, area.y0))
        pygame.display.flip()

    """ Main thread public methods """

    @log_function
    def close(self):
        self._stop_main_loop()

    @log_function
    def wait_until_exit(self):
        logging.info('Main thread awaiting gui exit')
        self._await_main_loop()

    """ Main thread protected methods """

    @log_function
    def _start_main_loop(self):
        self.main_loop_thread = threading.Thread(target=self._main_loop)
        self.gui_initialized = False
        self.continue_running_main_loop = True
        self.main_loop_thread.start()
        logging.info('Started gui thread')
        logging.debug('Main thread: waiting for gui to initialize')
        while not self.gui_initialized:
            pass
        logging.debug('Main thread: continue')

    @log_function
    def _await_main_loop(self):
        self.main_loop_thread.join()
        self.main_loop_thread = None
        logging.info('Joined gui thread')

    @log_function
    def _stop_main_loop(self):
        self.continue_running_main_loop = False
        self._await_main_loop()

    """ GUI thread public methods """

    @log_function
    def on_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            logging.info("pygame.QUIT message received")
            self.continue_running_main_loop = False

    """ GUI thread protected methods """

    @log_function
    def _init(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.w, self.h])
        self.gui_initialized = True

    @log_function
    def _main_loop(self):
        self._init()
        last_update_time = time.time()
        while self.continue_running_main_loop:
            for event in pygame.event.get():
                self.on_event(event)
            if self.auto_update_s is not None and time.time() > last_update_time + self.auto_update_s:
                self.invoke_redraws_for_all_areas()
                self.update()
                last_update_time = time.time()
        pygame.quit()
