import unittest

import zmq

from datetime import datetime, timedelta
import time

from dispatcher import dispatcher


class SubscriberTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = dispatcher.Dispatcher()
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:{port}".format(port=dispatcher.DEFAULT_PORT))
        self.dispatcher.start()

    def tearDown(self):
        self.subscriber.close()
        self.context.term()
        self.dispatcher.close()

    def test_keep_alive_interval_test(self):
        time.sleep(1)
        start_time = datetime.now()
        self.subscriber.setsockopt(zmq.SUBSCRIBE, dispatcher.KEEP_ALIVE)
        self.subscriber.recv_multipart()
        self.assertGreaterEqual(timedelta(seconds=dispatcher.KEEP_ALIVE_INTERVAL),
                                datetime.now() - start_time,
                                "Keep alive arrived late. like your girlfriend")

    def test_one_subscriber(self):
        self.subscriber.setsockopt(zmq.SUBSCRIBE, dispatcher.KEEP_ALIVE)
        [address, content] = self.subscriber.recv_multipart()

        self.assertEqual(dispatcher.KEEP_ALIVE, address, "got msg from different event: %s" % address)
        self.assertIsNotNone(content)
