import logging

import pygame

from misc import logging_config
import yadrawlib.libmain as yd


def custom_on_event(self, event: pygame.event):
    if event.type == pygame.MOUSEBUTTONUP:
        logging.info("Pressure! Pushing down on me")
    if event.type == pygame.QUIT:
        logging.warning("Aha-hah no quitting for you")
    if event.type == pygame.KEYUP:
        logging.info("You trik me I giv up")
        self.continue_running_main_loop = False


logging_config.init(level=logging.INFO)

# Monkey-patch the event handler for YaDrawWindow (since only 1 instance allowed anyway)
yd.YaDrawWindow.on_event = custom_on_event

# init window
window = yd.YaDrawWindow(auto_update_s=0.1)

# Draw something
window.fill((100, 100, 200))
window.circle(center=(200, 200), radius=100, color=(255, 0, 255))

window.wait_until_exit()
