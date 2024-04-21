from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QWidget, QSizePolicy, QGraphicsOpacityEffect, QHBoxLayout
from qfluentwidgets import SegmentedWidget
from app.module.stylesheet import StyleSheet


class Tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        StyleSheet.TAB.apply(self)
        self.parent = parent
        self.widgets = []

        self.tabHeads = QHBoxLayout()
        self.pivot = SegmentedWidget(self)
        self.tabHeads.setSpacing(0)
        self.tabHeads.setContentsMargins(0, 0, 0, 0)
        self.tabHeads.addWidget(self.pivot, 0)
        self.tabHeads.addStretch()

        self.stackedWidget = QStackedWidget(self)
        # self.stackedWidget.set
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)
        self.setLayout(self.vBoxLayout)

        self.vBoxLayout.addLayout(self.tabHeads, 0)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def setTab(self, index):
        self.stackedWidget.setCurrentWidget(self.widgets[index])
        self.pivot.setCurrentItem(self.widgets[index].objectName())

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )
        self.widgets.append(widget)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

