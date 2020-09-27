import socket
import sys
import select

s = socket.socket()

ip = sys.argv[1]
port = int(sys.argv[2])
file = sys.argv[3]
directory = sys.argv[4]

buffer = 1024

s.connect((ip, port))
s.send(file.encode())
data = s.recv(buffer)
if file == "listCache":
   print(data)
else:
    if data == "FDnE":
        print("File", file, "does not exist in the server")
    else:
        f = open(directory+file, 'wb')
        f.write(data)
        while (select.select([s],[],[],0.1)[0]):
            data = s.recv(buffer)
            f.write(data)
        print("File",file, "saved")
        f.close()
s.close()