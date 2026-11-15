from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QAbstractSocket, QTcpSocket

State = QAbstractSocket.SocketState


class RobotLink(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error = pyqtSignal(str)
    line_received = pyqtSignal(str)

    def __init__(self, host, port, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self._buffer = b""

        self._sock = QTcpSocket(self)
        self._sock.connected.connect(self.connected)
        self._sock.disconnected.connect(self.disconnected)
        self._sock.readyRead.connect(self._on_ready_read)
        self._sock.errorOccurred.connect(lambda _e: self.error.emit(self._sock.errorString()))

    @property
    def is_connected(self):
        return self._sock.state() == State.ConnectedState

    @property
    def is_connecting(self):
        return self._sock.state() in (State.ConnectingState, State.HostLookupState)

    def open(self):
        # reopen or open connection using functions
        self._sock.abort()
        self._buffer = b""
        self._sock.connectToHost(self.host, self.port)

    def send(self, message):
        # send mesage, but return false so if not connected, app doesnt explode
        if not self.is_connected:
            return False
        self._sock.write((message + "\n").encode())
        return True

    def close(self, last_message=None):
        if last_message and self.is_connected:
            self.send(last_message)
            self._sock.flush()
        self._sock.abort()

    def _on_ready_read(self):
        self._buffer += bytes(self._sock.readAll())
        while b"\n" in self._buffer:
            line, self._buffer = self._buffer.split(b"\n", 1)
            text = line.decode(errors="replace").strip()
            if text:
                self.line_received.emit(text)
