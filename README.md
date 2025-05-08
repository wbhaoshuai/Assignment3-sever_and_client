# Tuple space server-client system
## Project Introduction
This project implements a simple tuple space (represented by a list of tuples) server-client system based on Python. 
The client can read requests from specific files, convert them into a fixed format, and then send operation requests such as PUT, GET, READ to the server. 
The server accepts and processes requests, then performs operations on tuples in the tuple space, and finally sends a fixed response to the client. At the same time, the server will record operation statistics and data information, and regularly output them. 
## Main document description
- 'server.py': Implement the core logic of a tuple space server, handle client requests, perform operations, and periodically output statistical information.
- 'client.py': Implement client logic, read operation instructions from files, send them to the server, and process responses.
## Environmental requirements
- Python environment
## Usage steps
### Prepare client files
- There are 10 text files in the project directory, named in the format 'client i. txt' (where 'i' is a positive integer). Each file contains operation instructions in the following format:  
PUT key1 value1  
GET key1  
READ key1
### Start the server
Open the terminal, navigate to the project directory, and run the following command to start the server:  
python server.py  
After the server starts, it will listen on port 51234 of localhost and wait for the client to connect.
### Start client
In another terminal, navigate to the project directory and run the following command to start the client:  
python client.py  
The client will create 10 threads, each corresponding to a client file, to read operation instructions from the file and send them to the server. The client will display the results of each operation.
### Stop the server and client
After the client completes all operations, it will automatically send a Stop message to the server. This can disconnect the connection between the server and the client
## Reminder
1. Please ensure that the your test files are in the same folder as the Python code first.
2. After opening the code, please run server.py first, then run client.py.
3. If you want to connect the server to other clients, please ensure that the format of the message sent and the port number are correct. And please ensure that after the client reads and sends all requests, a 'Stop' request needs to be sent to end the connection between the server and the client.
4. After the server is started, it will continue to run to answer client link requests and create threads to process them.
5. The content of each operation (the sum of keys and values) cannot exceed 970 characters in length, otherwise the client will ignore the operation.
