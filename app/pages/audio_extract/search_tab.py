from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout

from app.components.view.AssetsTable import AssetsTable
from app.components.ItemSearch import ItemSearch
from qfluentwidgets import ScrollArea, InfoBar, InfoBarPosition

from app.pages.audio_extract import AEWorker
from app.pages.audio_extract.AudioTable import AudioTable


class SearchTab(ScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.__initWidget()
        self.lastText = ""
        self.worker = AEWorker()
        self.files = []
        self.parent_ = parent

    def __initWidget(self):
        # === Middle ===
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(10)
        self.setLayout(self.vBoxLayout)

        # === File Search ===
        self.fileSearch = ItemSearch()
        self.fileSearch.textChanged.connect(self.start_search_timeout)

        self.searchTimer = QTimer(self)
        self.searchTimer.setSingleShot(True)
        self.searchTimer.timeout.connect(self.search)

        # === Audio Table ===
        self.audioTable = AudioTable(self.parent(), self.PlayAudio, self.setAlias, self.export)

        self.vBoxLayout.addWidget(self.fileSearch)
        self.vBoxLayout.addWidget(self.audioTable, stretch=1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def export(self, index_list):
        pass

    def start_search_timeout(self):
        print(1)
        self.searchTimer.stop()
        self.searchTimer.start(300)

    def search(self):
        text = self.fileSearch.text()
        if text != self.lastText:  # Only trigger search if text has changed
            print(text)
            # Perform search here with the text
            self.lastText = text
            if text == "" or text is None:
                files = []
            else:
                files = self.worker.search(text)
            self.files = files
            self.audioTable.create_list(files)

    def PlayAudio(self, index: int, real_index):
        file_name = self.audioTable.item(real_index, 0).text()
        for file in self.files:
            if file.get_file_name() == file_name:
                audioMap = self.worker.ReadAudioFile(file.source)
                self.parent_.requestAudioPlay(audioMap, int(file.index))
                return

    def setAlias(self, index, name):
        pass
        # self.worker.set_alias(self.currentMap, index, name)
        # InfoBar.success(
        #     parent=self.parent_,
        #     title='Alias saved',
        #     content=f"",
        #     orient=Qt.Horizontal,
        #     isClosable=True,
        #     position=InfoBarPosition.BOTTOM_RIGHT,
        #     duration=1000,
        # )

    def reset(self):
        self.audioTable.table_reset()
