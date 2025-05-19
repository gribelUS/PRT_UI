from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from models.db import get_connection
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        db_conn = get_connection()

        window = MainWindow(db_conn)  # Pass it in
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        import traceback
        traceback.print_exc()
