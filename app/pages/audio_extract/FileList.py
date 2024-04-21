import os

from PyQt5.QtCore import Qt, pyqtSignal

from app.components.view.AssetsTable import AssetsTable, disableEdit, SizeItem
from app.module import format_bytes
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QHeaderView as QH, QTableWidgetItem


class FileList(AssetsTable):
    onFileOpened = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.files = []
        self.setColumnCount(3)
        self.itemDoubleClicked.connect(self.onFileOpen)
        self.setHorizontalHeaderLabels(['Name', 'Items', 'Size'])
        self.setResizeMode([QH.Stretch, QH.ResizeToContents, QH.ResizeToContents])

    def create_list(self, files, length):
        if files:
            self.files = files
            self.setRowCount(len(files))
            for i, file in enumerate(files):
                name_item = QTableWidgetItem(os.path.basename(file).rstrip(".pck"))
                name_item.setIcon(FIF.MUSIC_FOLDER.icon())
                disableEdit(name_item)
                self.setItem(i, 0, name_item)

                file_count = int(length[i])
                count_item = QTableWidgetItem()
                count_item.setData(0, file_count)
                disableEdit(count_item)
                self.setItem(i, 1, count_item)

                file_size = os.path.getsize(file)
                size_item = SizeItem(format_bytes(file_size))
                size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                disableEdit(size_item)
                self.setItem(i, 2, size_item)

        self.setHorizontalHeaderLabels(['Name', 'Items', 'Size'])

    def onFileOpen(self, item):
        index = self.row(item)
        file_name = self.item(index, 0).text()
        index, path = self.getRealIndexInFileList(file_name)
        self.onFileOpened.emit(path)

    def getRealIndexInFileList(self, name):
        for index, file in enumerate(self.files):
            if os.path.basename(file).rstrip(".pck") == name:
                return index, file

    def reset(self):
        self.clearSelection()
        self.setRowCount(0)
