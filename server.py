import socket
import threading
import time
from tuple_space import TupleSpace

ts=TupleSpace()
stats = {
    'client':0,
    'read':0,  #The number of successful read operations
    'get':0,  #                          get
    'put':0,  #                          put
    'error':0,  #The number of errors
    'ops':0  #Total number of operations
}

# Functions that handle a single client connection
def handle_client(conn,addr):
    stats['client']+=1
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
    try:
        # discard length prefix
        if len(message) < 4:
            return "020 ERR bad format"
        
        message = message[4:]  # remove NNN and space
        parts = message.split(' ', 2)

        if len(parts) < 2:
            return "020 ERR bad format"
        
        cmd = parts[0]
        
        if cmd == 'R':
            key = parts[1]
            ok, v = ts.read(key)
            if ok:
                stats['read'] += 1
                stats['ops'] += 1
                res = f"OK ({key}, {v}) read"
                return f"{len(res)+4:03} {res}"
            else:
                stats['error'] += 1
                stats['ops'] += 1
                return f"024 ERR {key} does not exist"

        elif cmd == 'G':
            key = parts[1]
            ok, v = ts.get(key)
            if ok:
                stats['get'] += 1
                stats['ops'] += 1
                res = f"OK ({key}, {v}) removed"
                return f"{len(res)+4:03} {res}"
            else:
                stats['error'] += 1
                stats['ops'] += 1
                return f"024 ERR {key} does not exist"

        elif cmd == 'P':
            key = parts[1]
            value = parts[2]
            ok = ts.put(key, value)
            if ok:
                stats['put'] += 1
                stats['ops'] += 1
                res = f"OK ({key}, {value}) added"
                return f"{len(res)+4:03} {res}"
            else:
                stats['error'] += 1
                stats['ops'] += 1
                return f"024 ERR {key} already exists"

        else:
            stats['error'] += 1
            return "020 ERR unknown cmd"
        
    except Exception as e:
        stats['error'] += 1
        return f"030 ERR internal error: {e}"
    
    #Print the current status of the server every 10 seconds
def report():
        while True:
            time.sleep(10)
            tuple_count = len(ts.data)

            if tuple_count > 0:
                total_key_len = sum(len(k) for k in ts.data)
                total_value_len = sum(len(v) for v in ts.data.values())
                avg_tuple_size = (total_key_len + total_value_len) / tuple_count
                avg_key_size = total_key_len / tuple_count
                avg_value_size = total_value_len / tuple_count
            else:
                avg_tuple_size = avg_key_size = avg_value_size = 0
            
            print(f"Tuples: {tuple_count}, Avg Tuple Size: {avg_tuple_size:.2f}, "
              f"Avg Key Size: {avg_key_size:.2f}, Avg Value Size: {avg_value_size:.2f}, "
              f"Clients: {stats['client']}, Ops: {stats['ops']}, READ: {stats['read']}, "
              f"GET: {stats['get']}, PUT: {stats['put']}, ERR: {stats['error']}")
            
            
            
    #Main function: Start the server and accept connections
def main():
    import sys
        #Parameter check
    if len(sys.argv) !=2:
            print("python server.py <port>")
            return
    port = int(sys.argv[1])  #Get port number
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('0.0.0.0',port))
    s.listen()  #listen port
    threading.Thread(target=report, daemon=True).start()  #Backend thread printing report
     #Loop receive client connection
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

    #entrance
if __name__ == "__main__":
    main() 
    
            

    
