from PyQt6.QtCore import Qt
import sys

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

# controller values
DRIVE_SEND_MS = 50                  # how often x:y:z is sent while enabled
STICK_DEADZONE = 0.10               # "fix" stick drift for my poor controllers =(
TURN_COEFFICIENT_INVERSE = 2.0      # undetermined coefficinet for the z axis sensitivity tuning
LOG_DRIVE = False                   # debugging log tool

if sys.platform == "win32":
    AXIS_LEFT_X, AXIS_LEFT_Y, AXIS_RIGHT_X = 0, 1, 2
else:
    AXIS_LEFT_X, AXIS_LEFT_Y, AXIS_RIGHT_X = 0, 1, 3