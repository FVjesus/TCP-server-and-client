import socket
import sys
import pickle

s = socket.socket()

address = sys.argv[1]
port = int(sys.argv[2])
x = sys.argv[3]
y = sys.argv[4]

s.connect((address, port))

msg = pickle.dumps((x,y))

s.send(msg)

data = s.recv(1024)
z = pickle.loads(data)

print('%s*%s = %d'%(x,y,z))