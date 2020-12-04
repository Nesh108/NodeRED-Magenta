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


@skill.intent_handler('TEAM_36_RED_NODE')
def handler(input_request: str) -> Response:
    print('computing...')
    request_client = "Magenta7828a"
   # input_request = "open windows"

    print("Connected client: ", manage.current_client)
    print("Input request: ", input_request)

    if manage.current_client == request_client:
        client_message = input_request
        while manage.client_response == "":
            time.sleep(0.1)
        response = tell(manage.client_response)
        return response
    else:
        response = tell("NodeClient is not connected")
        return response
