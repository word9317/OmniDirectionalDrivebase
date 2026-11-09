#!/usr/bin/env python3

import socket
import serial
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

ARDUINO_PORTS = [
    "/dev/ttyACM0",
    "/dev/ttyUSB0",
    "/dev/ttyACM1",
    "/dev/ttyUSB1"
]

BAUD_RATE = 9600

arduino = None
client_socket = None

arduino_lock = threading.Lock()
client_lock = threading.Lock()

def connect_arduino():
    global arduino

    while True:

        for port in ARDUINO_PORTS:

            try:

                print(f"[INFO] Trying Arduino on {port}")

                arduino = serial.Serial(
                    port,
                    BAUD_RATE,
                    timeout=0.1
                )

                time.sleep(2)

                print(f"[OK] Connected to Arduino on {port}")

                return

            except Exception:
                pass

        print("[WARN] Arduino not found")
        print("[INFO] Retrying in 3 seconds...\n")

        time.sleep(3)

def send_to_client(message):

    global client_socket

    with client_lock:

        if client_socket is None:
            return

        try:

            client_socket.sendall(
                (message + "\n").encode()
            )

        except Exception:

            try:
                client_socket.close()
            except:
                pass

            client_socket = None

def serial_reader():

    global arduino

    while True:

        try:

            if arduino is not None and arduino.in_waiting:

                line = (
                    arduino.readline()
                    .decode(errors="ignore")
                    .strip()
                )

                if line:

                    print(f"[ARDUINO] {line}")

                    send_to_client(
                        f"ARDUINO:{line}"
                    )

        except Exception as e:

            print(f"[ERROR] Serial lost: {e}")

            try:
                arduino.close()
            except:
                pass

            connect_arduino()

        time.sleep(0.01)
def handle_client(conn, address):

    global client_socket

    with client_lock:
        client_socket = conn

    print(f"[CLIENT CONNECTED] {address}")

    send_to_client("CONNECTED")

    try:

        while True:

            data = conn.recv(1024)

            if not data:
                break

            command = (
                data
                .decode(errors="ignore")
                .strip()
            )

            if not command:
                continue

            print(f"[PC] {command}")

            if arduino is not None:

                with arduino_lock:

                    arduino.write(
                        (command + "\n").encode()
                    )

    except Exception as e:

        print(f"[CLIENT ERROR] {e}")

    print("[CLIENT DISCONNECTED]")

    try:
        conn.close()
    except:
        pass

    with client_lock:
        client_socket = None
def main():

    print("started i think")

    connect_arduino()

    threading.Thread(
        target=serial_reader,
        daemon=True
    ).start()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[OK] Listening on {HOST}:{PORT}")

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    main()