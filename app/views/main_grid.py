import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtProperty, QPropertyAnimation, QEasingCurve


class GridButton(QPushButton):
    def __init__(self, image_path, title, description, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 350)  # Fixed overall size
        self._bg_color = QColor("#F8F8F8")  # Default background color
        self.updateStyleSheet()

        # Setup background color animation
        self.color_anim = QPropertyAnimation(self, b"bgColor")
        self.color_anim.setDuration(300)
        self.color_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Remove default focus/outline if needed
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)

        # Internal layout for image, separator, title, and description.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)

        # --- Image Label ---
        image_label = QLabel(self)
        image_path = os.path.abspath(image_path)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        # Scale the image to fit without distorting the button dimensions.
        image_label.setPixmap(pixmap.scaled(334, 334, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # --- Separator Line ---
        separator = QWidget(self)
        separator.setStyleSheet("background-color: #CCC;")
        separator.setFixedHeight(3)  # A 3px tall line
        layout.addWidget(separator)

        # --- Title Label ---
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; color: black; font-weight: bold;")
        layout.addWidget(title_label)

        # --- Description Label ---
        desc_label = QLabel(description, self)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(desc_label)

        # Final button styling is applied via our updateStyleSheet() method.
        # (No additional padding here since layout margins are already defined.)

    def updateStyleSheet(self):
        # Update the button's style with the current background color.
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #CCC;
                background-color: {self._bg_color.name()};
                text-align: center;
                border-radius: 10px;
                padding: 10px;
            }}
        """)

    def getBgColor(self):
        return self._bg_color

    def setBgColor(self, color):
        if isinstance(color, QColor):
            self._bg_color = color
            self.updateStyleSheet()

    bgColor = pyqtProperty(QColor, fget=getBgColor, fset=setBgColor)

    def enterEvent(self, event):
        self.color_anim.stop()
        self.color_anim.setStartValue(self._bg_color)
        self.color_anim.setEndValue(QColor("#edd4fe"))  # Hover background color
        self.color_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.color_anim.stop()
        self.color_anim.setStartValue(self._bg_color)
        self.color_anim.setEndValue(QColor("#F8F8F8"))
        self.color_anim.start()
        super().leaveEvent(event)


class MainGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Create a grid layout to hold grid buttons.
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.layout.addLayout(self.grid_layout)

        # Define image paths. Adjust these relative paths as needed.
        assets_img = r"..\..\app\assets\icons\assets.png"
        themes_img = r"..\..\app\assets\icons\themes.png"
        plugins_img = r"..\..\app\assets\icons\plugins.png"

        # Create grid buttons.
        button1 = GridButton(assets_img, "Assets", "Manage your assets here", self)
        button2 = GridButton(themes_img, "Themes", "Select a theme for your project", self)
        button3 = GridButton(plugins_img, "Plugins", "Browse and install plugins", self)

        # Add buttons to the grid (one row, three columns).
        self.grid_layout.addWidget(button1, 0, 0)
        self.grid_layout.addWidget(button2, 0, 1)
        self.grid_layout.addWidget(button3, 0, 2)
