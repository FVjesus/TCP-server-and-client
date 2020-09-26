import socket
import sys
import pickle
import threading
from threading import Thread

port = int(sys.argv[1])
directory = sys.argv[2]

cache = {}
current_size = 0
max_size_of_cache = 64*1024**2

buffer = 1024
fileList = []

s = socket.socket()
s.bind(('localhost',port))

def connection(conn, addr, lock):
    lock.acquire()

    global cache
    global current_size
    global max_size_of_cache
    global buffer
    global fileList

    while True:
        request = conn.recv(buffer).decode()
        if request == "listCache":
            conn.send(pickle.dumps(str(fileList)))
        else:
            print("Client", addr, "requesting file", request)
            if request in cache:
                conn.send(pickle.dumps(cache[request][1]))
                print("Cache hit. File", request, "sent to client.")
            else:
                try:
                    file = open(directory+request, 'rb')
                    content = file.read()
                    size_of_file = len(content)
                    if size_of_file > max_size_of_cache:
                        conn.send(pickle.dumps(content))
                        print("Cache miss. File", request, "sent to client.")
                    else:
                        while (size_of_file + current_size) > max_size_of_cache:
                            current_size -= cache[fileList[0]][0]
                            cache.pop(fileList[0])
                            fileList.pop(0)
                        set_to_cache = (size_of_file, content)
                        cache[request] = set_to_cache
                        current_size += size_of_file
                        fileList.append(request)
                        conn.send(pickle.dumps(content))
                        print("Cache miss. File", request, "sent to client.")
                    file.close()
                except FileNotFoundError:
                    print("File", data, "does not exist")
                    conn.send(pickle.dumps("FDnE"))
        lock.release()
    conn.close()

while True:
    s.listen()
    conn, addr = s.accept()
    lock = threading.Lock()
    Thread(target=connection, args=(conn, addr, lock)).start()

s.close()                         