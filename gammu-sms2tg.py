#!/usr/bin/env python3

import os
import sys
import requests

BOT_API_KEY = "super-secret-api-key"  # This is a telegram bot api token
# PhoneID - is a reference to relevant congig option of gammu-smsd for multi-phone set up
# In my case I have two modems connected and like to send them to different (personal) chats
CHAT_ID = {
    "PhoneID1": "chat-id-1",
    "PhoneID2": "chat-id-2"
}
SEND_TG_MESSAGE_ENDPOINT = "https://api.telegram.org/bot{key}/sendMessage"  # API URL for sending messages

#Message template to fill with meaningful info
NEW_SMS_RECIEVED_TEMPLATE = """\
New SMS recieved on your {phone}

FROM: {caller}
{message}\
"""

# TODO: No exception handling at all at this point. Do it!

# Method retrieves info from enviorement variables when called. DOes not work with old gammu versions (prev 1.32 or something like this)
def retrieve_sms():
    partsAmount = int(os.environ["DECODED_PARTS"])
    callerID = str(os.environ["SMS_1_NUMBER"])
    phoneID = str(os.environ["PHONE_ID"])
    text = ""

    # If 1 part message
    if partsAmount == 0:
        text = os.environ["SMS_1_TEXT"]
    # Otherwise - this is a long multipart message
    else:
        for i in range(1, partsAmount + 1):
            fragmentName = "DECODED_%d_TEXT" % i
            if fragmentName in os.environ:
                text = text + os.environ[fragmentName]

    return(phoneID, callerID, text)

# Method sends sms info and body to telegram
# TODO: add timestamp the message was recieved
def send_tg_message(phoneID, callerID, text):
    payload = {}
    payload["chat_id"] = CHAT_ID[phoneID]
    payload["text"] = NEW_SMS_RECIEVED_TEMPLATE.format(phone = phoneID, caller = callerID, message = text)
    requests.get(SEND_TG_MESSAGE_ENDPOINT.format(key = BOT_API_KEY), params = payload)

if __name__ == "__main__":
# Plain function calls.
# TODO: get info and fork immediately to send. It is best to return initial call ASAP not to miss any new messages coming during run
    phoneID, callerID, text = retrieve_sms()
    send_tg_message(phoneID, callerID, text)
