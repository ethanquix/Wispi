import keywords
from app import printReturnKW
from fbmq import Template
import logging
import alog

import urllib.parse

import event
import searchImage

import arrow

ev = event.EventAPI()
anal = keywords.WispiKeywords()


def addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity):
    alog.warning("Entering in add template")
    alog.info("Event address: " + eventAdress)
    urlOfAddress = "http://wispi.tk"
    try:
        urlOfAddress = "https://www.google.fr/maps/place/" + urllib.parse.quote(eventAdress)
    except Exception as e:
        alog.error("Cant parse adress " + eventAdress + str(e))

    return Template.GenericElement(eventName,
                                   subtitle=arrow.get(eventDate).humanize(),
                                   item_url=eventLink,
                                   # image_url=searchImage.getImageUrl(eventName + " " + eventCity),
                                   image_url="https://images.pexels.com/photos/5156/people-eiffel-tower-lights-night.jpg",
                                   buttons=[
                                       Template.ButtonWeb("Open in Map", urlOfAddress),
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
