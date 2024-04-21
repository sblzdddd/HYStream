# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect

from qfluentwidgets import ScrollArea, FluentIcon

from app.module.stylesheet import StyleSheet
from app.components.linkcard import LinkCardView
from app.components.card.samplecardview1 import SampleCardView1
# from tasks.base.tasks import start_task

# from module.config import cfg

from PIL import Image
import numpy as np

from app.module.GlobalObject import GlobalObject


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent_ = parent

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(f'HYStream', self)
        self.galleryLabel.setStyleSheet("color: black;font-size: 40px; font-weight:800;")
        self.introLabel = QLabel(f'Version 1.0', self)
        self.introLabel.setStyleSheet("color: black;font-size: 20px; font-weight:600;")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        shadow.setOffset(0.5, 1)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)

        # 创建阴影效果
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(16)  # 阴影模糊半径
        shadow2.setColor(Qt.black)  # 阴影颜色
        shadow2.setOffset(0.5, 1)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.introLabel.setGraphicsEffect(shadow2)

        self.img = Image.open("./resources/images/home_bg.jpg")
        self.banner = None
        self.path = None
        self.lastSize = (0, 0)

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
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.introLabel)
        # self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.addLayout(linkCardLayout)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr('Source Code Here!'),
            "https://github.com/sblzdddd/HYStream",
        )

        self.globalObj = GlobalObject()
        self.globalObj.addEventListener("Maximized", self.repaint)
        self.globalObj.addEventListener("Minimized", self.repaint)

    def repaint(self):
        self.lastSize = QSize(0, 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        if self.lastSize != self.size():
            self.lastSize = self.size()
            max_height = int(self.parent_.height() - 300)
            real_height = self.width() * self.img.height // self.img.width
            img = self.img
            if real_height > max_height:
                image_height = self.img.width * self.height() // self.width()
                crop_area = (0, 0, self.img.width, image_height)  # (left, upper, right, lower)
                img = self.img.crop(crop_area)

            img_data = np.array(img)  # Convert PIL Image to numpy array

            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)

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
        self.banner = BannerWidget(self)
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
        basicInputView = SampleCardView1(
            self.tr(" 功能"), self.view)

        basicInputView.addSampleCard(
            icon="./resources/images/sound_ic.png",
            title="音频提取",
            action=lambda: self.win.Switch(1)
        )
        basicInputView.addSampleCard(
            icon="./resources/images/sound_ic.png",
            title="过场CG",
            action=lambda: self.win.Switch(2)
        )
        basicInputView.addSampleCard(
            icon="./resources/images/sound_ic.png",
            title="工具箱",
            action=lambda: self.win.Switch(3)
        )
        basicInputView.addSampleCard(
            icon="./resources/images/sound_ic.png",
            title="文档",
            action=lambda: self.win.Switch(4)
        )
        # basicInputView.addSampleCard(
        #     icon="./resources/images/SilverWolf.jpg",
        #     title="锄大地",
        #     action={
        #         "快速启动 ⭐": lambda: start_task("fight"),
        #         "原版运行": lambda: start_task("fight_gui"),
        #         "更新锄大地": lambda: start_task("fight_update"),
        #         "重置配置文件": lambda: os.remove(os.path.join(cfg.fight_path, "config.json")),
        #         "打开程序目录": lambda: os.startfile(cfg.fight_path),
        #         "打开项目主页": lambda: os.startfile("https://github.com/linruowuyin/Fhoe-Rail"),
        #     }
        # )
        # basicInputView.addSampleCard(
        #     icon="./resources/images/Herta.jpg",
        #     title="模拟宇宙",
        #     action={
        #         "快速启动 ⭐": lambda: start_task("universe"),
        #         "原版运行": lambda: start_task("universe_gui"),
        #         "更新模拟宇宙": lambda: start_task("universe_update"),
        #         "重置配置文件": lambda: os.remove(os.path.join(cfg.universe_path, "info.yml")),
        #         "打开程序目录": lambda: os.startfile(cfg.universe_path),
        #         "打开项目主页": lambda: os.startfile("https://github.com/CHNZYX/Auto_Simulated_Universe"),
        #     }
        # )
        # basicInputView.addSampleCard(
        #     icon="./resources/images/Bronya.jpg",
        #     title="逐光捡金",
        #     action={
        #         "混沌回忆": lambda: start_task("forgottenhall"),
        #         "虚构叙事": lambda: start_task("purefiction"),
        #     }
        # )

        self.vBoxLayout.addWidget(basicInputView)
