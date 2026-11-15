from PyQt6.QtCore import QEvent, QObject, pyqtSignal

from config import DISABLE_KEYS, ENABLE_KEYS


class KeyTracker(QObject):
    enable_pressed = pyqtSignal()
    disable_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._down = set()

    def eventFilter(self, obj, event):
        t = event.type()

        if t == QEvent.Type.KeyPress:
            if event.isAutoRepeat():
                return False
            key = event.key()

            if key in ENABLE_KEYS:
                self._down.add(key)
                if self._down >= ENABLE_KEYS:
                    self.enable_pressed.emit()
                    return True
                return False

            if key in DISABLE_KEYS:
                self.disable_pressed.emit()
                return True

        elif t == QEvent.Type.KeyRelease:
            if not event.isAutoRepeat():
                self._down.discard(event.key())

        elif t == QEvent.Type.WindowDeactivate:
            self._down.clear()

        return False
