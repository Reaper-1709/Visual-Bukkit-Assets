from PyQt5.QtGui import QPainterPath, QPainter, QBrush, QColor, QRegion, QGuiApplication, QTransform, QLinearGradient
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys

from app.views.dock import Dock
# Import your grid view from a separate module.
from main_grid import MainGrid


class MainWindow(QMainWindow):
    MARGIN = 10

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        win_x = (screen.width() - self.width()) // 2
        win_y = (screen.height() - self.height()) // 2
        self.setGeometry(win_x, win_y, self.width(), self.height())

    def __init__(self):
        super().__init__()
        self.mouse_pos = None
        self.setWindowTitle("Visual Bukkit Manager")
        self.setGeometry(0, 0, 1200, 800)
        self.center_window()
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.dragging = False
        self.resizing = False
        self.edge = None
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.radius = 24  # Corner radius for white background
        self.setMouseTracking(True)

        # --- Title Bar, Wave, and Control Buttons (remain part of MainWindow) ---

        # Title bar covering the top area (e.g. 140px tall)
        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, self.width(), 140)
        self.title_bar.setStyleSheet("background: transparent;")
        self.title_bar.setMouseTracking(True)

        # Title label: centered text; adjust vertical position (here, y=90)
        self.title_label = QLabel("Visual Bukkit Manager", self.title_bar)
        self.title_label.setGeometry(0, 90, self.width(), 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "color: white; font-size: 32px; font-family: Lucida Console, Lucida Sans Typewriter, monospace; font-weight: bold;"
        )
        self.title_label.setMouseTracking(True)

        # Control buttons container (minimize, maximize, close)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(5)
        self.btn_min = QPushButton(" ")
        self.btn_max = QPushButton(" ")
        self.btn_close = QPushButton(" ")
        for btn, color in zip((self.btn_min, self.btn_max, self.btn_close), ("green", "yellow", "red")):
            btn.setFixedSize(20, 20)
            btn.setStyleSheet(f"background: {color}; border-radius: 10px;")
            btn_layout.addWidget(btn)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.toggle_maximize)
        self.btn_close.clicked.connect(self.close)
        self.buttons_widget = QWidget(self.title_bar)
        self.buttons_widget.setLayout(btn_layout)
        # Position the buttons widget with a right margin of 20 and top margin of 20
        self.buttons_widget.setGeometry(self.width() - 110, 20, 90, 30)
        self.buttons_widget.setStyleSheet("background: #333; border-radius: 7px;")
        self.buttons_widget.setMouseTracking(True)

        # --- Embedded Main Grid View ---
        # Create an instance of the MainGrid view (defined in main_grid.py)
        self.main_grid = MainGrid(self)
        # Place it below the title bar, filling the rest with the window.
        self.main_grid.setGeometry(0, 140, self.width(), self.height() - 140)
        self.main_grid.setMouseTracking(True)

        # --- Embedded Dock View ---
        # Create an instance of the Dock view (defined in dock.py)
        self.dock = Dock(self)
        self.dock.setGeometry(0, self.height() - 75, self.width(), 75)
        self.dock.setMouseTracking(True)


    @staticmethod
    def create_wave_path(height):
        """
        Converts the provided SVG path into a QPainterPath.
        (Original SVG viewBox: 0 0 1440 320)
        """
        path = QPainterPath()
        y_offset = height // 8  # Adjust vertical position of the wave
        path.moveTo(0, 160 + y_offset)  # M0,160
        path.lineTo(34.3, 176 + y_offset)  # L34.3,176
        # Cubic Bezier Curves (C)
        path.cubicTo(68.6, 192 + y_offset, 137, 224 + y_offset, 206, 240 + y_offset)
        path.cubicTo(274.3, 256 + y_offset, 343, 256 + y_offset, 411, 240 + y_offset)
        path.cubicTo(480, 224 + y_offset, 549, 192 + y_offset, 617, 192 + y_offset)
        path.cubicTo(685.7, 192 + y_offset, 754, 224 + y_offset, 823, 218.7 + y_offset)
        path.cubicTo(891.4, 213 + y_offset, 960, 171 + y_offset, 1029, 133.3 + y_offset)
        path.cubicTo(1097.1, 96 + y_offset, 1166, 64 + y_offset, 1234, 80 + y_offset)
        path.cubicTo(1302.9, 96 + y_offset, 1371, 160 + y_offset, 1406, 192 + y_offset)
        path.lineTo(1440, 224 + y_offset)  # L1440,224
        # Close the shape (covering the top part)
        path.lineTo(1440, 0)  # Top-right
        path.lineTo(0, 0)  # Top-left
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Draw the main window background (white rounded rectangle).
        bg_path = QPainterPath()
        bg_path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(Qt.NoPen)
        painter.drawPath(bg_path)
        # Apply mask for rounded corners.
        mask = QRegion(bg_path.toFillPolygon().toPolygon())
        self.setMask(mask)

        # 2. Draw the wave shape in the title bar area.
        wave_path = self.create_wave_path(self.height())
        scale_x = self.width() / 1440
        scale_y = self.title_bar.height() / 320
        transform = QTransform()
        transform.scale(scale_x, scale_y)
        wave_path = transform.map(wave_path)
        gradient = QLinearGradient(0, 0, self.width(), self.title_bar.height())
        gradient.setColorAt(0, QColor(14, 165, 233))
        gradient.setColorAt(0.50, QColor(240, 171, 252))
        gradient.setColorAt(1, QColor(240, 171, 252))
        painter.setBrush(QBrush(gradient))
        painter.drawPath(wave_path)

    def resizeEvent(self, event):
        self.title_bar.setGeometry(0, 0, self.width(), 140)
        self.title_label.setGeometry(0, ((self.height() // 8) - 30) // 2, self.width(), 40)  # y_offset -30 // 2
        self.buttons_widget.setGeometry(self.width() - 110, 20, 90, 30)
        # Update the main grid view to fill the area below the title bar.
        self.main_grid.setGeometry(0, 140, self.width(), self.height() - 140)
        # Update the dock view to fill the bottom area.
        self.dock.setGeometry(0, self.height() - 75, self.width(), 75)
        self.update()
        super().resizeEvent(event)

    def toggle_maximize(self):
        self.showNormal() if self.isMaximized() else self.showMaximized()

    # (Mouse event code for dragging/resizing omitted for brevity—keep your existing implementation.)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos = event.globalPos()
            if self.title_bar.geometry().contains(event.pos()):
                self.dragging = True
                self.resizing = False
                self.edge = None
                self.setCursor(Qt.ClosedHandCursor)
            elif self.buttons_widget.geometry().contains(event.pos()):
                self.dragging = False
                self.resizing = False
                self.edge = None
                self.setCursor(Qt.ArrowCursor)
            else:
                self.edge = self.get_edge(event.pos())
                if self.edge:
                    self.resizing = True
                else:
                    self.dragging = False
                    self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.isMaximized():
            if self.resizing and self.mouse_pos:
                self.resize_window(event.globalPos())
                self.mouse_pos = event.globalPos()
            elif self.dragging and self.mouse_pos:
                delta = event.globalPos() - self.mouse_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.mouse_pos = event.globalPos()
            else:
                if self.buttons_widget.geometry().contains(event.pos()):
                    self.setCursor(Qt.ArrowCursor)
                elif not self.title_bar.geometry().contains(event.pos()):
                    self.update_cursor(event.pos())
                else:
                    self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False
        self.edge = None
        if self.title_bar.geometry().contains(event.pos()) and not self.isMaximized():
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def get_edge(self, pos):
        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        if x < self.MARGIN:
            if y < self.MARGIN:
                return "top-left"
            elif y > h - self.MARGIN:
                return "bottom-left"
            return "left"
        if x > w - self.MARGIN:
            if y < self.MARGIN:
                return "top-right"
            elif y > h - self.MARGIN:
                return "bottom-right"
            return "right"
        if y > h - self.MARGIN:
            return "bottom"
        if y < self.MARGIN:
            return "top"
        return None

    def update_cursor(self, pos):
        edge = self.get_edge(pos)
        if edge == "bottom-right":
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge == "bottom-left":
            self.setCursor(Qt.SizeBDiagCursor)
        elif edge in ("left", "right"):
            self.setCursor(Qt.SizeHorCursor)
        elif edge == "bottom":
            self.setCursor(Qt.SizeVerCursor)
        elif edge in ("top-left", "top", "top-right"):
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def resize_window(self, global_pos):
        delta = global_pos - self.mouse_pos
        x, y, w, h = self.geometry().getRect()
        if self.edge == "bottom-left":
            self.setGeometry(x + delta.x(), y, w - delta.x(), h + delta.y())
        elif self.edge == "bottom-right":
            self.setGeometry(x, y, w + delta.x(), h + delta.y())
        elif self.edge == "bottom":
            self.setGeometry(x, y, w, h + delta.y())
        elif self.edge == "left":
            self.setGeometry(x + delta.x(), y, w - delta.x(), h)
        elif self.edge == "right":
            self.setGeometry(x, y, w + delta.x(), h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
