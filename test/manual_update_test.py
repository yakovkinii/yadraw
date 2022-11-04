import logging
from misc import logging_init

import time

import yadrawlib.libmain as yd


logging_init.init()
time.sleep(3)

logging.info("Creating a window")
time.sleep(1)
window = yd.YaDrawWindow()
time.sleep(3)

logging.info("Drawing an image")
time.sleep(1)
window.fill((100, 100, 200))
window.circle(center=(200, 200), radius=100, color=(255, 0, 255))
window.update()
time.sleep(3)

logging.info("Updating an image")
time.sleep(1)
window.fill((200, 000, 200))
window.circle(center=(400, 200), radius=200, color=(0, 0, 255))
window.update()
time.sleep(3)

logging.info("Exiting")
time.sleep(1)
window.close()
