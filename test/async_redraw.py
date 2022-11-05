"""
Async redraw handler test for YaDraw.
The GUI will draw the latest results at its own pace, not limiting the calculation speed to the screen update speed.
"""

import time

from misc import logging_config
import yadraw.libmain as yd


def custom_on_redraw(self: yd.YaDrawWindow):
    self.fill((200, 200, 200))
    for point in list_of_points_to_draw:
        self.circle(center=point, radius=4, color=(0,0,255))


# Init fancy logger (unrelated to YaDraw)
logging_config.init()

# Monkey-patch redraw handler for YaDrawWindow (since only 1 instance allowed anyway)
yd.YaDrawWindow.on_redraw = custom_on_redraw

# Init window, set automatic update to 1 second interval
window = yd.YaDrawWindow(auto_update_s=1)  # 1 fps

# Start the "calculation" of the points to draw
list_of_points_to_draw = []
for i in range(100):
    list_of_points_to_draw.append((i*8, i*8))
    time.sleep(0.2)  # around 5 dots per frame

# Await GUI exit
window.wait_until_exit()
