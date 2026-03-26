import socket
import threading

UDP_PORT = 9000
TCP_PORT = 2000

# --- UDP discovery ---
def udp_discovery():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "WHO_IS_DICTIONARY":
            sock.sendto("d".encode(), addr)

# --- TCP service ---
def tcp_service():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", TCP_PORT))
    server.listen()

    while True:
        client, addr = server.accept()
        print("Client connected:", addr)

threading.Thread(target=udp_discovery, daemon=True).start()
tcp_service()
