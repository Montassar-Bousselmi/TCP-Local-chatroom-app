# TCP-Local-chatroom-app

How it works : 
each server ( chatroom ) needs to connect to the dictionary so it registers its ip and port 
each client needs to connect to the dictionary to find the ips and ports of available chatrooms to connect to them

and to find the dictionary they do a udp broadcast and the dictionary accepts it and give its ip and port for a tcp connection
