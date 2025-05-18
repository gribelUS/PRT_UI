from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel, QSizePolicy
from gui.track_view import TrackView

class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Optional: Title label
        label = QLabel("Live map & Control Panel")
        label.setStyleSheet("font-size: 18px; color: #002855; font-weight: bold;")
        main_layout.addWidget(label)

        # Horizontal layout for map and panel
        h_layout = QHBoxLayout()
        h_layout.setSpacing(20)

        # Live Track Map
        self.map_frame = TrackView()

        # Control Panel
        self.panel_frame = QFrame()
        self.panel_frame.setMinimumSize(300, 400)
        self.panel_frame.setStyleSheet("background-color: #f0f0f0; border: 2px solid #002855;")
        
        h_layout.addWidget(self.map_frame, 3)
        h_layout.addWidget(self.panel_frame, 2)

        main_layout.addLayout(h_layout)
        self.setLayout(main_layout)