from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLayout, QPushButton, QTextEdit, QVBoxLayout, QWidget, QComboBox
)

from config import (
    DISABLE_MESSAGE, DRIVE_SEND_MS, ENABLE_MESSAGE, LOG_DRIVE, ROBOT_IP, ROBOT_PORT, RX_FLASH_MS,
)
from core.key_tracker import KeyTracker
from core.robot_link import RobotLink
from core.controller import ControllerInput
from ui.styles import BLUE, GREEN, GREY, LOG_COLORS, ORANGE, RED
from ui.widgets import IndicatorRow, StatusBar, make_panel


class DriverStation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Station")
        self.resize(900, 420)

        self.enabled = False

        self.link = RobotLink(ROBOT_IP, ROBOT_PORT, self)
        self.link.connected.connect(self.on_connected)
        self.link.disconnected.connect(self.on_disconnected)
        self.link.error.connect(self.on_error)
        self.link.line_received.connect(self.on_line_received)
        self.controller = ControllerInput()
        self._build_ui()
        self.refresh_controllers()

        self.keys = KeyTracker(self)
        self.keys.enable_pressed.connect(self.request_enable)
        self.keys.disable_pressed.connect(self.request_disable)
        QApplication.instance().installEventFilter(self.keys)

        # flash when robot sends stuff back
        self.rx_flash = QTimer(self)
        self.rx_flash.setSingleShot(True)
        self.rx_flash.setInterval(RX_FLASH_MS)
        self.rx_flash.timeout.connect(self.refresh_status)

        self.refresh_status()
        self.drive_timer = QTimer(self)
        self.drive_timer.setInterval(DRIVE_SEND_MS)
        self.drive_timer.timeout.connect(self.send_drive)
        self.drive_timer.start()
        self.connect_to_robot()

    # ui maker helper function
    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)
        root.addWidget(self._build_comm_panel())
        root.addWidget(self._build_overview_panel())
        root.addWidget(self._build_log_panel(), 1)

    def _build_comm_panel(self):
        panel = make_panel()
        lay = QVBoxLayout(panel)
        title = QLabel("Communications")
        title.setObjectName("title")
        lay.addWidget(title)

        self.row_link = IndicatorRow("Robot Link (TCP)")
        self.row_robot = IndicatorRow("Robot")
        self.row_enabled = IndicatorRow("Enabled")
        for row in (self.row_link, self.row_robot, self.row_enabled):
            lay.addWidget(row)

        lay.addSpacing(10)
        ctrl_title = QLabel("Controller")
        ctrl_title.setObjectName("title")
        lay.addWidget(ctrl_title)
        self.controller_box = QComboBox()
        self.controller_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.controller_box.currentIndexChanged.connect(self.on_controller_selected)
        lay.addWidget(self.controller_box)
        refresh_btn = QPushButton("Refresh Controllers")
        refresh_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        refresh_btn.clicked.connect(self.refresh_controllers)
        lay.addWidget(refresh_btn)
        
        lay.addStretch()
        reconnect_btn = QPushButton("Reconnect to Robot")
        reconnect_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        reconnect_btn.clicked.connect(self.connect_to_robot)
        lay.addWidget(reconnect_btn)
        panel.setFixedWidth(210)
        return panel

    def _build_overview_panel(self):
        panel = make_panel()
        lay = QVBoxLayout(panel)
        lay.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        overview = QLabel("Overview")
        overview.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        overview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(overview)

        self.sb_comm = StatusBar("Communications")
        self.sb_code = StatusBar("Robot")
        lay.addWidget(self.sb_comm)
        lay.addWidget(self.sb_code)

        lay.addSpacing(10)
        self.state_label = QLabel("Disabled")
        self.state_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.state_label)
        lay.addSpacing(10)
        self.drive_label = QLabel("Drive  x 0.00   y 0.00   z 0.00")
        self.drive_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.drive_label)
        lay.addStretch()
        panel.setFixedWidth(250)
        return panel

    def _build_log_panel(self):
        panel = make_panel()
        lay = QVBoxLayout(panel)
        title = QLabel("Message Log")
        title.setObjectName("title")
        lay.addWidget(title)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        lay.addWidget(self.log, 1)

        clear_btn = QPushButton("Clear Log")
        clear_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        clear_btn.clicked.connect(self.log.clear)
        lay.addWidget(clear_btn)
        return panel

    # logging data
    def log_line(self, kind, text):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.log.append(
            f'<span style="color:#777">{ts}</span> '
            f'<span style="color:{LOG_COLORS.get(kind, "#ccc")}"><b>{kind}</b> {safe}</span>'
        )

    # function to connect to robot
    def connect_to_robot(self):
        # make sure robot starts disabled(so you dont)
        self.enabled = False
        self.log_line("system", f"Connecting to {ROBOT_IP}:{ROBOT_PORT} ...")
        self.link.open()
        self.refresh_status()

    def on_connected(self):
        self.log_line("system", "Connected")
        self.refresh_status()

    def on_disconnected(self):
        self.enabled = False
        self.log_line("system", "Disconnected")
        self.refresh_status()

    def on_error(self, message):
        self.enabled = False
        self.log_line("error", message)
        self.refresh_status()

    def on_line_received(self, text):
        self.log_line("RX", text)
        self.sb_code.set_color(BLUE)
        self.rx_flash.start()

    def send(self, message):
        if not self.link.send(message):
            self.log_line("error", f"Not connected, can't send: {message}")
            return False
        self.log_line("TX", message)
        return True

    def request_enable(self):
        if self.enabled:
            return
        if self.send(ENABLE_MESSAGE):
            self.enabled = True
            self.refresh_status()

    def request_disable(self):
        self.enabled = False
        if self.link.is_connected:
            self.send(DISABLE_MESSAGE)
        self.refresh_status()

    def refresh_status(self):
        connected = self.link.is_connected
        connecting = self.link.is_connecting

        self.row_link.set_color(GREEN if connected else (ORANGE if connecting else RED))
        self.row_robot.set_color(GREEN if connected else GREY)
        self.row_enabled.set_color(GREEN if self.enabled else GREY)
        self.sb_comm.set_color(GREEN if connected else RED)
        self.sb_code.set_color(GREEN if connected else RED)

        conn_text = "Connected" if connected else ("Connecting..." if connecting else "No Connection")
        state_text = "Enabled" if self.enabled else "Disabled"
        self.state_label.setText(f"{conn_text}\n{state_text}")
        self.state_label.setStyleSheet(
            f"color:{GREEN if self.enabled else ('#e6e6e6' if connected else RED)};"
        )

    def closeEvent(self, event):
        self.drive_timer.stop()      # no drive frame may follow the final disable
        self.enabled = False
        self.link.close(last_message=DISABLE_MESSAGE)
        self.controller.shutdown()
        super().closeEvent(event)

    def refresh_controllers(self):
        self.controller_box.blockSignals(True)
        self.controller_box.clear()
        self.controller_box.addItem("No controller", None)
        for index, name in self.controller.list_controllers():
            self.controller_box.addItem(name, index)
        self.controller_box.blockSignals(False)
        self.on_controller_selected()

    def on_controller_selected(self, _row=None):
        self.controller.select(self.controller_box.currentData())

    def send_drive(self):
        x, y, z = self.controller.read()
        self.drive_label.setText(f"Drive  x {x:.2f}   y {y:.2f}   z {z:.2f}")
        if not (self.enabled and self.controller.active):
            return
        message = f"{x:.2f}:{y:.2f}:{z:.2f}"
        if LOG_DRIVE:
            self.send(message)
        else:
            self.link.send(message)