from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from qfluentwidgets import MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from .pages.home import HomeInterface
from .pages.audio_extract import AudioInterface


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
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


def navigations(window):
    return [
        Navigation('主页', FIF.HOME, HomeInterface(window)),
        Navigation('音频提取', FIF.ALBUM, AudioInterface(window)),
        Navigation('过场CG', FIF.CAMERA, Widget("Cutscene Interface", window)),
        Navigation('工具箱', FIF.DEVELOPER_TOOLS, Widget("Tool Interface", window)),
        Navigation('帮助', FIF.BOOK_SHELF, Widget("Help Interface", window)),
        Navigation('设置', FIF.SETTING, Widget("Settings Interface", window), isBottom=True),
    ]
