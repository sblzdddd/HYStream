from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from qfluentwidgets import TableWidget, ListWidget, themeColor


class DraggableWidget(TableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.dragging = False
        self.startPos = None
        self.endPos = None
        self.scrollY = 0
        self.offsetScrollY = 0
        self.verticalScrollBar().valueChanged.connect(self.updateScrollY)

    def updateScrollY(self, value):
        self.scrollY = value

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.offsetScrollY = self.verticalScrollBar().value()
        self.dragging = True
        self.startPos = event.pos()
        self.prevScrollBarValue = self.verticalScrollBar().value()
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.dragging:
            self.endPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.dragging = False
        self.startPos = None
        self.endPos = None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.dragging and self.startPos and self.endPos:
            painter = QPainter(self.viewport())
            theme = themeColor()
            colorFill = QColor(theme.red(), theme.green(), theme.blue(), 100)
            colorStroke = QColor(theme.red(), theme.green(), theme.blue(), 200)
            stroke = QPen(colorStroke)
            stroke.setWidth(2)
            painter.setPen(stroke)
            painter.setBrush(QBrush(colorFill))
            startPos = QPoint(self.startPos.x(), self.startPos.y())
            startPos.setY(self.startPos.y() - self.scrollY + self.offsetScrollY)
            rect = QRect(startPos, self.endPos).normalized()
            painter.drawRect(rect)
            self.updateSelectedRows()
