"""
Dispatcher API daemon
"""
import time
import zmq

DEFAULT_PORT = 5555


class Dispatcher(object):
    def __init__(self, port=DEFAULT_PORT):
        # Prepare context
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://*:{port}".format(port=port))

        while True:
            time.sleep(1)

        publisher.close()
        context.term()


if __name__ == '__main__':
    Dispatcher()
