"""
Minimal test for YaDraw. Nothing too fancy, but notice the absence of boilerplate code.
The key principle: avoid building the app around GUI. Make it easy to add GUI to already existing app.
"""
import unittest

from yatools import logging_config
import yadraw.yadraw as yd
import time

logging_config.init()


class TestMinimal(unittest.TestCase):
    def test_minimal(self):
        # Create a window
        window = yd.Window()

        # Draw a circle and a rectangle
        window.fill((100, 100, 200))
        window.circle(center=(200, 200), radius=100, color=(200, 0, 100))
        window.rectangle(rect=(200, 200, 100, 100), width=3, color=(0, 200, 0))
        window.text(text="Hello World", position=(200, 200), size=48)
        window.text(text="Hello World1", position=(600, 200), size=48)

        # Tell the window to update
        window.update()

        # Wait 5 seconds
        time.sleep(5)

        # Terminate gui
        window.close()


if __name__ == "__main__":
    unittest.main()
