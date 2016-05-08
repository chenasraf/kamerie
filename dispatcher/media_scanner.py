import os

from pymongo import MongoClient

from kamerie.utilities.consts import TYPE_MOVIE, TYPE_SERIES, LIBRARY_PATH, LIBRARY_TYPE, MEDIA_PATH, MEDIA_TYPE, \
    SCANNED


class MediaScanner(object):
    def __init__(self, logger):
        self.db = MongoClient('mongodb://localhost:27017').kamerie
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
                attributes = self.parse_file(dirname=dirname, filename=filename, media_type=media_type)
                yield self.get_db_record(**attributes)

    def parse_file(self, dirname, filename, media_type):
        self._logger.info('Parsing %s: %s' % (media_type, os.path.join(dirname, filename)))
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
            self.db.Media.update_one({'_id': result['_id']}, self._attrs_to_db_set(attributes))
            return result

    def _attrs_to_db_set(self, attributes):
        setter = {
            '$set': {},
            '$currentDate': {'lastModified': True}
        }
        for key, value in attributes.iteritems():
            setter['$set'][key] = value

        return setter
