from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QSizePolicy, QHeaderView, QTableWidgetItem
from qfluentwidgets import TableWidget, TableItemDelegate, RoundMenu, Action

from app.components.view.DraggableWidget import DraggableWidget
from qfluentwidgets import FluentIcon as FIF


class SizeItem(QTableWidgetItem):
    def __init__(self, parent=None):
        QTableWidgetItem.__init__(self, parent)

    def __lt__(self, otherItem):
        try:
            return int(self.getSize()) < int(otherItem.getSize())
        except:
            return self.text() < otherItem.text()

    def getSize(self):
        unit_conversions = {'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4}  # Add more units if needed
        float_value = float(self.text()[:-2])  # Extract float part (exclude last two characters which are the unit)
        unit = self.text()[-2:]  # Extract the unit (last two characters)
        return float_value * unit_conversions[unit]


def disableEdit(item: QTableWidgetItem):
    item.setFlags(item.flags() ^ Qt.ItemIsEditable)


class AssetsTable(DraggableWidget, TableWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.initUI()

    def initUI(self):
        # Enable border and set rounded corners
        self.setBorderVisible(True)
        self.setBorderRadius(8)

        self.setWordWrap(False)
        self.setSortingEnabled(True)

        self.verticalHeader().hide()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSelectRightClickedRow(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.generateMenu)

    def setResizeMode(self, modes):
        header = self.horizontalHeader()
        for i, mode in enumerate(modes):
            header.setSectionResizeMode(i, mode)

    def selectedRows(self):
        selected = []
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item.isSelected():
                selected.append((row))
        return selected

    def invertSelection(self):
        selected = self.selectedRows()
        self.clearSelection()
        for row in range(self.rowCount()):
            if row not in selected:
                item = self.item(row, 0)
                item.setSelected(True)

        self.updateSelectedRows()

    def generateMenu(self):
        if len(self.selectedRows()) == 0:
            return
        cursor = QCursor()
        pos = cursor.pos()
        print("Right Click on", pos)

        contextMenu = RoundMenu("Actions", self)

        # Add actions in batches
        contextMenu.addActions([
            Action(FIF.SAVE_AS, 'Export Selected', triggered=lambda: print("Copy successful")),
        ])

        # Add a separator
        contextMenu.addSeparator()

        contextMenu.addActions([
            Action(FIF.CHECKBOX, 'Select All', shortcut='Ctrl+A', triggered=lambda: self.selectAll()),
            Action(FIF.REMOVE_FROM, 'Select None', shortcut='Ctrl+N',
                   triggered=lambda: self.clearSelection())
        ])
        contextMenu.exec_(pos)
