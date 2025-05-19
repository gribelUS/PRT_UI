from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QTimer


class TrackView(QWidget):
    cart_selected = pyqtSignal(str)  # Signal to emit when a cart is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #fffbe6; border: 2px dashed red;")

        self.selected_cart_id = None
        self.cart_radius = 15
        self.cart_y = 0  # Y position will be calculated after resize
        self.carts = []

        # Setup timer to simulate or process cart movement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cart_positions)
        self.timer.start(100)  # Adjust this interval (ms) for smoothness

        # Example initial carts (can be overwritten with set_carts)
        self.set_carts([
            {"id": "C1", "x": 200, "status": "Moving"},
            {"id": "C2", "x": 400, "status": "Idle"},
        ])

    def set_carts(self, carts):
        """External method to update cart list."""
        self.carts = carts
        self.update()

    def update_cart_positions(self):
        """Move carts with status == 'Moving'."""
        for cart in self.carts:
            if cart.get("status") == "Moving":
                cart["x"] += 2  # Adjust speed here
                # Wrap around logic for demo; adjust if needed
                if cart["x"] > self.width() - 50:
                    cart["x"] = 50
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#fffbe6"))

        # Track design
        margin = 40
        outer_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        track_thickness = 40
        radius = 60

        # Outer blue track
        painter.setBrush(QColor("#002855"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(outer_rect, radius, radius)

        # Inner hollow center
        inner_rect = outer_rect.adjusted(track_thickness, track_thickness, -track_thickness, -track_thickness)
        painter.setBrush(QColor("#fffbe6"))
        painter.drawRoundedRect(inner_rect, radius, radius)

        # Stations and slots
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

            # 10 slots
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
        self.cart_y = outer_rect.top() + track_thickness // 2
        for cart in self.carts:
            cart_x = cart.get("x", 0)
            cart["y"] = self.cart_y  # store for click detection

            # Highlight if selected
            if cart.get("id") == self.selected_cart_id:
                painter.setBrush(QColor("#FFD700"))
            else:
                painter.setBrush(QColor("#EAAA00"))

            painter.drawEllipse(cart_x - self.cart_radius, self.cart_y - self.cart_radius,
                                self.cart_radius * 2, self.cart_radius * 2)

            # Draw cart ID above
            painter.setPen(Qt.black)
            painter.drawText(cart_x - 15, self.cart_y - 20, cart["id"])

    def mousePressEvent(self, event):
        clicked_x = event.x()
        clicked_y = event.y()

        for cart in self.carts:
            dx = clicked_x - cart["x"]
            dy = clicked_y - cart["y"]
            if dx ** 2 + dy ** 2 <= self.cart_radius ** 2:
                self.selected_cart_id = cart["id"]
                self.cart_selected.emit(cart["id"])
                self.update()
                break
