from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from qfluentwidgets import MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from .pages.home import HomeInterface
from .pages.audio_extract import AudioInterface
from .pages.settings import SettingInterface
from .pages.cutscene_extract import CutsceneInterface


class Navigation:
    def __init__(self, name, icon, component, isBottom=False):
        self.name = name
        self.icon = icon
        self.component = component
        self.isBottom = isBottom

    def register(self, window: MSFluentWindow):
        window.addSubInterface(self.component, self.icon, window.tr(self.name),
                               position=NavigationItemPosition.BOTTOM if self.isBottom else NavigationItemPosition.TOP)


class Widget(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


def navigations(window):
    return [
        Navigation(window.tr('Home'), FIF.HOME, HomeInterface(window)),
        Navigation(window.tr('Audio'), FIF.ALBUM, AudioInterface(window)),
        Navigation(window.tr('Cutscene'), FIF.CAMERA, CutsceneInterface(window)),
        Navigation(window.tr('Tools'), FIF.DEVELOPER_TOOLS, Widget("Tool Interface", window)),
        Navigation(window.tr('Help'), FIF.BOOK_SHELF, Widget("Help Interface", window)),
        Navigation(window.tr('Settings'), FIF.SETTING, SettingInterface(window), isBottom=True),
    ]
