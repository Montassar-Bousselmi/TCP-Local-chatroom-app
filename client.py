import socket
import json
import threading

def connect_to_dictionary():
    UDP_DISCOVERY_PORT = 9000
    DICT_TCP_PORT = 2000
    TIMEOUT = 2
    # udp broadcast to find dictionary
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


s1 = connect_to_dictionary()
print("Connected to server")
s1.send(b"C")   # send role
reply = json.loads(s1.recv(1024).decode())   # wait for server response
print(reply)

s1.close()

n = int(input("enter the chatbot number"))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((reply[n][0], reply[n][1]))

def recieve(s):
    while True:
        try:
            msg = s.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except :
            break


thread = threading.Thread(target=recieve, args=(s,))
thread.start()

while True:
    msg = input(">")
    if msg == "exit":
        break
    msg = msg.encode()
    s.send(msg)
print("server closed")
s.close()