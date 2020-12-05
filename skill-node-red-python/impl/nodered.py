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
import manage
import socket
import json

@skill.intent_handler('TEAM_36_RED_NODE')
def handler(input_request: str) -> Response:
    print('computing...')
    request_client = "Magenta7828a"

    print("Connected client: ", manage.current_client)
    print("Input request: ", input_request)

    message = {"message": input_request, "to": request_client}

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
