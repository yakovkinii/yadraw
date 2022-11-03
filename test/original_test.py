import time

import threading
import logging

import pygame

import yadrawlib.libmain as yd

if __name__ == "__main__":
    window = yd.YaDrawWindow(auto=False)

    logging.warning("Initializing loop thread")
    loop_thread = threading.Thread(target=window.start_main_loop)

    logging.warning("Starting loop thread")
    loop_thread.start()

    logging.warning("Loop thread started")
    time.sleep(6)

    logging.warning("Painting image")
    time.sleep(1)
    window.fill((100, 200, 100))
    window.circle(center=(100, 100), radius=50, color=(0, 0, 255))
    window.flip()
    time.sleep(6)

    logging.warning("Changing image")
    time.sleep(1)
    buffer = pygame.Surface((200, 100))
    pygame.draw.circle(buffer,
                       color=(255, 0, 0),
                       center=(50, 50),
                       radius=70)
    window.screen.blit(buffer, (100, 100))
    window.flip()
    time.sleep(6)

    logging.warning("Changing image")
    time.sleep(1)
    window.fill((100, 100, 200))
    window.circle(center=(200, 200), radius=100, color=(255, 0, 255))
    window.flip()
    time.sleep(6)

    logging.warning("Trying to stop loop thread")
    time.sleep(1)
    window.main_loop_running = False
    time.sleep(6)

    logging.warning("Joining loop thread")
    time.sleep(1)
    loop_thread.join()
    logging.warning("Main halt")
