import keywords
from app import printReturnKW
from fbmq import Template

import urllib.parse

import event
import searchImage

ev = event.EventAPI()
anal = keywords.WispiKeywords()


def addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity):
    return Template.GenericElement(eventName,
                                subtitle=eventDate,
                                item_url=eventLink,
                                image_url=searchImage.getImageUrl(eventName + " " + eventCity),
                                buttons=[Template.ButtonWeb("Open in Map", "https://www.google.fr/maps/place/" + urllib.parse.quote(eventAdress))])


def handle(user, msg, page):
    theme, city = anal.analyzeSentence(msg)
    printReturnKW(city, theme)
    out = "Veuillez reformuler"

    tList = []

    if city is None:
        out = "Veuillez spécifier une ville"

    if city is None and theme is None:
        page.send(user, out)
        return "ok", 200
    else:
        getEv = ev.getEvent(city, '5', theme)
        print(getEv)
        for tmp in getEv:
            tList.append(ev.formatEvent(tmp))
    page.send(user, Template.Generic(tList))
