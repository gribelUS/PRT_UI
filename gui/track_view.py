from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
import math

# Logical order of stops (segments and stations)
TRACK_NAMES = [
    "Segment_A", "Station_1", "Segment_B", "Station_2",
    "Segment_C", "Station_3", "Segment_D", "Station_4",
    "Segment_E", "Segment_F"
]

# These percent values determine where along the blue path each marker/carts/station goes.
# Tweak them as needed for your visual layout!
TRACK_POS_PERCENTS = [
    0.00,   # Segment_A (top left)
    0.047,   # Station_1
    0.1045,   # Segment_B
    0.661,   # Station_2
    0.265,   # Segment_C
    0.162,   # Station_3
    0.50,   # Segment_D
    0.548,   # Station_4
    0.6045,   # Segment_E
    0.765,   # Segment_F
]

class TrackView(QWidget):
    cart_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #fffbe6; border: 2px dashed red;")

        self.selected_cart_id = None
        self.cart_radius = 15
        self.carts = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cart_positions)
        self.timer.start(30)

        self.set_carts([
            {"id": "C1", "position": "Segment_A", "status": "Moving"},
            {"id": "C2", "position": "Segment_D", "status": "Idle"},
        ])

    def set_carts(self, carts):
        abs_pos = self.get_absolute_positions_for_carts()
        for cart in carts:
            pos_name = cart.get("position")
            target_xy = abs_pos.get(pos_name, (100, 100))
            if "x" not in cart or "y" not in cart:
                cart["x"], cart["y"] = target_xy
            cart["target_x"], cart["target_y"] = target_xy
        self.carts = carts
        self.update()

    def update_cart_positions(self):
        changed = False
        for cart in self.carts:
            x, y = cart.get("x", 0), cart.get("y", 0)
            target_x, target_y = cart.get("target_x", 0), cart.get("target_y", 0)
            if abs(x - target_x) > 1:
                step_x = 8 if x < target_x else -8
                if abs(target_x - x) < abs(step_x):
                    cart["x"] = target_x
                else:
                    cart["x"] += step_x
                changed = True
            else:
                cart["x"] = target_x

            if abs(y - target_y) > 1:
                step_y = 8 if y < target_y else -8
                if abs(target_y - y) < abs(step_y):
                    cart["y"] = target_y
                else:
                    cart["y"] += step_y
                changed = True
            else:
                cart["y"] = target_y
        if changed:
            self.update()

    def get_track_center_path(self):
        margin = 40
        track_thickness = 40
        radius = 60
        # For centerline: radius offset by half the thickness
        center_offset = margin + track_thickness // 2
        center_rect = self.rect().adjusted(center_offset, center_offset, -center_offset, -center_offset)
        center_radius = radius - track_thickness // 2

        x0, y0, w, h = center_rect.x(), center_rect.y(), center_rect.width(), center_rect.height()
        r = center_radius
        path = QPainterPath()
        path.moveTo(x0 + r, y0)
        path.lineTo(x0 + w - r, y0)
        path.arcTo(x0 + w - 2*r, y0, 2*r, 2*r, 90, -90)
        path.lineTo(x0 + w, y0 + h - r)
        path.arcTo(x0 + w - 2*r, y0 + h - 2*r, 2*r, 2*r, 0, -90)
        path.lineTo(x0 + r, y0 + h)
        path.arcTo(x0, y0 + h - 2*r, 2*r, 2*r, 270, -90)
        path.lineTo(x0, y0 + r)
        path.arcTo(x0, y0, 2*r, 2*r, 180, -90)
        path.closeSubpath()
        return path, center_rect

    def get_absolute_positions_for_carts(self):
        # Use pointAtPercent for precision
        path, _ = self.get_track_center_path()
        abs_pos = {}
        for name, percent in zip(TRACK_NAMES, TRACK_POS_PERCENTS):
            pt = path.pointAtPercent(percent)
            abs_pos[name] = (pt.x(), pt.y())
        return abs_pos

    def paintEvent(self, event):
        from PyQt5.QtCore import QPoint

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#fffbe6"))

        # Track shape parameters
        margin = 40
        track_thickness = 40
        radius = 60

        # Outer and inner rectangles for visual track shape
        outer_rect = self.rect().adjusted(margin, margin, -margin, -margin)
        inner_rect = outer_rect.adjusted(track_thickness, track_thickness, -track_thickness, -track_thickness)

        # Draw outer and inner tracks
        painter.setBrush(QColor("#002855"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(outer_rect, radius, radius)
        painter.setBrush(QColor("#fffbe6"))
        painter.drawRoundedRect(inner_rect, radius, radius)

        # Get centerline path and rect for blue path
        path, center_rect = self.get_track_center_path()

        # Draw blue path (centerline of the track)
        painter.setPen(QPen(QColor("#0077cc"), 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawPath(path)

        # Get exact positions for all segments/stations using the path
        abs_pos = self.get_absolute_positions_for_carts()

        # Get entrance marker x-coords for sorting left->right
        station_names = ["Station_1", "Station_2", "Station_3", "Station_4"]
        station_xs = [abs_pos[name][0] for name in station_names]
        sorted_pairs = sorted(zip(station_xs, station_names))
        sorted_stations = [name for _, name in sorted_pairs]

        # Evenly space stations horizontally inside inner_rect
        station_left = inner_rect.left()
        station_right = inner_rect.right()
        center_y = (inner_rect.top() + inner_rect.bottom()) // 2
        num_stations = len(station_names)
        even_xs = [
            int(station_left + (i + 1) * (station_right - station_left) / (num_stations + 1))
            for i in range(num_stations)
        ]
        station_centers = {
            name: (even_xs[i], center_y)
            for i, name in enumerate(sorted_stations)
        }

        # Draw station rectangles, entrance dots, dashed lines, and labels
        for i, name in enumerate(sorted_stations):
            x, y = station_centers[name]
            # Rectangle
            painter.setBrush(QColor("#ffc600"))
            painter.setPen(QPen(QColor("#002855"), 2))
            painter.drawRect(x - 20, center_y - 60, 40, 120)

            # Red entrance at the path
            ex, ey = abs_pos[name]
            painter.setBrush(Qt.red)
            painter.drawEllipse(int(ex) - 4, int(ey) - 4, 8, 8)

            # Dashed line from entrance to station
            painter.setPen(QPen(Qt.red, 2, Qt.DashLine))
            painter.drawLine(int(ex), int(ey), x, center_y - 60)

            # Station label
            painter.setPen(Qt.black)
            painter.drawText(x - 20, center_y - 70, f"Station {i+1}")

        # Draw segment markers (blue dots)
        segment_names = [n for n in TRACK_NAMES if "Segment" in n]
        for name in segment_names:
            x, y = abs_pos[name]
            painter.setBrush(QColor("#8888ff"))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawEllipse(int(x) - 10, int(y) - 10, 20, 20)
            painter.setPen(QPen(Qt.black, 2))
            painter.drawText(int(x) - 30, int(y) - 15, name.replace("_", " "))

        # Draw carts (on the path, at segment or station entrance positions)
        for cart in self.carts:
            pos_name = cart.get("position")
            if pos_name in abs_pos:
                cart_x, cart_y = abs_pos[pos_name]
                cart["x"], cart["y"] = cart_x, cart_y
            else:
                cart_x, cart_y = cart.get("x", 0), cart.get("y", 0)
            if cart.get("id") == self.selected_cart_id:
                painter.setBrush(QColor("#FFD700"))
            else:
                painter.setBrush(QColor("#EAAA00"))
            painter.setPen(Qt.black)
            painter.drawEllipse(int(cart_x) - self.cart_radius, int(cart_y) - self.cart_radius,
                                self.cart_radius * 2, self.cart_radius * 2)
            painter.drawText(int(cart_x) - 10, int(cart_y) + 30, cart["id"])

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
