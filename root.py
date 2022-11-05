from misc import logging_config
from test.async_redraw import async_redraw_test
from test.event_handler_test import event_handler_test
from test.minimal_test import minimal_test

if __name__ == "__main__":
    logging_config.init()
    minimal_test()
    event_handler_test()
    async_redraw_test()
