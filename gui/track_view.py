from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class TrackView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #fffbe6; border: 2px dashed red;")  # Light yellow background

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#fffbe6")) # Light yellow background

        margin = 40
        outer_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        track_thickness = 40 # Width of the conveyor track
        radius = 60

        # Draw outer track path (blue outline)
        painter.setBrush(QColor("#002855")) # Blue color for the track
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(outer_rect, radius, radius)

        # Draw inner track path to simulate hollow center
        inner_rect = outer_rect.adjusted(track_thickness, track_thickness, -track_thickness, -track_thickness)
        painter.setBrush(QColor("#fffbe6"))
        painter.drawRoundedRect(inner_rect, radius, radius)

        # Draw stations
        station_w = 40   # narrower width
        num_slots = 10
        slot_margin = 4

        spacing = (outer_rect.width() - 4 * station_w) // 5
        x_start = outer_rect.left() + spacing
        track_top = outer_rect.top()
        track_bottom = outer_rect.bottom()
        
        station_h = outer_rect.height() - 2 * track_thickness
        slot_h = station_h // num_slots

        painter.setPen(QPen(QColor("#002855"), 1))

        for i in range(4):
            x = x_start + i * (station_w + spacing)
            y = track_top + track_thickness
            painter.setBrush(QColor("#ffc600"))
            painter.drawRect(x, y, station_w, station_h)
            
            # Draw 10 cart slots inside the station
            painter.setBrush(QColor("#0077cc"))  # Placeholder color for cart slots
            for j in range(num_slots):
                slot_y = y + j * slot_h + slot_margin // 2
                painter.drawRect(x + 5, slot_y, station_w - 10, slot_h - slot_margin)

            # Show direction indicator
            painter.setBrush(Qt.red)
            if i % 2 == 0:
                painter.drawEllipse(x + station_w // 2 - 4, y - 8, 8, 8) # Top entry
            else:
                painter.drawEllipse(x + station_w // 2 - 4, y + station_h, 8, 8) # Bottom entry
 
        # Draw sample cart(s) inside the path
        painter.setBrush(QColor("#EAAA00"))
        cart_radius = 15

        cart_x = outer_rect.left() + 100
        cart_y = outer_rect.top() + (track_thickness // 2) # Inside the belt
        painter.drawEllipse(cart_x - cart_radius, cart_y - cart_radius, cart_radius * 2, cart_radius * 2)
