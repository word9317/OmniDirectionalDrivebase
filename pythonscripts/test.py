import socket
import threading

ROCK_IP = "192.168.4.1"
PORT = 5000

def receiver(sock):

    while True:

        try:

            data = sock.recv(1024)

            if not data:
                break

            print(data.decode().strip())

        except:
            break

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect(
    (ROCK_IP, PORT)
)

print("Connected")

threading.Thread(
    target=receiver,
    args=(sock,),
    daemon=True
).start()

while True:

    message = input("> ")

    sock.sendall(
        (message + "\n").encode()
    )