import socket


def connect_to_dictionary():
    UDP_DISCOVERY_PORT = 9000
    DICT_TCP_PORT = 2000
    TIMEOUT = 2
    # Step 1: UDP broadcast to find dictionary
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.settimeout(TIMEOUT)

    udp.sendto("WHO_IS_DICTIONARY".encode(),
               ("255.255.255.255", UDP_DISCOVERY_PORT))

    try:
        data, addr = udp.recvfrom(1024)
        if data.decode() != "d":
            return None

        dict_ip = addr[0]

    except socket.timeout:
        return None
    finally:
        udp.close()

    # Step 2: TCP connect to dictionary
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((dict_ip, DICT_TCP_PORT))

    return tcp


dict_socket = connect_to_dictionary()

if dict_socket:
    print("Connected to dictionary server")
    dict_socket.send("GET_SERVERS".encode())
    print(dict_socket.recv(4096).decode())
else:
    print("Dictionary server not found")

