from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QStyle
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ProgressBar, IndeterminateProgressBar
from app.module import clear_layout


class LoadingDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, title="Loading"):
        super().__init__(parent)

        self.logs = []
        self.total = 0
        self.progress = 0

        self.hideYesButton()
        self.buttonLayout.removeItem(self.buttonLayout.takeAt(0))
        self.hideCancelButton()
        self.buttonLayout.removeItem(self.buttonLayout.takeAt(0))

        self.titleLabel = SubtitleLabel(title, self)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setSpacing(10)

        self.progressLabel = QLabel("-/-")
        self.progressLabel.setObjectName("progressLabel")
        self.progressLabel.setStyleSheet('''
            #progressLabel {
                font: 12px 'Segoe UI SemiBold', 'Microsoft YaHei SemiBold';
            }
        ''')

        self.progressBar = ProgressBar(self)
        self.inProgressBar = IndeterminateProgressBar(self)
        self.progressBar.setValue(0)

        self.hBoxLayout.addWidget(self.inProgressBar)

        self.hBoxLayout.setContentsMargins(5, 0, 5, 0)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.viewLayout.addLayout(self.hBoxLayout)
        self.viewLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.widget.setMinimumWidth(600)
        self.widget.setMaximumWidth(800)

        self.buttonLayout.setContentsMargins(30, 0, 30, 0)
        self.buttonLayout.setAlignment(Qt.AlignCenter)
        self.logLabel = QLabel("")
        self.logLabel.setObjectName("logLabel")
        self.logLabel.setStyleSheet('''
            #logLabel {
                font: 10px 'Courier New', 'Microsoft YaHei SemiBold';
                color: #00ff64;
            }
        ''')
        self.logLabel.setAlignment(Qt.AlignLeft)
        self.buttonLayout.addWidget(self.logLabel, 0, alignment=Qt.AlignLeft)
        # self.buttonLayout.insertStretch(-1, 1)
        # self.buttonLayout.insertStretch(-2, 1)

        # self.hideYesButton()

    def setTotalValue(self, value):
        self.total = value
        clear_layout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.progressLabel)
        self.progressLabel.setText(f"{0}/{self.total}")
        self.hBoxLayout.addWidget(self.progressBar)
        self.progressBar.setValue(0)

    def updateValue(self, value: int):
        self.progress = int(value / self.total * 100)
        self.progressBar.setValue(self.progress)
        self.progressLabel.setText(f"{value}/{self.total}")

    def log(self, content):
        self.logs.append(str(content))
        if len(self.logs) > 3:
            self.logs = self.logs[-3:]
        self.updateLog()

    def updateLog(self):
        self.logLabel.setText("\n".join(self.logs))

    def setTitle(self, title):
        self.titleLabel.setText(title)
