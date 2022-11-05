"""
Async redraw handler test for YaDraw.
The GUI will draw the latest results at its own pace, not limiting the calculation speed to the screen update speed.
"""

import time
import unittest

from src.yadraw import logging_config
import src.yadraw.yadraw as yd

logging_config.init()


class TestAsyncRedraw(unittest.TestCase):
    def test_async_redraw(self):
        # Create a custom on_redraw handler
        def custom_on_redraw(self: yd.Window):
            self.fill((200, 200, 200))
            for point in list_of_points_to_draw:
                self.circle(center=point, radius=4, color=(0, 0, 255))

        # Monkey-patch the on_redraw handler for YaDrawWindow class
        yd.Window.on_redraw = custom_on_redraw

        # Create a window, set automatic update to 1 second interval
        window = yd.Window(auto_update_s=1)  # 1 fps

        # Start the "calculation" of the points to draw
        list_of_points_to_draw = []
        for i in range(100):
            list_of_points_to_draw.append((i * 8, i * 8))
            time.sleep(0.1)  # around 10 dots per frame

        # Await GUI exit
        window.wait_until_exit()


if __name__ == "__main__":
    unittest.main()
