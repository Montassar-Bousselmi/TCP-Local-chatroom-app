import socket
import json
import threading

UDP_PORT = 9000
TCP_PORT = 2000

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def udp_discovery():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "WHO_IS_DICTIONARY":
            sock.sendto("d".encode(), addr)

thread=threading.Thread(target=udp_discovery,daemon=True).start()

server_list = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0",TCP_PORT ))
s.listen()

print("Dictionary server listening on port 2000.")

while True:
    conn, addr = s.accept()
    print("Connected by", addr)
    conn.settimeout(5)

    try:
        print("Waiting for data...")
        msg = conn.recv(1024)

        if not msg:
            print("Client closed connection without sending data")
            conn.close()
            continue

        msg = msg.decode("utf-8")
        print("Received:", msg)

        if msg[0] == "S":
            server_list.append(addr)
            conn.send(bytes(str(addr[1]), "utf-8"))

            print(server_list)
        elif msg[0] == "C":
            conn.send(json.dumps(server_list).encode())

    except ConnectionResetError:
        print("Client disconnected unexpectedly")

    finally:
        conn.close()
