#!/usr/bin/env python
import threading
import socket
import json
import time
import queue

print('starting...')

current_client = ""
client_message = queue.Queue()
client_response = ""


def start_server(c_msg, port=65432):
    global current_client, client_response
    print('initializing...')
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ensure that you can restart your server quickly when it terminates
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the client socket's TCP "well-known port" number
    well_known_port = port
    sock.bind(('', well_known_port))

    # Set the number of clients waiting for connection that can be queued
    sock.listen(5)

    # loop waiting for connections (terminate with Ctrl-C)
    try:
        while 1:
            new_socket, address = sock.accept()
            print("Connected from", address)
            # loop serving the new client
            while 1:
                try:
                    received_data = new_socket.recv(1024).decode("utf-8").strip('\n')
                    if received_data and "{\"id\":" in received_data:
                        data = json.loads(received_data)
                        print("Connected: ", data["id"])
                        current_client = data["id"]
                        new_socket.send(bytes(json.dumps({"message": "Connected as " + current_client}).encode('utf-8')))
                    if received_data and "{\"response\":" in received_data:
                        client_response = json.loads(received_data)["response"]
                        new_socket.send(bytes(json.dumps({"message": "OK", "to": current_client}).encode('utf-8')))
                    else:
                        msg = c_msg.get()
                        if msg != "":
                            print("Sending to client: ", msg)
                            new_socket.send(bytes(msg.encode("utf-8")))
                except ConnectionResetError:
                    new_socket.close()
                    print("Removing: ", current_client)
                    current_client = ""
                    print("Disconnected from", address)
    finally:
        sock.close()


def start_comm_server(c_msg, port=7979):
    global current_client, client_response

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ensure that you can restart your server quickly when it terminates
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the client socket's TCP "well-known port" number
    well_known_port = port
    sock.bind(('', well_known_port))

    # Set the number of clients waiting for connection that can be queued
    sock.listen(5)

    # loop waiting for connections (terminate with Ctrl-C)
    try:
        while 1:
            new_socket, address = sock.accept()
            print("Comm: Connected from", address)
            # loop serving the new client
            while 1:
                try:
                    received_data = new_socket.recv(1024).decode("utf-8").strip('\n')
                    if received_data and "{\"message\":" in received_data:
                        print("Comm: Message: ", received_data)
                        c_msg.put(received_data)

                        while client_response == "":
                            time.sleep(0.1)
                        new_socket.send(bytes(client_response.encode('utf-8')))
                except ConnectionResetError:
                    new_socket.close()
                    print("Comm: Disconnected from", address)
    finally:
        sock.close()


server_thread = threading.Thread(target=start_server, name="TCP Server", args=(client_message, 65432))
server_thread.start()
print('started')
comm_thread = threading.Thread(target=start_comm_server, name="Comm Server", args=(client_message, 7979))
comm_thread.start()
