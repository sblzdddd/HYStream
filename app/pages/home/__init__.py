# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QImage, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect

from qfluentwidgets import ScrollArea, FluentIcon

from app.module.config import VERSION
from app.module.stylesheet import StyleSheet
from app.components.linkcard import LinkCardView
from app.components.ButtonCardView import CardList

from PIL import Image

from app.module.signal_bus import signalBus


class BannerWidget(QWidget):
    def __init__(self, parent=None, window=None):
        super().__init__(parent=parent)

        self.window = window
        self.parent_ = parent

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(f'HYStream', self)
        self.galleryLabel.setStyleSheet("color: black;font-size: 40px; font-weight:800;")
        self.introLabel = QLabel(f'Version ' + VERSION, self)
        self.introLabel.setStyleSheet("color: black;font-size: 20px; font-weight:600;")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)  # 阴影模糊半径
        shadow.setColor(QColor(0, 0, 0, 150))  # 阴影颜色
        shadow.setOffset(0.5, 1)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)

        # 创建阴影效果
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(16)  # 阴影模糊半径
        shadow.setColor(QColor(0, 0, 0, 150))  # 阴影颜色
        shadow2.setOffset(0.5, 1)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.introLabel.setGraphicsEffect(shadow2)

        self.img = Image.open("./resources/images/home_bg.jpg")
        self.banner = None
        self.path = None
        self.lastWindowSize = QSize(0, 0)
        self.lastSize = QSize(0, 0)

        self.linkCardView = LinkCardView(self)

        self.linkCardView.setContentsMargins(0, 0, 0, 36)
        # self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        # self.vBoxLayout.setSpacing(40)

        self.galleryLabel.setObjectName('galleryLabel')
        self.introLabel.setObjectName('introLabel')

        # Create a horizontal layout for the linkCardView with bottom alignment and margin
        linkCardLayout = QHBoxLayout()
        linkCardLayout.addWidget(self.linkCardView)
        # linkCardLayout.setContentsMargins(0, 0, 0, 0)  # Add bottom margin of 20 units
        linkCardLayout.setAlignment(Qt.AlignBottom)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 20)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.introLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        # self.vBoxLayout.addLayout(linkCardLayout)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr('Source Code Here!'),
            "https://github.com/sblzdddd/HYStream",
        )

        signalBus.windowResized.connect(self.repaint)

    def repaint(self):
        self.lastWindowSize = QSize(0, 0)
        self.lastSize = QSize(0, 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if self.lastWindowSize != self.window.size() or self.lastSize != self.size():
            self.lastWindowSize = self.window.size()
            self.lastSize = self.size()
            max_height = int(self.parent_.height() - 220)
            real_height = self.width() * self.img.height // self.img.width
            img = self.img
            if real_height > max_height:
                image_height = self.img.width * self.height() // self.width()
                crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
                img = self.img.crop(crop_area)

            img_data = img.tobytes()  # Convert PIL Image to numpy array

            width, height = img.size
            channels = 3
            bytes_per_line = channels * width
            self.banner = QImage(img_data, width, height, bytes_per_line, QImage.Format_RGB888)

            real_height = min(real_height, max_height)
            self.setFixedHeight(real_height)

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self, parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()
        self.win = parent

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        basicInputView = CardList(self.view)

        basicInputView.addCard(icon=FluentIcon.MUSIC_FOLDER.icon(), title=self.tr("Audio Browser"),
                               content=self.tr("Parse .pck bank files; browse and extract audio clips"),
                               action=lambda: self.win.Switch(1))
        basicInputView.addCard(icon=FluentIcon.VIDEO.icon(), title=self.tr("Cutscene Browser"),
                               content=self.tr("Parse .usm cutscene files; preview and extract videos"),
                               action=lambda: self.win.Switch(2))
        basicInputView.addCard(icon=FluentIcon.DEVELOPER_TOOLS.icon(), title=self.tr("Toolbox"),
                               content=self.tr("Additional utilities"),
                               action=lambda: self.win.Switch(3))
        basicInputView.addCard(icon=FluentIcon.LIBRARY.icon(), title=self.tr("Help"),
                               content=self.tr("Read usage documentations"),
                               action=lambda: self.win.Switch(4))

        self.vBoxLayout.addWidget(basicInputView)
