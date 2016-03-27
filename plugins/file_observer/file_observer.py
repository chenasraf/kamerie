import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class FileObserver:

    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
        event_handler = LoggingEventHandler()
        observer = Observer()

        observer.schedule(event_handler, path, recursive=True)
        print 'Now watching: %s' % (os.path.abspath(path))
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print '\rInterrupted by user'
            observer.stop()

        observer.join()
