# -*- coding: utf-8 -*-

import _thread
import logging
import os
import sys
import traceback

import time

import alog
import messages.keywords
from fbmq import Page, Attachment
from flask import Flask, request

import config
from eventManager import event
from messages import handleMessage

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

BANNED_USERNAME = ["1492060920843672"]

GET_STARTED = "GET_STARTED"

page = Page(config.PAGE_ACCESS_TOKEN)

ev = event.EventAPI()
anal = messages.keywords.WispiKeywords()

from datadog import statsd
from datadog import initialize

options = {
    'api_key': config.DATADOG_API_KEY,
    'app_key': config.DATADOG_APP_KEY
}

initialize(**options)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == config.VERIFY_TOKEN:
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
        data = request.get_json()

        if data["object"] == "page":
            for entry in data["entry"]:
                if "messaging" not in entry:
                    continue
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):

                        statsd.increment('message.received')

                        if "is_echo" in messaging_event["message"]:
                            statsd.increment('message.echo')

                            continue
                        sender_id = messaging_event["sender"]["id"]

                        if "attachments" in messaging_event["message"]:

                            print("[WISPI_BOT] Received new location...")
                            time.sleep(0.5)
                            print("[WISPI_BOT] Analyzing", end="")
                            time.sleep(0.2)
                            print(".", end="")
                            time.sleep(0.2)
                            print(".", end="")
                            time.sleep(0.2)
                            print(".")
                            statsd.increment('message.location')

                            coord = ""
                            if "payload" in messaging_event["message"]["attachments"][0]:
                                payload = messaging_event["message"]["attachments"][0]["payload"]
                                if "coordinates" in payload:
                                    coord = str(payload["coordinates"]["lat"]) + "," + str(
                                        payload["coordinates"]["long"])
                                    alog.warning("Received coordinates: " + coord)
                                else:
                                    continue
                            else:
                                continue

                            if sender_id not in BANNED_USERNAME:
                                _thread.start_new_thread(handleMessage.handleLocation, (sender_id, coord, page))
                            else:
                                alog.warning("SENDER ID IN BANNED USERNAME")

                            continue

                        message_text = messaging_event["message"]["text"]

                        print("[WISPI_BOT] Received new message...")
                        time.sleep(0.5)
                        print("[WISPI_BOT] Analyzing message", end="")
                        time.sleep(0.2)
                        print(".", end="")
                        time.sleep(0.2)
                        print(".", end="")
                        time.sleep(0.2)
                        print(".")
                        print("[WISPI_BOT] Found sender ! ", messaging_event["sender"]["id"])

                        if sender_id not in BANNED_USERNAME:
                            _thread.start_new_thread(handleMessage.handle, (sender_id, message_text, page))
                        else:
                            alog.warning("SENDER ID IN BANNED USERNAME")

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):

                        print("[WISPI_BOT] Received new message...")
                        time.sleep(0.5)
                        print("[WISPI_BOT] Analyzing message", end="")
                        time.sleep(0.2)
                        print(".", end="")
                        time.sleep(0.2)
                        print(".", end="")
                        time.sleep(0.2)
                        print(".")
                        print("[WISPI_BOT] Found sender ! ", messaging_event["sender"]["id"])

                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["postback"]["payload"]

                        if message_text == GET_STARTED:
                            statsd.increment('message.get_started')
                            page.send(sender_id, "Hello je suis Wispi ton compagnon de voyage\n je suis la pour te suggérer des activitées :)\n\nTape aide pour plus d'infos")
                            continue

                        if sender_id not in BANNED_USERNAME:
                            _thread.start_new_thread(handleMessage.handle, (sender_id, message_text, page))
                        else:
                            alog.warning("SENDER ID IN BANNED USERNAME")
    except:
        print("Exception in user code:")
        print("-" * 20)
        traceback.print_exc(file=sys.stdout)
        print("-" * 20)
        page.send(sender_id, "Il y a eu une erreur désolé")

    return "ok", 200


if __name__ == '__main__':
    page.show_starting_button(GET_STARTED)
    # page.hide_greeting()
    page.greeting("Hello je suis wispi ton compagnon de voyage\n je suis la pour te suggérer des activitées :)")
    page.hide_persistent_menu()
    app.run(port=8042, debug=True)
