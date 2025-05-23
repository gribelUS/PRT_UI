from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QDateTimeEdit, QPushButton, QHeaderView
)
from PyQt5.QtCore import QDateTime, Qt
from models.db import fetch_filtered_logs, fetch_all_cart_ids

class ActivityLogView(QWidget):
    def __init__(self, db_conn):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f2f2f2;")
        main_layout = QHBoxLayout()

        # Table container
        table_container = QWidget()
        table_container.setStyleSheet("background-color: white; padding: 10px; border-radius: 8px;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Cart ID", "Position", "Event", "Time"])
        self.table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    alternate-background-color: #f9f9f9;
                    gridline-color: #ddd;
                    font-size: 12pt;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 4px;
                    font-weight: bold;
                    border: 1px solid #ddd;
                }
            """)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_layout.addWidget(self.table)

        # Sidebar: Filter panel on the right

        filter_panel = QWidget()
        filter_panel.setStyleSheet("background-color: white; padding: 10px; border-radius: 8px; border: 1px solid #ddd;")
        filter_layout = QVBoxLayout(filter_panel)

        # Cart filter
        filter_layout.addWidget(QLabel("Cart ID:"))
        self.cart_filter = QComboBox()
        self.cart_filter.addItem("All", None)
        for cart_id in fetch_all_cart_ids():
            self.cart_filter.addItem(cart_id, cart_id)
        filter_layout.addWidget(self.cart_filter)

        # Station filter
        filter_layout.addWidget(QLabel("Position:"))
        self.station_filter = QComboBox()
        self.station_filter.addItem("All", None)
        for station in [
            "Station_1", "Station_2", "Station_3", "Station_4",
            "Segment_A", "Segment_B", "Segment_C", "Segment_D",
            "Segment_E", "Segment_F"
        ]:
            self.station_filter.addItem(station, station)
        filter_layout.addWidget(self.station_filter)

        # Time filter
        filter_layout.addWidget(QLabel("Since:"))
        self.time_filter = QDateTimeEdit()
        self.time_filter.setCalendarPopup(True)
        self.time_filter.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.time_filter.setDateTime(QDateTime.currentDateTime().addDays(-1))
        filter_layout.addWidget(self.time_filter)

        # Buttons
        self.filter_btn = QPushButton("Filter")
        self.filter_btn.clicked.connect(self.load_logs)
        filter_layout.addWidget(self.filter_btn)

        self.clear_btn = QPushButton("Clear Filters")
        self.clear_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.clear_btn)

        filter_layout.addStretch()

        # Add to main layout
        main_layout.addWidget(table_container, 3)
        main_layout.addWidget(filter_panel, 1)

        self.setLayout(main_layout)
        self.load_logs()
        
    def load_logs(self):
        cart_id = self.cart_filter.currentData()
        position = self.station_filter.currentData()
        time_stamp = self.time_filter.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        logs = fetch_filtered_logs(cart_id, position, time_stamp)

        self.table.setRowCount(len(logs))
        for i, row in enumerate(logs):
            self.table.setItem(i, 0, QTableWidgetItem(row["cart_id"]))
            self.table.setItem(i, 1, QTableWidgetItem(row["position"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["event_type"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["time_stamp"].strftime("%Y-%m-%d %H:%M:%S")))    

            if row["event_type"] == "diverted":
                for col in range(4):
                    item = self.table.item(i, col)
                    item.setBackground(Qt.red)
                    item.setForeground(Qt.white)

    def clear_filters(self):
        self.cart_filter.setCurrentIndex(0)
        self.station_filter.setCurrentIndex(0)
        self.time_filter.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.load_logs()