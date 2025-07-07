from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QComboBox
from gui.track_view import TrackView
from models.db import get_cart_info
from models.api import send_cart_to_station

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Outer vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title label
        label = QLabel("Live map & Control Panel")
        label.setStyleSheet("font-size: 25px; color: #002855; font-weight: bold; color: white;")
        main_layout.addWidget(label)

        # Horizontal layout for map and panel
        h_layout = QHBoxLayout()
        h_layout.setSpacing(20)

        # Live Track Map
        self.track_view = TrackView()
        self.track_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.track_view.cart_selected.connect(self.display_cart_info)

        # Side panel for cart info
        self.panel_frame = QFrame()
        self.panel_frame.setMinimumSize(300, 400)
        self.panel_frame.setStyleSheet("background-color: #EAAA00; border: 2px solid #002855;")

        self.info_label = QLabel("Select a cart to view details.")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("padding: 10px; font-size: 25px; color: white;")

        panel_layout = QVBoxLayout()
        info_title = QLabel("<b>Cart Information</b>")
        info_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        panel_layout.addWidget(info_title)
        panel_layout.addWidget(self.info_label)

        # Dropdown for stations
        self.station_dropdown = QComboBox()
        self.station_dropdown.addItems(["Station 1", "Station 2", "Station 3", "Station 4"])
        self.station_dropdown.setEnabled(False)
        self.station_dropdown.setStyleSheet("QComboBox:enabled { background-color: white; color: #002855; } QComboBox:disabled { background-color: #f5e6b5; color: #888; }")
        panel_layout.addWidget(self.station_dropdown)

        # Send button
        self.send_button = QPushButton("Send Cart to Station")
        self.send_button.setEnabled(False)
        self.send_button.setStyleSheet("QPushButton:enabled { background-color: white; color: #002855; } QPushButton:disabled { background-color: #f5e6b5; color: #888; }")
        panel_layout.addWidget(self.send_button)

        # Remove active cart button
        self.remove_button = QPushButton("Remove Active Cart")
        self.remove_button.setEnabled(False)
        self.remove_button.setStyleSheet("QPushButton:enabled { background-color: white; color: #002855; } QPushButton:disabled { background-color: #f5e6b5; color: #888; }")
        panel_layout.addWidget(self.remove_button)

        panel_layout.addStretch()
        self.panel_frame.setLayout(panel_layout)

        h_layout.addWidget(self.track_view, 3)
        h_layout.addWidget(self.panel_frame, 2)

        main_layout.addLayout(h_layout)
        self.setLayout(main_layout)

        self.send_button.clicked.connect(self.send_cart_to_station_clicked)
        # self.remove_button.clicked.connect(self.remove_active_cart_clicked) # Uncomment when implemented

    def display_cart_info(self, cart_id):
        data = get_cart_info(cart_id)
        if data:
            self.info_label.setText(
                f"<b>Cart ID:</b> {data['cart_id']}<br>"
                f"<b>Status:</b> {data.get('event_type', 'N/A')}<br>"
                f"<b>Location:</b> {data.get('position', 'Unknown')}<br>"
                f"<b>Time:</b> {data['time_stamp']}"
            )
            self.station_dropdown.setEnabled(True)
            self.send_button.setEnabled(True)
        else:
            self.info_label.setText(f"Cart '{cart_id}' has no recent data.")
            self.station_dropdown.setEnabled(False)
            self.send_button.setEnabled(False)

    def send_cart_to_station_clicked(self):
        if not hasattr(self, 'track_view') or not self.track_view.selected_cart_id:
            return
        cart_id = self.track_view.selected_cart_id
        station_index = self.station_dropdown.currentIndex()
        station_id = f"Station_{station_index + 1}"
        send_cart_to_station(cart_id, station_id)
        self.info_label.setText(f"Sent cart {cart_id} to {station_id}.")
