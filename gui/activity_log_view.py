from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QDateTimeEdit, QPushButton
)
from PyQt5.QtCore import QDateTime


class ActivityLogView(QWidget):
    def __init__(self, db_conn):
        super().__init__()
        self.conn = db_conn
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filters
        filter_layout = QHBoxLayout()

        self.cart_filter = QComboBox()
        self.cart_filter.addItem("All", None)
        for cart in ["C1", "C2", "C3", "C4"]:
            self.cart_filter.addItem(cart, cart)

        self.station_filter = QComboBox()
        self.station_filter.addItem("All", None)
        for station in [
            "Station_1", "Station_2", "Station_3", "Station_4",
            "Segment_A", "Segment_B", "Segment_C", "Segment_D",
            "Segment_E", "Segment_F"
        ]:
            self.station_filter.addItem(station, station)

        self.time_filter = QDateTimeEdit()
        self.time_filter.setCalendarPopup(True)
        self.time_filter.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.time_filter.setDateTime(QDateTime.currentDateTime().addDays(-1))

        self.filter_btn = QPushButton("Filter")
        self.filter_btn.clicked.connect(self.load_logs)

        filter_layout.addWidget(QLabel("Cart:"))
        filter_layout.addWidget(self.cart_filter)
        filter_layout.addWidget(QLabel("Position:"))
        filter_layout.addWidget(self.station_filter)
        filter_layout.addWidget(QLabel("Since:"))
        filter_layout.addWidget(self.time_filter)
        filter_layout.addWidget(self.filter_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Cart ID", "Position", "Event", "Time"])

        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_logs()

    def load_logs(self):
        cart_id = self.cart_filter.currentData()
        position = self.station_filter.currentData()
        time_stamp = self.time_filter.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        query = """
            SELECT cart_id, position, event_type, time_stamp
            FROM cart_logs
            WHERE (%s IS NULL OR cart_id = %s)
              AND (%s IS NULL OR position = %s)
              AND (%s IS NULL OR time_stamp >= %s)
            ORDER BY time_stamp DESC
        """
        params = (cart_id, cart_id, position, position, time_stamp, time_stamp)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            rows = []

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
