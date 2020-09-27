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
    global cache
    global current_size
    global max_size_of_cache
    global buffer
    global fileList

    while True:
        request = conn.recv(buffer).decode()
        if request:
            if request == "listCache":
                conn.send(str(fileList).encode())
            else:
                print("Client", addr, "requesting file", request)
                if request in cache:
                    lock.acquire()
                    content = pickle.loads(cache[request][1])
                    conn.send(content)
                    print("Cache hit. File", request, "sent to client.")
                    lock.release()
                else:
                    try:
                        file = open(directory+request, 'rb')
                        content = file.read()
                        size_of_file = len(content)
                        if size_of_file > max_size_of_cache:
                            conn.send(content)
                            print("Cache miss. File", request, "sent to client.")
                        else:
                            lock.acquire()
                            while (size_of_file + current_size) > max_size_of_cache:
                                current_size -= cache[fileList[0]][0]
                                cache.pop(fileList[0])
                                fileList.pop(0)
                            set_to_cache = (size_of_file,pickle.dumps(content))
                            cache[request] = set_to_cache
                            current_size += size_of_file
                            fileList.append(request)
                            conn.send(content)
                            print("Cache miss. File", request, "sent to client.")
                            lock.release()
                        file.close()
                    except FileNotFoundError:
                        print("File", data, "does not exist")
                        conn.send("FDnE")
    conn.close()

while True:
    s.listen()
    conn, addr = s.accept()
    lock = threading.Semaphore()
    client = Thread(target=connection, args=(conn, addr, lock))
    client.start()

s.close()                         