"""
Minimal test for YaDraw. Nothing too fancy, but notice the absence of boilerplate code.
The key principle: avoid building the app around GUI. Make it easy to add GUI to already existing app.
"""
from misc import logging_config
import time
import yadraw.libmain as yd

# Init fancy logger (unrelated to YaDraw)
logging_config.init()

# Placeholder for a giant app which calculates some results that need visualization

# Init window
window = yd.YaDrawWindow()

# Draw a circle
window.fill((100, 100, 200))
window.circle(center=(200, 200), radius=100, color=(255, 0, 255))

# Tell the window to update
window.update()

# Wait 10 seconds
time.sleep(10)

# Terminate gui
window.close()
