"""
Dispatcher API daemon
"""
import json
from time import sleep

import pika
from bson import json_util

from kamerie.utilities.consts import DISPATCHER_NAME, EXCHANGE_NAME, MEDIA_KEYS, SCANNED, \
    MEDIA_PATH, MEDIA_TYPE
from kamerie.utilities.utilities import get_logger
from media_scanner import MediaScanner
from plugin_manager import PluginManager


class Dispatcher(object):
    def __init__(self):
        # Prepare instance
        self.name = DISPATCHER_NAME

        # Prepare logger
        self._logger = get_logger('dispatcher')
        self._logger.info("Initialized dispatcher")

        self.media_scanner = MediaScanner(self._logger)

        self.plugin_manager = PluginManager()

        # rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self._logger.info('Connected to RabbitMQ successfully')

        self.channel.exchange_declare(exchange=EXCHANGE_NAME, type='direct')

        # self.plugin_manager.add_plugin('metadata_fetcher')
        # self.plugin_manager.add_plugin('subtitle_downloader')

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
        self.plugin_manager.close()


if __name__ == '__main__':
    dispatcher = Dispatcher()
    sleep(4)
    dispatcher.close()
