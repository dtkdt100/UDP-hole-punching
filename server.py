# Server
# Runs as rendezvous server
# Need to have to clients connected to it
# When both clients are connected, it will exschange the information between the two clients
# Information: 
#  - Router IP of the second client
#  - Destination port of the second client
#  - Source port of the second client
import socket

clients_addrs: dict[str, list] = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
server_socket.bind(('', 5000))

def send_information_to_clients(peers) -> None:
    server_socket.sendto('{} {}'.format(peers[1][0], peers[1][1]).encode('utf-8'), peers[0])
    server_socket.sendto('{} {}'.format(peers[0][0], peers[0][1]).encode('utf-8'), peers[1])


def listen_to_connections() -> None:
    print("Server started")

    while len(clients_addrs) < 2:
        data, addr = server_socket.recvfrom(128)

        print("Connection from: " + str(addr))

        data = data.decode('utf-8')

        if data not in clients_addrs:
            clients_addrs[data] = [addr]
        else:
            clients_addrs[data].append(addr)

        if len(clients_addrs[data]) == 2:
            print("Both clients connected, data: ", data)
            send_information_to_clients(clients_addrs[data])
            print("Information sent")
            del clients_addrs[data] 

    server_socket.close()
    exit()


listen_to_connections()
