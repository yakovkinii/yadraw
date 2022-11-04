from misc import logging_init
import time
import yadrawlib.libmain as yd


logging_init.init()

# init window
window = yd.YaDrawWindow()

# Draw something
window.fill((100, 100, 200))
window.circle(center=(200, 200), radius=100, color=(255, 0, 255))
window.update()

time.sleep(10)

# terminate gui
window.close()
