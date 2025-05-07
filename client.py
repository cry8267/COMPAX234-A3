import socket
import sys
import os

# This function turns a line from the input file into a message string for the server 
def make(line):
    parts = line.strip().split(' ', 2)  #split into at most 3 parts
   
   # handle PUT command 
    if parts[0] == 'PUT' and len(parts) == 3:
        k = parts[1]
        v = parts[2]
        msg = f"P {k} {v}"
    
    # handle READ command,just needs key
    elif parts[0] == 'READ' and len(parts) == 2:
        k = parts[1]
        msg = f"R {k}"
    
    # handle GET command,just needs key 
    elif parts[0] == 'GET' and len(parts) == 2:
        k = parts[1]
        msg = f"G {k}"
    else:  # anything else is invalid
        return None
    
    total_len = 3 + 1 +len(msg)  #Include NNN + 1 space
    if total_len >999:
        return None
    return f"{total_len:03d} {msg}"
    
# this is the main function
def main():
    if len(sys.argv) !=4:
        print("python client.py <host> <port> <file>")
        return
    host =sys.argv[1]
    port =int(sys.argv[2])
    file =sys.argv[3]
    
    # check if the input file exists
    if not os.path.exists(file):
        print("file not found")
        return
    
    # creat a socket connect and connet to the server
    s = socket.socket()
    s.connect((host, port))
    with open(file) as f:  # open the file and process each line
        for line in f:
            msg = make(line)
            if msg:
                s.sendall(msg.encode())  # send the message to server
                reply = s.recv(1024)  # receive response
                print(f"{line.strip()}: {reply.decode()}")
            else:
                print(f"bad request: {line.strip()}")
    s.close()


# run the main function
if __name__ == "__main__":
    main()
   