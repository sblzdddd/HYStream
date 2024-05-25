# coding:utf-8
import os
import threading
import time

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QListWidgetItem, QLabel
from PyQt5.QtCore import QPropertyAnimation, QRect

from qfluentwidgets import ScrollArea, PushButton, PrimarySplitPushButton, RoundMenu, Action, InfoBar, InfoBarPosition

from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.multimedia import StandardMediaPlayBar

from app.components.Tab import Tab
from app.components.TopPanel import TopPanel
from app.components.dialog.FileDialog import FileDialog
from app.components.dialog.LoadingDialog import LoadingDialog

from app.module.stylesheet import StyleSheet
from app.pages.audio_extract.AudioExtractWorker import AEWorker
from app.pages.audio_extract.browse_tab import BrowseTab
from app.pages.audio_extract.search_tab import SearchTab


class AudioInterface(ScrollArea):
    """ Audio interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.import_thread = None
        self.view = QWidget(self)

        self.targetFolder = None
        self.win = parent
        self.fd = FileDialog()
        self.loadingDiag = LoadingDialog(self.win)
        self.files = []
        self.fileLengths = []
        self.worker = AEWorker()
        self.audioLoading = False
        self.currentPlaying = None

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('audioInterface')
        StyleSheet.GENERAL_INTERFACE.apply(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(15)

        # Top Panel
        top_panel = TopPanel("Audio Bank Explorer", self.view)

        importBtn = PrimarySplitPushButton(FIF.ADD, 'Load files (.pck)')
        importBtn.clicked.connect(lambda: self.import_files())

        # Create self.menu
        self.menu = RoundMenu(parent=importBtn)
        self.menu.addAction(Action(FIF.FOLDER, 'Scan Folder', triggered=lambda: self.import_folder()))
        self.menu.addAction(Action(FIF.HISTORY, 'Import Cached', triggered=lambda: print("not implemented")))

        # Add self.menu
        importBtn.setFlyout(self.menu)

        clearBtn = PushButton("Clear")
        clearBtn.clicked.connect(lambda: self.reset())

        top_panel.add_widgets([clearBtn, importBtn])

        self.vBoxLayout.addLayout(top_panel)

        # Middle Stacked
        self.body = Tab(self)
        self.browseTab = BrowseTab(self)
        self.searchTab = SearchTab(self)

        self.body.addSubInterface(self.browseTab, "browseTab", "Browse")
        self.body.addSubInterface(self.searchTab, "searchTab", "Search")
        self.body.setTab(0)

        self.body.pivot.setFixedWidth(260)

        length = self.worker.getAudioFilesLength()
        self.cached_label = QLabel(f"{length} audio files cached")
        self.cached_label.setObjectName("cachedLabel")
        self.body.tabHeads.addWidget(self.cached_label)

        self.vBoxLayout.addWidget(self.body)

        # Bottom
        self.playBar = None

        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def import_folder(self):
        self.targetFolder = self.fd.openFolderDialog()
        if self.targetFolder is not None:
            files = self.worker.scan_files(self.targetFolder)
            self.start_import_thred(files)

    def import_files(self):
        files = self.fd.openFileDialog("Bank Files (*.pck)", ".pck")
        if files is not None:
            self.start_import_thred(files)

    def start_import_thred(self, files):
        new_files = []
        for file in files:
            if file not in self.files:
                new_files.append(os.path.abspath(file))
        if len(new_files) <= 0:
            self.show_import_success_message("No")
            return
        self.loadingDiag = LoadingDialog(self.win)
        self.files += new_files
        self.loadingDiag.setTotalValue(len(new_files))
        self.loadingDiag.log(f"Processing {len(new_files)} bank files")

        self.loadingDiag.log("Scanning Files...")
        self.worker.oneFinished.connect(self.updateFinish)
        self.worker.allFinished.connect(self.import_finished)
        self.worker.onLog.connect(self.loadingDiag.log)
        self.worker.onSetTitle.connect(self.loadingDiag.setTitle)

        lock = threading.Lock()
        self.import_thread = threading.Thread(target=self.worker.do_import_job, args=[lock, new_files])
        self.import_thread.start()

        self.loadingDiag.show()

    def updateFinish(self, value):
        if self.loadingDiag.total > 0:
            self.loadingDiag.updateValue(value)
        # QApplication.processEvents()

    def import_finished(self, length):
        self.loadingDiag.accept()
        self.fileLengths += length
        self.browseTab.GenerateFileList(self.files, self.fileLengths)
        self.worker.oneFinished.disconnect(self.updateFinish)
        self.worker.allFinished.disconnect(self.import_finished)
        self.worker.onLog.disconnect(self.loadingDiag.log)
        self.worker.onSetTitle.disconnect(self.loadingDiag.setTitle)
        self.show_import_success_message(len(length))
        length = self.worker.getAudioFilesLength()
        self.cached_label.setText(f"{length} audio files cached")

    def init_playbar(self):
        self.playBar = StandardMediaPlayBar()
        self.playBar.setVolume(75)
        self.playBar.setObjectName("playBar")
        self.vBoxLayout.addWidget(self.playBar)

    def destroy_playbar(self):
        if self.playBar:
            self.playBar.player.stop()
            self.vBoxLayout.removeWidget(self.playBar)
            self.playBar.deleteLater()
            self.playBar = None

    def requestAudioPlay(self, data, index):
        if self.currentPlaying and (data.files[index].source == self.currentPlaying.source and
                                    data.files[index].index == self.currentPlaying.index):
            return
        self.currentPlaying = data.files[index]
        if not self.playBar:
            self.init_playbar()
        self.playBar.player.stop()
        path = self.worker.extract(data, index)
        url = QUrl.fromLocalFile(os.path.abspath(path))
        self.playBar.player.setSource(url)
        self.playBar.player.mediaStatusChanged.connect(self.handle_status)
        self.audioLoading = True

    def handle_status(self, status):
        if status == QMediaPlayer.LoadedMedia and self.audioLoading:
            self.playBar.player.play()
            self.audioLoading = False

    def reset(self):
        self.import_thread = None
        self.targetFolder = None
        self.loadingDiag = LoadingDialog(self.win)
        self.files = []
        self.fileLengths = []
        self.audioLoading = False
        self.destroy_playbar()
        self.browseTab.reset()
        InfoBar.success(
            title='Workspace has been reset',
            content=f"",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )

    def show_import_success_message(self, number):
        InfoBar.success(
            title='Files Imported Successful',
            content=f"{number} new pck banks has been imported",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self
        )
