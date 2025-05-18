from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy, QStackedWidget
from gui.navbar import NavBar
from gui.home_view import HomeView
from gui.activity_log_view import ActivityLogView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRT Control Interface")
        self.setMinimumSize(1200, 700)

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) # No gap between navbar and content area

        # Add navbar and content area
        self.navbar = NavBar()
        self.navbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Page stack
        self.stack = QStackedWidget()
        self.home_view = HomeView()
        self.activity_view = ActivityLogView()
        self.stack.addWidget(self.home_view) # Index 0
        self.stack.addWidget(self.activity_view) # Index 1

        # Connect navbar buttons to routing
        self.navbar.dashboard_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.navbar.activity_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addWidget(self.navbar)
        layout.addWidget(self.stack)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Background color
        self.setStyleSheet("background-color: #002855;") # Set main window color to WVU blue