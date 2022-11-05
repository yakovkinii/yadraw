"""
Custom event handler test for YaDraw. Customize the reaction to GUI events such as keyboard input.
"""

import logging
import unittest

import pygame

from src.yadraw import logging_config
import src.yadraw.yadraw as yd

logging_config.init()


class TestEventHandler(unittest.TestCase):
    def test_event_handler(self):
        # Create a custom event handler
        def custom_on_event(self, event: pygame.event):
            if event.type == pygame.MOUSEBUTTONUP:
                logging.info("Pressure! Pushing down on me")
            if event.type == pygame.QUIT:
                logging.info("pygame.QUIT message received")
                self.continue_running_main_loop = False

        # Monkey-patch the event handler for YaDrawWindow class
        yd.Window.on_event = custom_on_event

        # Create a window, set automatic update to 0.1 second interval
        window = yd.Window(auto_update_s=0.1)  # 10 fps

        # Draw something
        window.fill((100, 200, 100))
        window.circle(center=(500, 500), radius=50, color=(0, 255, 255))

        # Await GUI exit
        window.wait_until_exit()


if __name__ == "__main__":
    unittest.main()
