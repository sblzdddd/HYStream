from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import ScrollArea, InfoBar, InfoBarPosition

from app.module.data_manager import AudioMapData
from app.pages.audio_extract import AudioExtractWorker
from app.pages.audio_extract.AudioTable import AudioTable
from app.pages.audio_extract.FileList import FileList


class BrowseTabState(Enum):
    IDLE = 1
    CREATING_FILELIST = 2
    CREATING_AUDIOLIST = 3

class BrowseTab(ScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.__initWidget()
        self.parent_ = parent
        self.worker: AudioExtractWorker = self.parent_.worker
        self.currentMap: AudioMapData | None = None
        self.currentSelectedFile = None
        self.state: BrowseTabState = BrowseTabState.IDLE

    def __initWidget(self):
        # === Middle ===
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(10)
        self.setLayout(self.hBoxLayout)

        # === FIle List ===
        self.fileList = FileList(self.parent())
        self.setObjectName("fileList")
        self.fileList.onFileOpened.connect(self.OpenFile)
        self.fileList.setMinimumWidth(300)
        self.hBoxLayout.addWidget(self.fileList)

        # === Audio Table ===
        self.audioTable = AudioTable(self.parent(), self.PlayAudio, self.setAlias)
        self.hBoxLayout.addWidget(self.audioTable, stretch=1)

    def GenerateFileList(self, files, length):
        self.state = BrowseTabState.CREATING_FILELIST
        self.fileList.create_list(files, length)
        self.worker.onDurationChanged.connect(self.audioTable.updateDuration)
        self.state = BrowseTabState.IDLE

    def OpenFile(self, path):
        self.state = BrowseTabState.CREATING_AUDIOLIST

        if self.currentSelectedFile == path:
            return

        audioMap: None | AudioMapData = self.worker.ReadAudioFile(path)
        if audioMap is not None:
            self.currentSelectedFile = path
            self.currentMap = audioMap
            self.audioTable.create_list(self.currentMap.files)

        self.state = BrowseTabState.IDLE

    def PlayAudio(self, index: int, real_index):
        self.parent_.requestAudioPlay(self.currentMap, index)

    def setAlias(self, index, name):
        self.worker.set_alias(self.currentMap, index, name)
        InfoBar.success(
            parent=self.parent_,
            title='Alias saved',
            content=f"",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=1000,
        )

    def reset(self):
        self.fileList.reset()
        self.audioTable.table_reset()
        self.currentMap = None
        self.currentSelectedFile = None
