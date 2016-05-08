"""
Dispatcher API daemon
"""
import json

import pika
from bson import json_util

import kamerie_plugins
from kamerie.utilities.consts import DISPATCHER_NAME, EXCHANGE_NAME, MEDIA_KEYS, SCANNED, \
    MEDIA_PATH, MEDIA_TYPE
from kamerie.utilities.utilities import get_logger
from media_scanner import MediaScanner


class Dispatcher(object):
    def __init__(self):
        # Prepare instance
        self.name = DISPATCHER_NAME

        # Prepare logger
        self._logger = get_logger('dispatcher')
        self._logger.info("Initialized dispatcher")

        self.media_scanner = MediaScanner(self._logger)
        self.plugins = kamerie_plugins.register_plugins()

        # rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self._logger.info('Connected to RabbitMQ successfully')

        self.channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
        # self.on_message({'media_path': '/home/dor/Videos/movies', 'media_type': TYPE_MOVIE})
        # self.on_message({'media_path': '/home/dor/Videos/tv', 'media_type': TYPE_SERIES})

    def start(self):
        self._logger.info("Starting" % self.name)

    def on_message(self, message):
        if isinstance(message, dict) and all(k in MEDIA_KEYS for k in message.keys()):
            if not message.get(SCANNED, False):
                for scanner_message in self.media_scanner.scan_directory(message[MEDIA_PATH], message[MEDIA_TYPE]):
                    self.channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='',
                                               body=json_util.dumps(scanner_message))
            else:
                self._logger.info('Publishing message to all plugins: %s' % str(message))
                self.channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=json.dumps(message))
        else:
            self._logger.error("Invalid message: %s" % str(message))

    def __exit__(self):
        self.close()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    Dispatcher()
