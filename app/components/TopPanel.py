from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QLabel


class TopPanel(QHBoxLayout):
    def __init__(self, title, parent=None):
        super().__init__()
        self.title_label = QLabel(title)
        self.initUI()
        
    def initUI(self):
        self.title_label.setObjectName('titleLabel')
        self.addWidget(self.title_label)
        self.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
    def add_widgets(self, widgets):
        for w in widgets:
            self.addWidget(w)
