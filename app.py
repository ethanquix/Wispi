# -*- coding: utf-8 -*-

import os
import sys
import json
from datetime import datetime

import event

import requests
from flask import Flask, request

app = Flask(__name__)

ev = event.EventAPI()


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    try:
        # endpoint for processing incoming messaging events
        data = request.get_json()
        log(data)  # you may not want to log every incoming message in production, but it's good for testing
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                        message_text = messaging_event["message"]["text"]  # the message's text

                        # We get messages
                        getEv = ev.getEvent(message_text, '5')
                        out = ""
                        for x in getEv['events']['event']:
                            out += x['title'] + "\n"

                        send_message(sender_id, "Voici les evenement: " + out)

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
                        # send_message(sender_id, "t'a recu mon message... trop cool !")

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
    except Exception as e:
        print("EXCEPTION")
        print(str(e))

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log("Status code != 200")
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):
    print(msg)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(port=8042, debug=True)
