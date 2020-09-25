import socket
import sys
import pickle
import time

s = socket.socket()

port = int(sys.argv[1])

s.bind(('localhost',port))
s.listen()

while True:
    print('waiting conexion')

    conn, addr = s.accept()

    data = conn.recv(1024)
    x,y = pickle.loads(data)

    print('log: processing...')
    time.sleep(10)

    z = int(x)*int(y)

    print('log: %s X %s = %d'%(x,y,z))

    msg = pickle.dumps(z)

    conn.send(msg)