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


# Handle messages from the client
def deal(message):
    parts=message.split(' ',2)
    if len(parts)<2:
        return "020 ERR bad format"
    cmd=parts[1]
    if cmd =='R':  #read operation
        ok,v=ts.read(parts[2])
        if ok:
            stats['read']+=1
            stats['ops']+=1
            res=f"OK ({parts[2]}, {v}) read"
            return f"{len(res)+4:03} {res}"
        else:
            stats['error']+=1
            stats['ops']+=1
            return f"024 ERR {parts[2]} does not exist"
    elif cmd =='G':  #get operation
        ok,v=ts.get(parts[2])
        if ok:
            stats['get']+=1
            stats['ops']+=1
            res=f"OK ({parts[2]}, {v}) removed"
            return f"{len(res)+4:03} {res}"
        else:
            stats['error']+=1
            stats['ops']+=1
            return f"024 ERR {parts[2]} does not exist"
    elif cmd =='P':  #put operation
        if len(parts)<3:
            return "020 ERR bad format"
        k_v=parts[2].split(' ',1)
        if len(k_v) !=2:
            return "020 ERR bad format"
        k,v=k_v
        ok=ts.put(k,v)  #put tuples
        if ok:
            stats['put']+=1
            stats['ops']+=1
            res = f"OK ({k}, {v}) added"
            return f"{len(res)+4:03} {res}"
        else:
            stats['error']+=1
            stats['ops']+=1
            return f"024 ERR {k} already exists"
    else:  
        stats['error']+=1  #Handle unknown information
        return"020 ERR unknown cmd"
    
    def report():
        while True:
            time.sleep(10)
            print(f"Clients: {stats['clients']},Ops:{stats['ops']}, READ: {stats['read']},GET:{stats['get']},PUT:{stats['put']},ERR:{stats['error']}")

    def main():
        import sys
        if len(sys.argv) !=2:
            print("python server.py <port>")
            return
        port = int(sys.argv[1])
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('0.0.0.0',port))
        s.listen()
        thhreading.Thread(target=report, deamon=True).start()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

    if __name__ == "__main__":
        main() 
    
            

    
