import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 1027))
server.listen(50)


def new_connection(readable, socket):
    client_socket, adress = socket.accept()
    print('user {} connected'.format(adress[1]))
    client_socket.setblocking(0)
    connections.append(client_socket)
    clients.append(client_socket)


def listening_for_clients(socket):
    nickname = socket.getpeername()[1]
    msg_from_client = socket.recv(2048).decode(encoding='utf-8')
    if not msg_from_client:             # if something went wrong
        print('user {} has left'.format(nickname))
        connections.remove(socket)
        clients.remove(socket)
        pass
    else:
        msg_to_all = bytearray(source='{}-->> {}'.format(nickname, msg_from_client),
                               encoding='utf-8')
        broadcast(msg_to_all, socket)


def broadcast(msg_to_all, socket):
    for client in clients:
        if client == socket:
            pass
        else:
            client.send(msg_to_all)
 

connections = [server]      # all sockets including server one
clients = []        # only client sockets

while connections:
    readable, _, _ = select.select(connections, [], [])
    for socket in readable:
        if socket == server:       
            new_connection(readable, socket)    # if we`ve got new connection
        elif socket != server:     
            listening_for_clients(socket)   # if we waiting for messages



