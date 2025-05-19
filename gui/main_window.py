from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSizePolicy, QStackedWidget, QMessageBox
)
from gui.navbar import NavBar
from gui.home_view import HomeView
from gui.activity_log_view import ActivityLogView 
from models.db import get_connection
import sys

class MainWindow(QMainWindow):
    def __init__(self, db_conn):
        super().__init__()
        self.db_conn = db_conn

        try:
            # Create navigation bar
            self.navbar = NavBar()
            self.navbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # Create views
            self.home_view = HomeView()
            self.activity_view = ActivityLogView(self.db_conn)

            # Page stack
            self.stack = QStackedWidget()
            self.stack.addWidget(self.home_view)
            self.stack.addWidget(self.activity_view)

            # Connect navbar buttons
            self.navbar.dashboard_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            self.navbar.activity_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

            # Create main layout
            central_widget = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(self.navbar)
            layout.addWidget(self.stack)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            # Set background color
            self.setStyleSheet("background-color: #002855;")

        except Exception as e:
            import traceback
            print("❌ Exception inside MainWindow setup:")
            traceback.print_exc()
            sys.exit(1)
