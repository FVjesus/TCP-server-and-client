# TCP Server Client
> Project proposed in the discipline of Distributed Systems.

This system consists of a server and a client, the server is responsible for sending files requested by the client via TCP communication.

## Server

The server is responsible for fetching the file and sending it to the client, if the file is already in the cache the server will not fetch it from the directory provided at the start of the server.

A cache listing request can also be received, in this scenario the server will return a list with the names of the files in the cache.

#### Cache
When a requested file is not in the cache the server will add it to the cache, if there is not enough space the older file is removed, this process is repeated until the necessary space is available, this concept is knonw as FIFO (first in, first out).
#### How use
To start the server it is necessary to inform the port it will listen to and the directory containing the files.
```sh
python3 server.py port directory
```
```sh
python3 server.py 3333 \home\
```
## Client

The client can request a list of the files that are cached, or request the transfer of a file.

#### How use
There are two use cases for the client, requesting a file and requesting the cache listing.

To request a file, 4 arguments are required: the host, the port the server listens to, the file name, and the directory it will be recorded in.

```sh
python3 client.py host port file directory
```
```sh
python3 client.py localhost 3333 hero.txt ./
```

To request a chace listing, 3 arguments are required: the host, the port the server listens to and the command "listCache".

```sh
python3 client.py host port listCache
```
```sh
python3 client.py localhost 3333 listCache

```

## Requisites
* [python 3 or higher](https://www.python.org/downloads/)
* [Socket](https://docs.python.org/3/library/socket.html)
* [Pickle](https://docs.python.org/3/library/pickle.html)
* [Thread](https://docs.python.org/3/library/threading.html)
## Meta
Fabrício Velôso de Jesus

Bachelor of Exact and Technological Sciences - UFRB

Graduating in Computer Engineering - UFRB

[linkedin](https://www.linkedin.com/in/fabricio-veloso-23aa92198/) - [github](https://github.com/FVjesus) - [gitlab](https://gitlab.com/fabriciovellozo)

fabriciovellozo@gmail.com



