import socket
import threading
import time
from tuple_space import TupleSpace

ts=TupleSpace()
stats={
    'client':0,
    'read':0,  #The number of successful read operations
    'get':0,  #                          get
    'put':0,  #                          put
    'error':0,  #The number of errors
    'ops':0  #Total number of operations
}

# Functions that handle a single client connection
def handle_client(conn,addr):
    stats['clients']+=1
    try:
        while True:
            msg=conn.recv(1024)
            if not msg:
                break
            reply=deal(msg.decode())
            conn.sendall(reply.encode())
    except Exception as e:
        print(f"Exception from {addr}: {e}")  #Print exception information
    finally:
        conn.close()  #Close the connection, no matter what

    
