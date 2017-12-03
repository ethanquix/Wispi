# -*- coding: utf-8 -*-

import _thread
import logging
import os
import sys
import traceback

import alog
import messages.keywords
from fbmq import Page
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
    'app_key':config.DATADOG_APP_KEY
}

initialize(**options)

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
        data = request.get_json()

        if data["object"] == "page":
            for entry in data["entry"]:
                if "messaging" not in entry:
                    continue
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):

                        statsd.increment('messages_received')

                        if "is_echo" in messaging_event["message"]:

                            statsd.increment('messages_echo')

                            continue
                        sender_id = messaging_event["sender"]["id"]

                        if "attachments" in messaging_event["message"]:

                            statsd.increment('messages_location')

                            coord = ""
                            if "payload" in messaging_event["message"]["attachments"][0]:
                                payload = messaging_event["message"]["attachments"][0]["payload"]
                                if "coordinates" in payload:
                                    coord = str(payload["coordinates"]["lat"]) + "," + str(payload["coordinates"]["long"])
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
                        alog.warning("Received message: " + message_text)

                        if sender_id not in BANNED_USERNAME:
                            _thread.start_new_thread(handleMessage.handle, (sender_id, message_text, page))
                        else:
                            alog.warning("SENDER ID IN BANNED USERNAME")

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["postback"]["payload"]

                        alog.warning("Receive postback " + sender_id + " " + message_text)
                        if message_text == GET_STARTED:
                            statsd.increment('get_started')
                            handleMessage.sendHelp(sender_id, page)
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
    page.greeting("Bievenue sur Wispi !\n Le bot intelligent qui cherche des evenements pour toi !\nMais te previent aussi des evènements autour de toi pourraient t'intéresser")
    page.hide_persistent_menu()
    app.run(port=8042, debug=True)
