# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QCompleter

from qfluentwidgets import LineEdit, PushButton, SearchLineEdit, setTheme, Theme


class ItemSearch(SearchLineEdit):

    def __init__(self, autocomplete=()):
        super().__init__()

        self.hBoxLayout = QHBoxLayout(self)

        # self.autocomplete = autocomplete
        # self.completer_ = QCompleter(self.autocomplete, self)
        # self.completer_.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer_.setMaxVisibleItems(45)
        # self.setCompleter(self.completer_)

        self.setClearButtonEnabled(True)
        self.setPlaceholderText('Search Item...')

