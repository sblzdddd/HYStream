import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.last_folder = "./"

    def initUI(self):
        self.setWindowTitle("Folder Select Dialog Example")
        self.setGeometry(100, 100, 400, 200)

        button = QPushButton("Select Folder", self)
        button.clicked.connect(self.openFolderDialog)
        button.setGeometry(150, 80, 100, 30)

    def openFolderDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", self.last_folder)
        if folder_path:
            self.last_folder = folder_path
            print("Selected Folder:", folder_path)
            return folder_path
        return None

    def openFileDialog(self, filter, filter_name):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter(filter)
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setDirectory(self.last_folder)  # Set initial directory here if needed
        file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        selected_files, _ = file_dialog.getOpenFileNames(self, f"Select {filter_name} Files", "", filter)
        if selected_files:
            self.last_folder = os.path.dirname(selected_files[0])
            return selected_files
        return None
