# -*- coding: utf-8 -*-

import json
import os
import sys
import traceback
import logging

import requests
from fbmq import Page
from flask import Flask, request

import event
import handleMessage
import keywords
import secret

app = Flask(__name__)

page = Page(secret.PAGE_ACCESS_TOKEN)

ev = event.EventAPI()
anal = keywords.WispiKeywords()


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


def printReturnKW(city, theme):
    if city is None and theme is not None:
        print("City is None, theme is: " + theme)
    elif theme is None and city is not None:
        print("Theme is None, city is: " + city)
    if city is not None and theme is not None:
        print("City is " + city + " theme is " + theme)
    if city is None and theme is None:
        print("City is " + "None" + " theme is " + "None")


@app.route('/', methods=['POST'])
def webhook():
    try:
        # endpoint for processing incoming messaging events
        data = request.get_json()
        # log(data)  # you may not want to log every incoming message in production, but it's good for testing
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("message"):  # someone sent us a message
                        sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                        message_text = messaging_event["message"]["text"]  # the message's text
                        logging.warning("Received message: " + message_text)

                        handleMessage.handle(sender_id, message_text, page)


                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
    except:
        print("Exception in user code:")
        print("-" * 20)
        traceback.print_exc(file=sys.stdout)
        print("-" * 20)

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
