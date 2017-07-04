import socket
import sys
port = 70
host = sys.argv[1]
filename = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall('{}\r\n'.format(filename).encode('utf8'))
while True:
    buf = s.recv(2048)
    if not len(buf):
        break
    sys.stdout.write(buf.decode('utf8'))
