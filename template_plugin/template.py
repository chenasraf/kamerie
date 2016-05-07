class TemplatePlugin(object):
    def __init__(self, plugin_name, logger):#, rabbitmq_settings
        # Prepare instance
        self.name = plugin_name
        self._logger = logger

        self._logger.info("Initialized %s plugin" % self.name)

        # Connect to rabbitmq queue
        # self.rabbitmq_settings = rabbitmq_settings
        # self._connection = pika.BlockingConnection(pika.ConnectionParameters(**self.rabbitmq_settings))
        # self._channel = self._connection.channel()
        # self._logger.info("Established %s's MQ connection\nMQ Settings: %s" % (self.name, str(self.rabbitmq_settings)))

    def start(self):
        self._logger.info("Starting" % self.name)
        # self._channel.start_consuming()

    def on_message(self, message):
        raise NotImplementedError

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