from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QColor


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # Fixed height so scaling doesn't distort button dimensions.
        self.setFixedHeight(35)
        self._text_color = QColor("black")
        self.anim = QPropertyAnimation(self, b"textColor")
        self.anim.setDuration(200)  # 200 ms transition
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.updateStyleSheet()
        self.setCursor(Qt.PointingHandCursor)

    def getTextColor(self):
        return self._text_color

    def setTextColor(self, color):
        if isinstance(color, QColor):
            self._text_color = color
            self.updateStyleSheet()

    textColor = pyqtProperty(QColor, fget=getTextColor, fset=setTextColor)

    def updateStyleSheet(self):
        # Only the text color is animated; padding and font remain fixed.
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                font-size: 20px;
                color: {self._text_color.name()};
                padding: 5px 10px;
            }}
        """)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._text_color)
        self.anim.setEndValue(QColor("#8A2BE2"))  # Hover color (whiter tone can be adjusted)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._text_color)
        self.anim.setEndValue(QColor("black"))
        self.anim.start()
        super().leaveEvent(event)


class Dock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the dock's fixed height; width will be managed by the layout.
        self.setFixedHeight(100)

        # Create a horizontal layout that scales with the parent.
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 10)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Create navigation buttons using AnimatedButton.
        home_button = AnimatedButton("Home", self)
        repo_link = AnimatedButton("Repository", self)
        vb_discord_link = AnimatedButton("Official Discord", self)

        # Create a spacer widget to push the settings button to the right.
        spacer = QLabel("")
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Settings button.
        settings_button = AnimatedButton("⚙ Settings", self)

        # Add widgets to the layout.
        layout.addWidget(home_button)
        layout.addWidget(repo_link)
        layout.addWidget(vb_discord_link)
        layout.addWidget(spacer)
        layout.addWidget(settings_button)

