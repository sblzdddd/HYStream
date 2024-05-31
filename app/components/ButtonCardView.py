from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect, QHBoxLayout

from qfluentwidgets import IconWidget, FlowLayout, CardWidget
from app.module.stylesheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF


class ButtonCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, content, action, parent=None):
        super().__init__(parent=parent)

        self.action = action

        self.iconWidget = IconWidget(icon, self)
        self.iconOpacityEffect = QGraphicsOpacityEffect(self)
        self.iconOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.iconWidget.setGraphicsEffect(self.iconOpacityEffect)

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.titleOpacityEffect = QGraphicsOpacityEffect(self)
        self.titleOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.titleLabel.setGraphicsEffect(self.titleOpacityEffect)
        self.contentLabel = QLabel(content, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        # self.setFixedSize(160, 200)
        self.iconWidget.setFixedSize(32, 32)

        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(25, 10, 10, 10)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignLeft)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if callable(self.action):
            try:
                self.action()
            except Exception as e:
                print(f"执行失败：{e}")
        elif isinstance(self.action, dict):
            pass


class CardList(QWidget):
    """ Sample card view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayouts = []
        self.count = 0

        self.vBoxLayout.setContentsMargins(20, 0, 20, 20)
        self.vBoxLayout.setSpacing(10)

        # self.vBoxLayout.addWidget(self.titleLabel)

        # self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def addCard(self, icon, title, content, action):
        """ add sample card """
        card = ButtonCard(icon, title, content, action, self)
        self.count += 1

        if self.count % 2 == 1:
            hBoxLayout = QHBoxLayout(self)
            hBoxLayout.setContentsMargins(0, 0, 0, 0)
            hBoxLayout.setSpacing(10)
            self.hBoxLayouts.append(hBoxLayout)
            self.vBoxLayout.addLayout(self.hBoxLayouts[-1])
        self.hBoxLayouts[-1].addWidget(card, 1)
