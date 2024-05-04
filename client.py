import socket
import json
import time
import random
import threading

# num OP NUM
OP = "%"
NUM = 2

host = "127.0.0.1"
port = 9999

def reader_thread(name):
    time.sleep(random.randint(1, 20)/10.0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # 傳送數據
    message = {"operation": "read",
            "op": OP,
            "num": NUM}
    s.send(json.dumps(message).encode('utf-8'))

    # 接收小於 1024 字節的數據
    msg = s.recv(1024)
    s.close()

    print(name, '\t', msg.decode('utf-8'))


def writer_thread(name, start = 0):
    time.sleep(random.randint(1, 20)/10.0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # send message
    message = {"operation": "write",
            "new_num_array": [i for i in range(start, start+10, 1)]
            }
    s.send(json.dumps(message).encode('utf-8'))

    # receive message(operation) from client
    msg = s.recv(1024)
    s.close()
    print(name, "done!\t", msg.decode('utf-8'))

for i in range(30):
    threading.Thread(target=reader_thread, args=(f"#reader:{i}", )).start()
    threading.Thread(target=writer_thread, args=(f"writer:{i}", i*10, )).start()
