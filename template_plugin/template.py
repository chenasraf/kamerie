import json

import pika


class TemplatePlugin(object):
    def __init__(self, plugin_name, logger=None):# rabbitmq_settings
        # Prepare instance
        self.name = plugin_name
        self._logger = logger
        if self._logger:
            self._logger.info("Initialized %s plugin" % self.name)

        # Connect to rabbitmq queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange='kamerie-distribute', type='direct')
        self._channel.queue_declare(queue=self.name)
        self._channel.queue_bind(queue=self.name, exchange='kamerie-distribute', routing_key='')
        if self._logger:
            self._logger.info("Established %s's MQ connection" % self.name)

    def start(self):
        if self._logger:
            self._logger.info("Starting %s" % self.name)
        print "Starting %s" % self.name
        self._channel.basic_consume(self._message_received, queue=self.name, no_ack=True, exclusive=True)
        self._channel.start_consuming()

    def _message_received(self, channel, method, properties, message):
        message = json.loads(message)
        if self.name not in message.get('plugins', []):
            self.on_message(message)

    def on_message(self, message):
        raise NotImplementedError("n00b")

    def send_message(self, message):
        pass
        # self._channel.basic_publish(exchange=self.rabbitmq_settings['exchange'],
        #                             routing_key=self.rabbitmq_settings['routing_key'],
        #                             body=message)

    def __exit__(self):
        self.close()

    def close(self):
        pass
        # self._connection.close()
