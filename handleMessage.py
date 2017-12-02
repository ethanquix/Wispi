import keywords
from app import printReturnKW
from fbmq import Template
import logging

import urllib.parse

import event
import searchImage

ev = event.EventAPI()
anal = keywords.WispiKeywords()


def addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity):
    logging.info("Event address: " + eventAdress)
    return Template.GenericElement(eventName,
                                   subtitle=eventDate,
                                   item_url=eventLink,
                                   image_url=searchImage.getImageUrl(eventName + " " + eventCity),
                                   buttons=[
                                       Template.ButtonWeb("Open in Map",
                                                          "https://www.google.fr/maps/place/" + urllib.parse.quote(eventAdress)),
                                       Template.ButtonWeb("Open Event", eventLink),
                                       Template.ButtonShare()
                                   ])


def handle(user, msg, page):
    theme, city = anal.analyzeSentence(msg)
    printReturnKW(city, theme)
    out = "Veuillez reformuler"

    tList = []

    if city is None:
        out = "Veuillez spécifier une ville"

    if city is None and theme is None:
        page.send(user, out)
        return
    else:
        getEv = ev.getEvent(city, '5', theme)
        for tmp in getEv:
            eventName, eventDate, eventLink, eventAdress, eventCity = ev.formatEvent(tmp)
            tList.append(addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity))
        page.send(user, Template.Generic(tList))
