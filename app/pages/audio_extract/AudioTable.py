from enum import Enum

from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtGui import QColor, QPainter, QCursor

from app.components.view.AssetItemDelegate import AssetItemDelegate
from app.components.view.AssetsTable import AssetsTable, disableEdit, SizeItem
from PyQt5.QtWidgets import QHeaderView as QH, QTableWidgetItem, QStyleOptionViewItem
from qfluentwidgets import FluentIcon as FIF, TableItemDelegate, isDarkTheme, themeColor, RoundMenu, Action

from app.module import format_bytes, format_duration

class ATState(Enum):
    IDLE = 0
    UPDATING = 1


class AudioTable(AssetsTable):
    def __init__(self, parent, playAudio, setAlias):
        super().__init__(parent)
        self.delegate = AssetItemDelegate(self)
        self.setItemDelegate(self.delegate)
        self.parent_ = parent
        self.itemDoubleClicked.connect(self.playAudio)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Title', 'Alias', 'Duration', 'Size'])
        self.setResizeMode([QH.ResizeToContents, QH.Stretch, QH.ResizeToContents, QH.ResizeToContents])
        self.cellChanged.connect(self.audioCellChanged)
        self.state: ATState = ATState.IDLE
        self.playAudioCallback = playAudio
        self.setAliasCallback = setAlias
        self.currentPlaying = None

    def create_list(self, files):
        self.state = ATState.UPDATING
        self.setRowCount(0)
        self.clearSelection()
        self.setRowCount(len(files))
        for i, info in enumerate(files):
            name_item = QTableWidgetItem(info.get_file_name())
            name_item.setIcon(FIF.MUSIC.icon())
            disableEdit(name_item)
            self.setItem(i, 0, name_item)

            alias_item = QTableWidgetItem(info.alias)
            self.setItem(i, 1, alias_item)

            self.updateDuration(info.get_file_name(), info.duration)

            size = format_bytes(info.size)
            size_item = SizeItem(size)
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            disableEdit(size_item)
            self.setItem(i, 3, size_item)

        self.state = ATState.IDLE

    def updateDuration(self, name, duration):
        d = ""
        if duration != 0:
            d = format_duration(duration)
        duration_item = QTableWidgetItem(d)
        duration_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        disableEdit(duration_item)
        index = self.getRelativePositionByName(name)
        if index is not None:
            self.setItem(index, 2, duration_item)
            if self.currentPlaying == name:
                self.setHighlight(index, True)

    def getRelativePositionByName(self, name):
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item is not None and item.text() == name:
                return row
        return None

    def getRealIndexByName(self, name):
        return int(name.split("_")[1].split(".")[0])

    def playAudio(self, item):
        self.state = ATState.UPDATING
        # Get the index of the clicked item
        real_index = self.row(item)

        # update highlights
        if self.currentPlaying:
            last_index = self.getRelativePositionByName(self.currentPlaying)
            self.setHighlight(last_index, False)
            self.reset()
        self.setHighlight(real_index, True)

        file_name = self.item(real_index, 0).text()

        self.currentPlaying = file_name
        index = self.getRealIndexByName(file_name)
        self.playAudioCallback(index, real_index)
        self.state = ATState.IDLE

    def setHighlight(self, row, isHighlighted):
        for col in range(self.columnCount()):
            if isHighlighted:
                self.item(row, col).setData(Qt.BackgroundRole, themeColor())
                self.item(row, col).setSelected(True)
            else:
                self.item(row, col).setData(Qt.BackgroundRole, QVariant())

    def audioCellChanged(self, row, col):
        if col == 1 and self.state != ATState.UPDATING:
            file_name = self.item(row, 0).text()
            index = self.getRealIndexByName(file_name)
            name = self.item(row, 1).text()
            self.setAliasCallback(index, name)

    def table_reset(self):
        self.state: ATState = ATState.IDLE
        self.currentPlaying = None
        self.clearSelection()
        self.setRowCount(0)

    def generateMenu(self):
        if len(self.selectedRows()) == 0:
            return
        cursor = QCursor()
        pos = cursor.pos()
        print("Right Click on", pos)

        contextMenu = RoundMenu("Actions", self)

        # Add actions in batches
        contextMenu.addActions([
            Action(FIF.SAVE_AS, 'Export Selected', triggered=lambda: print(self.selectedRows())),
        ])

        # Add a separator
        contextMenu.addSeparator()

        contextMenu.addActions([
            Action(FIF.CHECKBOX, 'Select All', shortcut='Ctrl+A', triggered=lambda: self.selectAll()),
            Action(FIF.REMOVE_FROM, 'Select None', shortcut='Ctrl+N',
                   triggered=lambda: self.clearSelection())
        ])
        contextMenu.exec_(pos)
