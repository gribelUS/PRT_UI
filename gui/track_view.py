from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, pyqtSignal

class TrackView(QWidget):
    cart_clicked = pyqtSignal(str)  # Signal to emit when a cart is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #fffbe6; border: 2px dashed red;")

        self.selected_cart_id = None  # Tracks the selected cart
        self.cart_radius = 15
        self.carts = [  # Example carts
            {"id": "C1", "x": 200, "status": "Moving"},
            {"id": "C2", "x": 400, "status": "Idle"},
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#fffbe6"))

        margin = 40
        outer_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        track_thickness = 40
        radius = 60

        # Draw outer track
        painter.setBrush(QColor("#002855"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(outer_rect, radius, radius)

        # Hollow center
        inner_rect = outer_rect.adjusted(track_thickness, track_thickness, -track_thickness, -track_thickness)
        painter.setBrush(QColor("#fffbe6"))
        painter.drawRoundedRect(inner_rect, radius, radius)

        # Draw stations
        station_w = 40
        num_slots = 10
        slot_margin = 4

        spacing = (outer_rect.width() - 4 * station_w) // 5
        x_start = outer_rect.left() + spacing
        track_top = outer_rect.top()
        station_h = outer_rect.height() - 2 * track_thickness
        slot_h = station_h // num_slots

        painter.setPen(QPen(QColor("#002855"), 1))

        for i in range(4):
            x = x_start + i * (station_w + spacing)
            y = track_top + track_thickness
            painter.setBrush(QColor("#ffc600"))
            painter.drawRect(x, y, station_w, station_h)

            # Draw 10 cart slots
            painter.setBrush(QColor("#0077cc"))
            for j in range(num_slots):
                slot_y = y + j * slot_h + slot_margin // 2
                painter.drawRect(x + 5, slot_y, station_w - 10, slot_h - slot_margin)

            # Direction indicators
            painter.setBrush(Qt.red)
            if i % 2 == 0:
                painter.drawEllipse(x + station_w // 2 - 4, y - 8, 8, 8)
            else:
                painter.drawEllipse(x + station_w // 2 - 4, y + station_h, 8, 8)

        # Draw carts
        for cart in self.carts:
            cart_x = cart["x"]
            cart_y = outer_rect.top() + track_thickness // 2
            cart["y"] = cart_y  # for click detection

            if cart.get("id") == self.selected_cart_id:
                painter.setBrush(QColor("#FFD700"))  # Highlight
            else:
                painter.setBrush(QColor("#EAAA00"))

            painter.drawEllipse(cart_x - self.cart_radius, cart_y - self.cart_radius,
                                self.cart_radius * 2, self.cart_radius * 2)

    def mousePressEvent(self, event):
        clicked_x = event.x()
        clicked_y = event.y()

        for cart in self.carts:
            dx = clicked_x - cart["x"]
            dy = clicked_y - cart["y"]
            if dx ** 2 + dy ** 2 <= self.cart_radius ** 2:
                self.selected_cart_id = cart["id"]
                self.cart_clicked.emit(cart["id"])
                self.update()
                break
