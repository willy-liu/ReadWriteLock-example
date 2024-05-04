import socket
import threading
import json
import atexit
import queue

# maintained array of 10 integers
num_array = [0] * 10

# create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
atexit.register(serversocket.close)

# Set SO_REUSEADDR to 1 to reuse the socket
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket to localhost and port 9999
host = "127.0.0.1"
port = 9999
serversocket.bind((host, port))

# set max client connections
serversocket.listen(60)

# set timeout to 5 seconds
serversocket.settimeout(5.0)

busy_loop_max = int(2e6)

class ReadWriteLock:
    def __init__(self):
        self.condition = threading.Condition()
        self.readers = 0
        self.writers_waiting = queue.Queue()  # Queue to manage writer order
        self.writers = 0

    def acquire_read_lock(self):
        with self.condition:
            while self.writers > 0 or not self.writers_waiting.empty():
                self.condition.wait()
            self.readers += 1

    def release_read_lock(self):
        with self.condition:
            self.readers -= 1
            if self.readers == 0:
                self.condition.notify_all()

    def acquire_write_lock(self):
        # Using queue for fair ordering
        wait_entry = threading.Event()
        self.writers_waiting.put(wait_entry)
        with self.condition:
            # if someone is using shared data or waiting writer is not first should wait
            while self.readers > 0 or self.writers > 0 or (self.writers_waiting.queue[0] != wait_entry):
                self.condition.wait()
            self.writers_waiting.get()
            wait_entry.set()  # Signal to next writer, if there is one
            self.writers += 1

    def release_write_lock(self):
        with self.condition:
            self.writers -= 1
            if self.writers == 0:
                self.condition.notify_all()

# lock for synchronization
lock = ReadWriteLock()

# read_thread
def read_thread(clientsocket, op: str, num: int):
    try:
        lock.acquire_read_lock()
        # busy loop
        busy_loop = 0
        while busy_loop <= busy_loop_max:
            busy_loop += 1
        
        ret = []
        for data in num_array:
            condition = f"{data} {op} {num}"
            # print(condition)
            if eval(condition) is True or eval(condition) is 0:
                ret.append(data)
        clientsocket.send(f"num[10]{op}{num}: {json.dumps(ret)}".encode('utf-8'))
    finally:
        clientsocket.close()
        lock.release_read_lock()

# write_thread
def write_thread(clientsocket, new_num_array: list[int]):
    global num_array
    try:
        lock.acquire_write_lock()
        # busy loop
        busy_loop = 0
        while busy_loop <= busy_loop_max:
            busy_loop += 1

        # when acquired lock then we can write data and return status to client.
        num_array = new_num_array
        # print(num_array)
        clientsocket.send(f"num[10]={json.dumps(num_array)}".encode('utf-8'))
    finally:
        clientsocket.close()
        lock.release_write_lock()
    
def main():
    print("Server listening on")
    while True:
        try:
            # wait for connection
            clientsocket, addr = serversocket.accept()
            # receive message(operation) from client
            msg = clientsocket.recv(1024)

            # parse message
            parsed_msg = json.loads(msg)
            print("="*10)
            print(f"client message: {parsed_msg}")
            if parsed_msg["operation"] == "read":
                threading.Thread(target=read_thread, args=(clientsocket, parsed_msg["op"], parsed_msg["num"])).start()
            elif parsed_msg["operation"] == "write":
                threading.Thread(target=write_thread, args=(clientsocket, parsed_msg["new_num_array"])).start()
            
        except socket.timeout:
            if clientsocket:
                clientsocket.close()
            continue

if __name__ == "__main__":
    main()
