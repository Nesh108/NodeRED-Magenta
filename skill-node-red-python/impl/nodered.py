#
# voice-skill-sdk
#
# (C) 2020, YOUR_NAME (YOUR COMPANY), Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#
#
from skill_sdk import skill, Response, tell
from skill_sdk.l10n import _
import time
import socket
import json


@skill.intent_handler('TEAM_36_NODE_RED')
def handler(nodered: str) -> Response:
    print('computing...')
    request_client = "Magenta7828a"

    print("Input request: ", nodered)

    message = {"message": nodered, "to": request_client}

    try:
        sock = socket.create_connection(('localhost', 7979))
        sock.sendall(bytes(json.dumps(message).encode('utf-8')))

        client_response = sock.recv(1024).decode("utf-8").strip('\n')
        print("received: ", client_response)
    finally:
        print("finished receiving")
        sock.close()

    response = tell(client_response)
    return response
