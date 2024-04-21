import os
import time
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal

from app.module import file_md5
from app.module.audio_extract import AudioExtractor as ae
from app.module.data_manager import AudioFileDataManager, AudioFileData, AudioMapData


class AEWorker(QObject):
    allFinished = pyqtSignal(list)
    oneFinished = pyqtSignal(int)
    onLog = pyqtSignal(str)
    onSetTitle = pyqtSignal(str)
    onDurationChanged = pyqtSignal(str, float)

    def __init__(self):
        super().__init__()
        self.fileDataManager = AudioFileDataManager()

    def scan_files(self, folder):
        files = ae.scan_banks(folder)
        return files

    def do_import_job(self, lock, files):
        with lock:
            time.sleep(0.5)

            completed = 0
            filesLength = []

            for file in files:
                file_name = os.path.basename(file)
                self.onSetTitle.emit(f"Processing {file_name}...")

                md5 = file_md5(file)
                mapData = self.fileDataManager.get(os.path.abspath(file), "path")
                if mapData is None or mapData[0].md5 != md5:
                    mapData = ae.parse_waves(file, self.onLog.emit)
                    mapData.md5 = md5
                    self.fileDataManager.save(mapData)
                else:
                    mapData = mapData[0]
                filesLength.append(len(mapData.files))

                completed += 1
                self.oneFinished.emit(completed)
            self.onLog.emit(f"{completed} files completed (0 errors)")
            self.onLog.emit("Saving to database...")
            self.onSetTitle.emit("Saving to database...")
            self.fileDataManager.db.storage.flush()
            self.allFinished.emit(filesLength)

    def ReadAudioFile(self, source_file: str) -> List[AudioFileData] | None:
        data = self.fileDataManager.get(source_file, "path")
        if data:
            return data[0]
        return None

    def extract(self, data: AudioMapData, index: int) -> str:
        file = data.files[index]
        out = file.get_cached_path(False)
        if not os.path.exists(out):
            out, duration = ae.decrypt_wave(file)
            if file.duration == 0:
                data.files[index].duration = duration
                self.fileDataManager.update(data)
                self.onDurationChanged.emit(file.get_file_name(), duration)
                self.fileDataManager.db.storage.flush()
        return out

    def set_alias(self, data: AudioMapData, index: int, alias: str):
        data.files[index].alias = alias
        self.fileDataManager.update(data)
        self.fileDataManager.db.storage.flush()

    def search(self, alias):
        return self.fileDataManager.search_by_alias(alias)

    def getAudioFilesLength(self):
        return self.fileDataManager.getLength()
