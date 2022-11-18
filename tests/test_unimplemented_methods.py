"""
Test for using methods which are not yet implemented in YaDraw.
Pygame methods can be used directly with YaDraw,
but already implemented in YaDraw methods automatically account for shifts and scales of areas.
"""
import pygame
import unittest

from yadraw import logging_config
import yadraw as yd
import time

logging_config.init()


class TestUnimplementedMethods(unittest.TestCase):
    def test_unimplemented_methods(self):
        # Create a window, set automatic update to 0.1 second interval
        window = yd.Window(auto_update_s=0.1)  # 10 fps

        # Fill window (implemented in YaDrawWindow)
        window.fill((100, 100, 200))

        # Draw ellipse (not implemented in YaDrawWindow)
        pygame.draw.ellipse(surface=window.surface, color=(0, 255, 0), rect=pygame.Rect(100, 100, 200, 150), width=5)

        # Tell the window to update
        window.update()

        # Wait 5 seconds
        time.sleep(5)

        # Terminate gui
        window.close()


if __name__ == "__main__":
    unittest.main()
