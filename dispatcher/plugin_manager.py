import os
import subprocess
from time import sleep

import psutil
import signal

from kamerie.utilities.consts import KAMERIE_PID_DIR, KAMERIE_PLUGINS_DIR, DEFAULT_MAIN_MODULE


class PluginManager(object):
    def __init__(self, pid_dir=KAMERIE_PID_DIR, plugin_dir=KAMERIE_PLUGINS_DIR):
        self.pid_dir = pid_dir
        self.plugin_dir = plugin_dir
        self.plugins = {}

        # TODO: take care of plugins dir - separate built-ins and downloaded
        for p in [pid_dir, plugin_dir]:
            if not os.path.exists(p) or not os.path.isdir(p):
                os.makedirs(p)

        # self.plugins = {
        #        "plugin1": <pid1>,
        #        "plugin2": <pid2>
        # }

    def close(self):
        for plugin in list(self.plugins):
            self.remove_plugin(plugin, self.plugins[plugin])

    def add_plugin(self, name):
        pid = self._create_process(name)
        if self._ping_pid(pid):
            self._create_pid_file(name, pid)
            self.plugins[name] = pid
        else:
            raise OSError('process was not created %s' % name)

    def remove_plugin(self, name, pid=None):
        if not self._check_alive(name):
            raise OSError('process not available %s' % name)
        if name not in self.plugins and self._get_pid(name):
            raise IOError('pid file exists but plugin was not registered')
        if name in self.plugins and not self._get_pid(name):
            raise TypeError('pid file does not exist but plugin was registered')
        self._kill_process(name, self._get_pid(name)if not pid else pid)
        self._remove_pid_file(name)
        self.plugins.pop(name)

    def _validate_plugin(self, name):
        package_path = os.path.join(self.plugin_dir, name)
        plugin_path = os.path.join(package_path, DEFAULT_MAIN_MODULE)
        if os.path.exists(package_path) and  os.path.isdir(package_path) and os.path.exists(plugin_path):
            return plugin_path
        else:
            raise IOError('plugin directory unavailable.\n\t(package: %s\n\tmodule: %s)' % (package_path, plugin_path))

    def _create_pid_file(self, name, pid):
        pid_filename = os.path.join(self.pid_dir, '%s.pid' % name)
        if not os.path.exists(pid_filename):
            with open(pid_filename, 'wb') as output_file:
                output_file.write(str(pid))
        else:
            self._kill_process(pid)
            raise IOError('pid file already exists. ' + pid_filename)

    def _remove_pid_file(self, name):
        pid_filename = os.path.join(self.pid_dir, '%s.pid' % name)
        if os.path.exists(pid_filename):
            os.remove(pid_filename)
        else:
            raise IOError('no such pid file exists. ' + pid_filename)

    def _create_process(self, name):
        path = self._validate_plugin(name)
        process = subprocess.Popen(("python", path))
        return process.pid

    def _kill_process(self, name, pid=None):
        pid = self._get_pid(name) if not pid else pid
        p = psutil.Process(pid)
        p.terminate()
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        sleep(.5)
        if self._ping_pid(pid):
            raise OSError('unable to kill process (%s, %d)' % (name, pid))

    def _get_pid(self, name):
        pid_filename = os.path.join(self.pid_dir, '%s.pid' % name)
        if os.path.exists(pid_filename):
            with open(pid_filename, 'rb') as input_file:
                return input_file.read().strip()
        else:
            return None

    def _check_alive(self, name):
        return self._ping_pid(self._get_pid(name))

    @staticmethod
    def _ping_pid(pid):
        if not pid:
            raise TypeError('None cannot be a pid')
        try:
            os.kill(int(pid), 0)
        except OSError:
            return False
        return True
