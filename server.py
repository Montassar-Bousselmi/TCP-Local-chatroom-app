import socket
import threading

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

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

s1 = connect_to_dictionary()
print("Connected to server")
s1.send(b"S")   # send role

reply = s1.recv(1024)   # wait for server response
print("Server reply:", reply.decode())
reply = reply.decode()

s1.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((myip(), int(reply)))
s.listen()


conn, addr = s.accept()

def recieve(s):
    while True:
        try:
            msg = s.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except :
            break


thread = threading.Thread(target=recieve, args=(conn,))
thread.start()

while True:
    msg = input(">")
    if msg == "exit":
        break
    msg = msg.encode()
    conn.send(msg)
print("server closed")
conn.close()
s.close()










