import socket
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(('', 0)) # Random port
sock.sendto(b'hello', ('192.168.1.134', 5000)) # server ip and port
data = sock.recv(128)
data = data.decode('utf-8').split(' ')

def listen_to_peer() -> None:
    print('Listening to peer on port: ', sock.getsockname()[1])
    while True:
        hi = sock.recv(1024)
        print("Peer sent: ", hi.decode('utf-8'))


t = Thread(target=listen_to_peer, daemon=True)
t.start()


while True:
    message = input("Enter message: ")
    print("Sending to: ", data)
    sock.sendto(message.encode('utf-8'), (data[0], int(data[1])))
