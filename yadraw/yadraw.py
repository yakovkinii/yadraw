import logging
import threading
import time

import attrs
from typing import Tuple, Union, Dict

import numpy as np
import pygame
from yatools.logging_config import log_function


@attrs.define(kw_only=True)
class Area:
    """
    Represents an area within the window.
    Area has the following parameters:

    x0: int - Top left corner of the area on the screen

    y0: int - Top left corner of the area on the screen

    w: int - Width

    h: int - Height

    xc: int - Coord of zero-point on the area

    yc: int - Coord of zero-point on the area

    xs: float - Scale

    ys: float - Scale

    Are has the following functions:

    fill; circle; rect; rectangle; polygon; ellipse; arc; line; lines;
    aaline; aalines; text; is_screen_pos_inside_area.
    """
    x0: int = attrs.field(init=True, default=0)  # Top left corner on the screen
    y0: int = attrs.field(init=True, default=0)  # Top left corner on the screen
    w: int = attrs.field(init=True, default=800)  # Width/Height
    h: int = attrs.field(init=True, default=800)  # Width/Height
    xc: int = attrs.field(init=True, default=0)  # Coord of zero-point on the surface
    yc: int = attrs.field(init=True, default=0)  # Coord of zero-point on the surface
    xs: float = attrs.field(init=True, default=1)  # Scale
    ys: float = attrs.field(init=True, default=1)  # Scale
    font: pygame.font.Font = attrs.field(init=False, default=None)
    surface: pygame.Surface = attrs.field(init=False, default=None)

    @log_function
    def __attrs_post_init__(self):
        self.surface = pygame.Surface((self.w, self.h))

    """ Any thread public methods """

    def fill(self, *args, **kwargs):
        """
        color: _ColorValue,

        rect: Optional[_CanBeRect],

        special_flags: int
        """
        return self.surface.fill(*args, **kwargs)

    def circle(self, center: Union[Tuple[float, float], np.ndarray], **kwargs):
        """
        center: Union[Tuple[float, float], np.ndarray] - (x0, y0),

        color: _ColorValue,

        center: _Coordinate,

        radius: float,

        width: int = 0,

        draw_top_right: Optional[bool] = None,

        draw_top_left: Optional[bool] = None,

        draw_bottom_left: Optional[bool] = None,

        draw_bottom_right: Optional[bool] = None
        """
        center = self._local_to_area(np.array(center))
        return pygame.draw.circle(self.surface, center=center, **kwargs)

    def rect(self, rect: Union[Tuple[float, float, float, float], np.ndarray], **kwargs):
        """
        rect: Union[Tuple[float, float, float, float], np.ndarray] - (x0, y0, width, height),

        surface: Surface,

        color: _ColorValue,

        width: int = 0,

        border_radius: int = -1,

        border_top_left_radius: int = -1,

        border_top_right_radius: int = -1,

        border_bottom_left_radius: int = -1,

        border_bottom_right_radius: int = -1
        """
        rect = self._local_to_area_rect(np.array(rect))
        return pygame.draw.rect(self.surface, rect=pygame.Rect(self._p_to_list_rect(rect)), **kwargs)

    def rectangle(self, *args, **kwargs):
        """
        rect: Union[Tuple[float, float, float, float], np.ndarray] - (x0, y0, width, height),

        surface: Surface,

        color: _ColorValue,

        width: int = 0,

        border_radius: int = -1,

        border_top_left_radius: int = -1,

        border_top_right_radius: int = -1,

        border_bottom_left_radius: int = -1,

        border_bottom_right_radius: int = -1
        """
        return self.rect(*args, **kwargs)

    def polygon(self, color, points, **kwargs):
        """
        color: _ColorValue,

        points: Sequence[Union[Tuple[float, float], np.ndarray]] - [(x0, y0), (x1, y1), ...]

        width: int = 0
        """
        points_scaled = []
        for p in points:
            points_scaled.append(self._local_to_area(np.array(p)))
        return pygame.draw.polygon(self.surface, color=color, points=points, **kwargs)

    def ellipse(self, color, rect, **kwargs):
        """
        color: _ColorValue,

        rect: Union[Tuple[float, float, float, float], np.ndarray] - (x0, y0, width, height),

        width: int = 0
        """
        rect = self._local_to_area_rect(np.array(rect))
        return pygame.draw.ellipse(self.surface, color=color, rect=pygame.Rect(self._p_to_list_rect(rect)), **kwargs)

    def arc(self, color, rect, start_angle, stop_angle, **kwargs):
        """
        color: _ColorValue,

        rect: Union[Tuple[float, float, float, float], np.ndarray] - (x0, y0, width, height),

        start_angle: float,

        stop_angle: float,

        width: int = 1
        """
        if self.xs != self.ys:
            logging.error("Arc is not implemented for x_scale != y_scale")
        return pygame.draw.arc(self.surface, color=color, rect=pygame.Rect(self._local_to_area(np.array(rect))),
                               start_angle=start_angle, stop_angle=stop_angle, **kwargs)

    def line(self, color, start_pos, end_pos, **kwargs):
        """
        color: _ColorValue,

        start_pos: Union[Tuple[float, float], np.ndarray] - (x0, y0),

        end_pos: Union[Tuple[float, float], np.ndarray] - (x1, y1),

        width: int = 1
        """
        return pygame.draw.line(self.surface, color=color,
                                start_pos=pygame.Vector2(*(self._local_to_area(np.array(start_pos)))),
                                end_pos=pygame.Vector2(*(self._local_to_area(np.array(end_pos)))), **kwargs)

    def lines(self, color, closed: bool, points, **kwargs):
        """
        color: _ColorValue,

        closed: bool,

        points: Sequence[Union[Tuple[float, float], np.ndarray]] - [(x0, y0), (x1, y1), ...]

        width: int = 1
        """
        points_scaled = []
        for p in points:
            points_scaled.append(self._local_to_area(np.array(p)))
        return pygame.draw.lines(self.surface, color=color, closed=closed, points=points, **kwargs)

    def aaline(self, color, start_pos, end_pos, **kwargs):
        """
        Line with antialiasing.

        color: _ColorValue,

        start_pos: Union[Tuple[float, float], np.ndarray] - (x0, y0),

        end_pos: Union[Tuple[float, float], np.ndarray] - (x1, y1),

        width: int = 1
        """
        return pygame.draw.aaline(self.surface, color=color,
                                  start_pos=pygame.Vector2(*(self._local_to_area(np.array(start_pos)))),
                                  end_pos=pygame.Vector2(*(self._local_to_area(np.array(end_pos)))), **kwargs)

    def aalines(self, color, closed: bool, points, **kwargs):
        """
        Lines with antialiasing.

        color: _ColorValue,

        closed: bool,

        points: Sequence[Union[Tuple[float, float], np.ndarray]] - [(x0, y0), (x1, y1), ...]

        width: int = 1
        """
        points_scaled = []
        for p in points:
            points_scaled.append(self._local_to_area(np.array(p)))
        return pygame.draw.aalines(self.surface, color=color, closed=closed, points=points, **kwargs)

    def text(self, text: str, position, size=48, font=None, antialias=True, color=(0, 0, 0), bold=False, italic=False):
        """
        text: str,

        position: Union[Tuple[float, float], np.ndarray] - (x0, y0),

        size: int = 48,

        font: pygame.font.SysFont = None - overrides size if spcified,

        antialias: bool = True,

        color: _ColorValue,

        bold: bool = False,

        italic: bool = False
        """
        if font is None:
            font = pygame.font.SysFont('Calibri', size, bold=bold, italic=italic)

        img = font.render(text, antialias, color)
        self.surface.blit(img, self._local_to_area(np.array(position)))

    def is_screen_pos_inside_area(self, pos: Union[Tuple[float, float], np.ndarray]):
        """
        Is given screen coordinate inside this area?
        :param pos: Union[Tuple[float, float], np.ndarray] - (x0, y0)
        :return: bool
        """
        x = pos[0]
        y = pos[1]
        if (x < self.x0) or (x > self.x0 + self.w):
            return False
        if (y < self.y0) or (y > self.y0 + self.h):
            return False
        return True

    def _r0(self):
        return np.array([self.x0, self.y0])

    def _rc(self):
        return np.array([self.xc, self.yc])

    def _rs(self):
        return np.array([self.xs, self.ys])

    def _local_to_area(self, point: np.ndarray):
        return self._rc() + self._rs() * point

    def _screen_to_local(self, point: np.ndarray):
        return (point - self._rc() - self._r0()) / self._rs()

    def _local_to_area_rect(self, point_2p: np.ndarray):
        p1 = self._rc() + point_2p[0:2] * self._rs()
        p2 = point_2p[2:4] * self._rs()
        p1 = p1 - p2 * (np.sign(p2) - 1) / 2
        p2 = np.abs(p2)
        return np.concatenate([p1, p2])

    @staticmethod
    def _p_to_list(point):
        return [point[0], point[1]]

    @staticmethod
    def _p_to_list_rect(point):
        return [point[0], point[1], point[2], point[3]]

    """ GUI thread public methods """

    def on_event(self, event: pygame.event):
        ...

    def on_redraw(self):
        ...


