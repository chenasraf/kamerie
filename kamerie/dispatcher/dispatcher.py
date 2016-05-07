"""
Dispatcher API daemon
"""
import logging
from os import listdir
from os.path import isdir, exists
import os
import imp

from template_plugin.consts import DISPATCHER_NAME


PLUGIN_DIRECTORY = '/home/dor/dev/python/kamerie/kamerie-plugins/'


class Dispatcher(object):
    def __init__(self):
        # Prepare instance
        self.name = DISPATCHER_NAME

        # Prepare logger
        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)

        self._logger.info("Initialized dispatcher")
        self.plugins = self.register_plugins()

        for plugin in self.plugins:
            plugin['plugin_cls'].on_message('/home/dor/Videos/movies')

    def register_plugins(self):
        plugin_list = []
        plugin_path = lambda plugin: os.path.join(PLUGIN_DIRECTORY, plugin)
        plugins = filter(lambda x: isdir(plugin_path(x)) and x[0] is not '.', listdir(PLUGIN_DIRECTORY))

        for plugin in plugins:
            config_path = os.path.join(plugin_path(plugin), 'plugin.py')
            config_import = imp.load_source('kamerie_plugin_%s' % plugin, config_path)

            if exists(config_path):
                plugin_conf = {
                    'name': plugin,
                    'path': plugin_path(plugin),
                    'config_path': config_path,
                    'plugin_cls': config_import.Plugin(plugin, self._logger)
                }
                plugin_list.append(plugin_conf)

        return plugin_list

    def start(self):
        self._logger.info("Starting" % self.name)

    def on_message(self, message):
        raise NotImplementedError

    def send_message(self, message):
        pass

    def __exit__(self):
        self.close()

    def close(self):
        pass


if __name__ == '__main__':
    Dispatcher()