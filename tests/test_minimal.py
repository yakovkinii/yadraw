"""
Minimal test for YaDraw. Nothing too fancy, but notice the absence of boilerplate code.
The key principle: avoid building the app around GUI. Make it easy to add GUI to already existing app.
"""
import unittest

from src.yadraw_yakovkinii import logging_config
import time
import src as yd

logging_config.init()


class TestMinimal(unittest.TestCase):
    def test_minimal(self):
        # Create a window
        window = yd.Window()

        # Draw a circle
        window.fill((100, 100, 200))
        window.circle(center=(200, 200), radius=100, color=(255, 0, 255))

        # Tell the window to update
        window.update()

        # Wait 5 seconds
        time.sleep(5)

        # Terminate gui
        window.close()


if __name__ == "__main__":
    unittest.main()
