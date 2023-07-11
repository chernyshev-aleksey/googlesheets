import pymongo

from src import settings


class DataBaseGoogleSheet:
    def __init__(self, config):
        self.db = pymongo.MongoClient(
            settings.CONNECTION_STRING, ssl=True, tlsCAFile=config.CA_FILE)[config.DB_NAME]
        self.collection = self.db[config.DB_COL_NAME]

    def get_credential(self, name):
        return self.collection.find_one({'name': name})
