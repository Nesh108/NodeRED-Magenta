#!/usr/bin/env python
from skill_sdk.manage import manage
import threading
import socket
import json

print('starting...')

current_client = "Magenta7828a"
client_message = "get temperature"
client_response = "temperature is 16C"


def start_server(port=65432):
    global current_client, client_message, client_response
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
                    if received_data and "{\"response\":" in received_data:
                        client_response = json.loads(received_data)["response"]
                    elif client_message != "":
                        new_socket.send(bytes(client_message.encode("utf-8")))
                        client_message = ""
                except ConnectionResetError:
                    new_socket.close()
                    print("Removing: ", current_client)
                    current_client = ""
                    print("Disconnected from", address)
    finally:
        sock.close()


server_thread = threading.Thread(target=start_server, name="TCP Server", daemon=True)
server_thread.start()
print('started')

manage()
