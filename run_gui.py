from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

# This script is the entry point for the GUI application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())