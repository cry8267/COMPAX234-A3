
# COMPX234-A3: Tuple Space Client/Server System

##  Project Introduction

This is the implementation of COMPX234 Assignment 3, which builds a multi-threaded client server system that uses TCP socket communication and supports basic operations for sharing tuple space: PUT, GET, and READ. The server can process requests from multiple clients simultaneously and output statistical information every 10 seconds.


##  file description

|   file name     | discription                             |
|----------------|----------------------------------|
| `server.py`     | Start the server, listen for client connections, and process requests |
| `client.py`     |   Read instruction files and communicate with the server       |
| `tuple_space.py`| Implement the TupleSpace class to provide data read and write operations |
| `*.txt`         | Client request instruction text |

##  Protocol Description
Each client request must be sent to the server in the following format:

```
NNN R key        # READ 
NNN G key        # GET 
NNN P key value  # PUT 
```

- `NNN` It is a 3-digit decimal number representing the length of the entire message (including commands and spaces)
- `key` and `value` For any string (total length limit<999 characters)

##  Example Request

```
012 G apple
010 R x
025 P name Alice Smith
```

##  Example response

```
024 OK (apple, red) removed
020 OK (name, Alice) added
024 ERR name already exists
```

---

##  Instructions for use
##  Start the server


```bash
python server.py 51234
```

- The port number (51234) should be within the range of 50000~59999

##  Start the client

```bash
python client.py 127.0.0.1 51234 test-workload\test-workload\client_1.txt
```

- `test-workload\test-workload\client_1.txt` 文件中包含指令，如：

```
GET silvertip
GET michel_montaigne
PUT hard_liquor an alcoholic beverage that is distilled rather than fermented
PUT al_aqabah Jordan's port; located in southwestern Jordan on the Gulf of Aqaba
READ mulberry_tree
```

---

## The server outputs statistical information every 10 seconds ：

```
Tuples: 0, Avg Tuple Size: 0.00, Avg Key Size: 0.00, Avg Value Size: 0.00, Clients: 0, Ops: 0, READ: 0, GET: 0, PUT: 0, ERR: 0
Tuples: 44, Avg Tuple Size: 75.95, Avg Key Size: 11.05, Avg Value Size: 64.91, Clients: 1, Ops: 38066, READ: 6336, GET: 6392, PUT: 6436, ERR: 18902
Tuples: 39, Avg Tuple Size: 76.00, Avg Key Size: 11.62, Avg Value Size: 64.38, Clients: 1, Ops: 76238, READ: 12710, GET: 12747, PUT: 12786, ERR: 37995
```

---

##  Technical Details

-Multi threading support: Each client connection is handled by an independent thread
-* * Thread safety * *: Use ` threading Lock() ` protects shared data
-* * Complete protocol support * *: Message length and format fully comply with the requirements of the title
-* * Error Handling * *: Illegal formats and duplicate keys can both return error responses correctly

---

##  Testing suggestions

1. First run 'server. py' (set port)
2. Run multiple instances of 'client. py' using different input files
3. Check if the client output is consistent with the server statistics

---

##  Author's note

-The project is written in pure Python and does not require external libraries
-Clear structure, easy to expand and test
-Complies with all functions and protocol specifications of COMPX234-A3