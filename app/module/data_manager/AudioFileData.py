import os
from app.module import md5_hash
from typing import Tuple, List
from app.module.data_manager.DataManagerBase import DataManagerBase

CACHE_PATH = "./cached/"
if not os.path.exists("cached/"):
    os.makedirs("cached/", exist_ok=True)


class AudioFileData:
    def __init__(self, source: str = "", index: str = "", duration: int = 0, alias: str = "", position: int = 0,
                 size: int = 0):
        self.source = source
        self.index = index
        self.duration = duration
        self.alias = alias
        self.position = position
        self.size = size

    def get_source_name(self):
        return os.path.basename(self.source).rstrip('.pck')

    def get_file_name(self) -> str:
        return f"{self.get_source_name()}_{self.index}.wav"

    def get_cached_path(self, raw=True):
        source_hash = md5_hash(self.source)
        file_path = f"{source_hash}@{self.index}.{'raw.wav' if raw else 'wav'}"
        full_path = os.path.join(CACHE_PATH, file_path)
        return os.path.abspath(full_path)

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, json_data):
        return cls(**json_data)


class AudioMapData:
    def __init__(self, path: str = "", files: List[AudioFileData] = None, md5: str = ""):
        self.path: str = path
        self.files: List[AudioFileData] = files
        self.md5: str = md5

    def to_dict(self):
        dict_ = self.__dict__.copy()
        if not isinstance(dict_["files"][0], dict):
            dict_["files"] = [i.to_dict().copy() for i in self.files]
        return dict_

    @classmethod
    def from_dict(cls, json_data):
        obj = cls(**json_data)
        obj.files = [AudioFileData.from_dict(f) for f in obj.files]
        return obj


AUDIO_DATA_PATH = "cached/audio_data.json"


class AudioFileDataManager(DataManagerBase):
    def __init__(self, data_path=AUDIO_DATA_PATH):
        super().__init__(data_path, AudioMapData)
        # self.db.create_index('path')

    def update(self, data: AudioMapData):
        self.db.update(data.to_dict(), self.query.path == data.path)

    def search_by_alias(self, string):
        result = []
        for i in self.db:
            files = [AudioFileData.from_dict(file) for file in i["files"] if string in file["alias"]]
            if files:
                result += files
        return result

    def getLength(self):
        length = 0
        for i in self.db:
            length += len(i["files"])
        return length


if __name__ == '__main__':
    m = AudioFileDataManager()
    result = m.search_by_alias("bgm")
    print(result)
