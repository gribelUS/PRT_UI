from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ActivityLogView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Activity Log")
        label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(label)
        self.setLayout(layout)