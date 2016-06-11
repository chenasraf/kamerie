import os

from kamerie.utilities.consts import TYPE_MOVIE, TYPE_SERIES, LIBRARY_PATH, LIBRARY_TYPE, MEDIA_PATH, MEDIA_TYPE, \
    SCANNED, MEDIA_FILE_EXTENSIONS
from kamerie.utilities.db import db, attrs_to_db_set


class MediaScanner(object):
    def __init__(self, logger):
        self.db = db
        self._logger = logger

    def scan_directory(self, directory, media_type):
        if media_type not in [TYPE_MOVIE, TYPE_SERIES]:
            self._logger.error('media_type wrong: %s' % media_type)

        attributes = {
            LIBRARY_PATH: directory,
            LIBRARY_TYPE: media_type,
        }
        library = self.db.Library.find_one(attributes)

        if library is None:
            self._logger.info("Adding library: %s" % str(attributes))
            self.db.Library.insert_one(attributes)

        for dirname, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.lower().endswith(MEDIA_FILE_EXTENSIONS):
                    self._logger.info('Parsing %s: %s' % (media_type, os.path.join(dirname, filename)))
                    attributes = self.parse_file(dirname=dirname, filename=filename, media_type=media_type)
                    yield self.get_db_record(**attributes)
                else:
                    self._logger.info('Ignoring %s: %s' % (media_type, os.path.join(dirname, filename)))

    def parse_file(self, dirname, filename, media_type):
        return {
            MEDIA_PATH: os.path.join(dirname, filename),
            MEDIA_TYPE: media_type,
            SCANNED: True,
        }

    def get_db_record(self, **attributes):
        result = self.db.Media.find_one({
            MEDIA_PATH: attributes[MEDIA_PATH],
            MEDIA_TYPE: attributes[MEDIA_TYPE],
        })

        if result is None:
            self._logger.info("Adding media: %s" % str(attributes))
            result = self.db.Media.insert_one(attributes)
            return self.db.Media.find_one({'_id': result.inserted_id})
        else:
            self._logger.info("Updating media: %s" % str(attributes))
            self.db.Media.update_one({'_id': result['_id']}, attrs_to_db_set(attributes))
            return result
