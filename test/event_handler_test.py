"""
Custom event handler test for YaDraw. Customize the reaction to GUI events such as keyboard input.
"""

import logging

import pygame

from misc import logging_config
import yadraw.libmain as yd


# Create a substitute for event handler
def custom_on_event(self, event: pygame.event):
    if event.type == pygame.MOUSEBUTTONUP:
        logging.info("Pressure! Pushing down on me")
    if event.type == pygame.QUIT:
        logging.warning("Aha-hah no quitting for you (do not press any key pls)")
    if event.type == pygame.KEYUP:
        logging.warning("You trik me I giv up")
        self.continue_running_main_loop = False


# Init fancy logger (unrelated to YaDraw)
logging_config.init()

# Monkey-patch the event handler for YaDrawWindow class
# It's easier than patching an instance, and only 1 GUI instance is supported anyway
yd.YaDrawWindow.on_event = custom_on_event

# Init window, set automatic update to 0.1 second interval
window = yd.YaDrawWindow(auto_update_s=0.1)  # 10 fps

# Draw something
window.fill((100, 100, 200))
window.circle(center=(200, 200), radius=100, color=(255, 0, 255))

# Await GUI exit
window.wait_until_exit()
