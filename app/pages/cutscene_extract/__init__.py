# coding:utf-8
import os
import threading
import time

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QListWidgetItem, QLabel, QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QRect

from qfluentwidgets import ScrollArea, PushButton, PrimarySplitPushButton, RoundMenu, Action, InfoBar, InfoBarPosition, \
    ComboBox

from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.multimedia import StandardMediaPlayBar, VideoWidget

from app.components.Tab import Tab
from app.components.TopPanel import TopPanel
from app.components.dialog.FileDialog import FileDialog
from app.components.dialog.LoadingDialog import LoadingDialog

from app.module.stylesheet import StyleSheet
from app.pages.cutscene_extract.CutsceneExtractWorker import CEWorker
from app.pages.cutscene_extract.VideoList import VideoList
from app.module.cutscene_extract import extract


class CutscenePlayer(VideoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.playBar.fadeOut()

    def enterEvent(self, e):
        self.isHover = True
        self.playBar.fadeIn()

    def leaveEvent(self, e):
        self.isHover = False
        self.playBar.fadeOut()


class CutsceneInterface(ScrollArea):
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
        self.worker = CEWorker()
        self.audioLoading = False
        self.currentPlaying = None

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('cutsceneInterface')
        StyleSheet.GENERAL_INTERFACE.apply(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(15)

        # ================ Top Panel ================
        top_panel = TopPanel("Cutscene Explorer", self.view)

        # cache info
        length = self.worker.getVideoFilesLength()
        self.cached_label = QLabel(f"{length} cutscene files cached")
        self.cached_label.setObjectName("cachedLabel")
        top_panel.addWidget(self.cached_label)

        importBtn = PrimarySplitPushButton(FIF.ADD, 'Load files (.usm)')
        importBtn.clicked.connect(lambda: self.import_files())

        # Create menu
        self.menu = RoundMenu(parent=importBtn)
        self.menu.addAction(Action(FIF.FOLDER, 'Scan Folder', triggered=lambda: self.import_folder()))
        self.menu.addAction(Action(FIF.HISTORY, 'Import Cached', triggered=lambda: print("not implemented")))

        # Add menu
        importBtn.setFlyout(self.menu)

        clearBtn = PushButton("Clear")
        clearBtn.clicked.connect(lambda: self.reset())

        comboBox = ComboBox(self)
        comboBox.setPlaceholderText("Specify game")

        items = ['GI', 'SR']
        comboBox.addItems(items)
        comboBox.setCurrentIndex(1)

        comboBox.currentTextChanged.connect(print)

        top_panel.add_widgets([comboBox, clearBtn, importBtn])

        self.vBoxLayout.addLayout(top_panel)

        # ================ Middle Content ================
        self.body = QHBoxLayout(self.view)

        self.videoWidget = CutscenePlayer(self)

        # ================ Video File List ================
        self.fileList = VideoList(self)
        self.fileList.setMinimumWidth(400)
        self.fileList.onFileOpened.connect(self.requestVideoPlay)

        self.body.addWidget(self.fileList)
        self.body.addWidget(self.videoWidget, stretch=1)

        self.vBoxLayout.addLayout(self.body)

        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def import_folder(self):
        self.targetFolder = self.fd.openFolderDialog()
        if self.targetFolder is not None:
            files = self.worker.scan_files(self.targetFolder)
            if files and len(files) > 0:
                self.fileList.create_list(files)

    def import_files(self):
        files = self.fd.openFileDialog("Cutscene Files (*.usm)", ".usm")
        if files is not None:
            self.fileList.create_list(files)

    def updateFinish(self, value):
        pass

    def import_finished(self, length):
        pass

    def requestVideoPlay(self, path):
        print(path)
        extract(path)

    def reset(self):
        self.fileList.reset()
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
            content=f"{number} new cutscene(s) have been imported",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self
        )