@attrs.define(kw_only=True)
class Window(Area):
    """
    Main YaDraw class. Represents a single window.
    Window and each of its areas have the following parameters:

    x0: int - Top left corner of the area on the screen

    y0: int - Top left corner of the area on the screen

    w: int - Width

    h: int - Height

    xc: int - Coord of zero-point on the area

    yc: int - Coord of zero-point on the area

    xs: float - Scale

    ys: float - Scale

    Window and each of its areas have the following functions:

    fill; circle; rect; rectangle; polygon; ellipse; arc; line; lines;
    aaline; aalines; text; is_screen_pos_inside_area.
    """
    screen: pygame.Surface = attrs.field(init=False, default=None)  # Main screen handler
    areas: Dict[str, Area] = attrs.field(init=True, default={})
    continue_running_main_loop: bool = attrs.field(init=False, default=False)
    main_loop_thread: Union[threading.Thread, None] = attrs.field(init=False, default=None)
    auto_update_s: float = attrs.field(init=True, default=None)
    gui_initialized: bool = attrs.field(init=False, default=False)

    @log_function
    def __attrs_post_init__(self):
        super(Window, self).__attrs_post_init__()
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
    def add_area(self, name, x0, y0, w, h, xc, yc, xs, ys):
        if name in self.areas.keys():
            logging.error(f"Cannot add area: area with the name '{name}' already exists")
        else:
            self.areas[name] = Area(x0, y0, w, h, xc, yc, xs, ys)

    def invoke_redraws_for_all_areas(self):
        self.on_redraw()
        for name, area in self.areas.items():
            area.on_redraw()

    def update(self):
        self.invoke_redraws_for_all_areas()
        self.screen.blit(self.surface, (self.x0, self.y0))
        for name, area in self.areas.items():
            self.screen.blit(area.surface, (area.x0, area.y0))
        pygame.display.flip()

    def on_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            logging.info("pygame.QUIT message received")
            self.continue_running_main_loop = False
        for name, area in self.areas.items():
            if True:
                area.on_event(event)

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
            time.sleep(0.1)  # To avoid GIL
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
