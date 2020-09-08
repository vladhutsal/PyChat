import socket
import sys
import select

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1027))


while True:
    slist = [sys.stdin, client]
    readable, _, _ = select.select(slist, [], [])
    for socket in readable:
        if socket == client:        # if data goes from socket
            msg = socket.recv(2048)
            if not msg:
                print('lost connection')
                exit()
            msg = msg.decode(encoding='utf-8')
            print(msg)
        else:                       # if data goes from user`s input
            message = sys.stdin.readline().strip()
            client.send(message.encode(encoding='utf-8')) 
            sys.stdout.flush() 
