#widget library to make ui creation easy
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from ui.styles import GREY, RED


def make_panel():
    f = QFrame()
    f.setObjectName("panel")
    return f


class Led(QLabel):
    # circle indicator which you can set a certain color to

    def __init__(self, size=10):
        super().__init__()
        self._size = size
        self.setFixedSize(size, size)
        self.set_color(GREY)

    def set_color(self, color):
        self.setStyleSheet(
            f"background:{color}; border-radius:{self._size // 2}px; border:1px solid #111;"
        )


class IndicatorRow(QWidget):
    # basically an led but if you also have text

    def __init__(self, text):
        super().__init__()
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        self.led = Led()
        lay.addWidget(self.led)
        lay.addWidget(QLabel(text))
        lay.addStretch()

    def set_color(self, color):
        self.led.set_color(color)


class StatusBar(QWidget):
    # kinda liked indicator row but the orientation and layout is flipped

    def __init__(self, text):
        super().__init__()
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addStretch()
        lay.addWidget(QLabel(text))
        self.bar = QLabel()
        self.bar.setFixedSize(30, 10)
        lay.addWidget(self.bar)
        self.set_color(RED)

    def set_color(self, color):
        self.bar.setStyleSheet(f"background:{color}; border:1px solid #111;")
