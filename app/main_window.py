from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QHBoxLayout

from contextlib import redirect_stdout

from app.module.GlobalObject import GlobalObject

with redirect_stdout(None):
    from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, setThemeColor, \
         NavigationBarPushButton, toggleTheme, setTheme, Theme, MessageBox, isDarkTheme
    from qfluentwidgets import FluentIcon as FIF

from app.navigations import navigations

import base64


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        self.initInterface()
        self.navigations = navigations(self)
        self.initNavigation()

        # 检查更新
        # checkUpdate(self, flag=True)
        # checkAnnouncement(self)

    def initWindow(self):

        setThemeColor('#8b9aee', lazy=True)
        setTheme(Theme.DARK, lazy=True)
        self.setMicaEffectEnabled(False)

        # 创建启动画面
        self.splashScreen = SplashScreen(QIcon('./resources/images/favicon.ico'), self)
        self.splashScreen.setIconSize(QSize(150, 150))
        self.splashScreen.raise_()

        # 禁用最大化
        # self.titleBar.maxBtn.setHidden(True)
        # self.titleBar.maxBtn.setDisabled(True)
        # self.titleBar.setDoubleClickEnabled(False)
        # self.setResizeEnabled(False)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.resize(1080, 700)
        self.setMicaEffectEnabled(True)
        self.setMinimumSize(900, 640)
        self.setWindowIcon(QIcon('./resources/images/window_icon.png'))
        self.setWindowTitle("HYStream")


        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()

    def initInterface(self):
        pass

    def initNavigation(self):
        for n in self.navigations:
            n.register(self)

        self.navigationInterface.addWidget(
            'themeButton',
            NavigationBarPushButton(FIF.CONSTRACT, '主题', isSelectable=False),
            lambda: toggleTheme(lazy=True),
            NavigationItemPosition.BOTTOM)

        self.Switch(1)
        self.splashScreen.finish()

    def Switch(self, index):
        self.switchTo(self.navigations[index].component)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if event.oldState() and Qt.WindowMinimized:
                print("WindowMinimized")
                GlobalObject().dispatchEvent("Minimized")
            elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                print("WindowMaximized")
                GlobalObject().dispatchEvent("Maximized")
