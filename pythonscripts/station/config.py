from PyQt6.QtCore import Qt

ROBOT_IP = "192.168.4.1"
ROBOT_PORT = 5000

# enable robot keys
ENABLE_KEYS = {Qt.Key.Key_BracketLeft, Qt.Key.Key_BracketRight, Qt.Key.Key_Backslash}
# disable keys
DISABLE_KEYS = {Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space}

# message to send
ENABLE_MESSAGE = "enable"
DISABLE_MESSAGE = "disable"

# changeable flash time for when robot responds to computer
RX_FLASH_MS = 100
