import unittest

from template_plugin.template import TemplatePlugin


class TestPlugin(TemplatePlugin):
    def on_message(self, message):
        pass


class SubscriberTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass