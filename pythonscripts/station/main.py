import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import DriverStation
from ui.styles import STYLE


app = QApplication(sys.argv)
app.setStyleSheet(STYLE)
window = DriverStation()
window.show()
sys.exit(app.exec())