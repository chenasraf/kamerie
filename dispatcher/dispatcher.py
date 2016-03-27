"""
Dispatcher API daemon
"""
import threading
import time
import zmq
from random import randint
import logging

KAMERIE_NAME = "kameried"

DEFAULT_PORT = 5555

KEEP_ALIVE_INTERVAL = 10  # secs

KEEP_ALIVE = b"keep_alive"
TRUE_SIGNAL = b"true"
CLOSE_SIGNAL = b"connection_closed"

DEFAULT_THREAD_NAME = "default_thread_name"


class Dispatcher(threading.Thread):
    def __init__(self, thread_id=None, thread_name=DEFAULT_THREAD_NAME, port=DEFAULT_PORT):
        # Prepare context
        super(Dispatcher, self).__init__()
        self.alive = True
        self.thread_id = thread_id if thread_id is not None else randint(0, 1000)
        self.thread_name = thread_name

        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)

        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:{port}".format(port=port))

    def run(self):
        self._logger.info("Starting thread #{id}, name: {name}".format(id=self.thread_id, name=self.thread_name))
        while self.alive:
            self.keep_alive()

    def close(self):
        self._logger.info("Exiting thread #{id}, name: {name}".format(id=self.thread_id, name=self.thread_name))
        self.publisher.close()
        self.context.term()
        self.alive = False

    def keep_alive(self):
        self._logger.info("Sent keep alive signal")
        self.publisher.send_multipart(msg_parts=[KEEP_ALIVE, TRUE_SIGNAL])
        time.sleep(KEEP_ALIVE_INTERVAL)
