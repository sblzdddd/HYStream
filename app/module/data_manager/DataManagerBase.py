from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage


class DataManagerBase:
    def __init__(self, data_path, data_class, backup=None):
        self.backupName = backup
        self.backupPath = None
        self.dataPath = data_path
        # self.db = TinyDB(self.dataPath, sort_keys=True, indent=4, separators=(',', ': '))
        self.db = TinyDB(self.dataPath, storage=CachingMiddleware(JSONStorage), ensure_ascii=False, encoding="utf-8")
        self.query = Query()
        self.data_class = data_class

    def save(self, data):
        self.db.insert(data.to_dict())

    def get(self, value, key, length=False):
        # noinspection PyTypeChecker
        result = self.db.search(self.query[key] == value)
        if len(result) == 0:
            return None
        if length:
            return len(result)
        return [self.data_class.from_dict(i) for i in result]

    def get_all(self):
        return self.db.all()

    def delete_all(self):
        self.db.truncate()

    def delete(self, value, key):
        # noinspection PyTypeChecker
        self.db.remove(self.query[key] == value)

