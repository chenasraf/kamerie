import os

TYPE_MOVIE = 'movie'
TYPE_SERIES = 'series'


class MediaScanner(object):
    def scan_directory(self, directory, media_type):
        if media_type not in [TYPE_MOVIE, TYPE_SERIES]:
            print 'media_type wrong: %s' % media_type
            # self._logger.error('media_type wrong: %s' % media_type)

        for dirname, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                attributes = self.parse_file(dirname=dirname, filename=filename, media_type=media_type)
                self.add_file_to_library(filename, **attributes)

    def parse_file(self, dirname, filename, media_type):
        print 'parsing %s: %s' % (media_type, os.path.join(dirname, filename))
        # self._logger.info('parsing %s: %s' % media_type, os.path.join(dirname, file))
        return {}

    def add_file_to_library(self, filename, **attributes):
        pass