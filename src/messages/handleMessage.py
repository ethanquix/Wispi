import urllib.parse

import alog
import arrow
from fbmq import Template

from app import printReturnKW
from data_collect import searchImage
from eventManager import event
from interests import tastes
from messages import keywords

from pymongo import MongoClient

ev = event.EventAPI()
anal = keywords.WispiKeywords()

client = MongoClient("localhost")
db = client.wispi


def addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity, idEvent):
    if eventAdress is None:
        return
    urlOfAddress = "http://wispi.tk"
    try:
        urlOfAddress = "https://www.google.fr/maps/place/" + urllib.parse.quote(eventAdress)
    except Exception as e:
        alog.error("Cant parse adress " + eventAdress + str(e))

    return Template.GenericElement(eventName,
                                   subtitle=arrow.get(eventDate).humanize(),
                                   item_url=eventLink,
                                   image_url=searchImage.getImageUrl(eventName),
                                   buttons=[
                                       Template.ButtonWeb("Open in Map", urlOfAddress),
                                       Template.ButtonWeb("Open Event", eventLink),
                                       Template.ButtonShare()
                                   ])


def handleLocation(user, loc, page):
    tList = []
    getEv = ev.getEventByLocation(loc, '5')
    if getEv is None:
        page.send(user, "Désolé il n'y a aucun evenement a cet endroit")
        return
    for tmp in getEv:
        eventName, eventDate, eventLink, eventAdress, eventCity, eventId = ev.formatEvent(tmp)
        if eventAdress is not None:
            tList.append(addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity, eventId))
    page.send(user, Template.Generic(tList))


def sendHelp(user, page):
    out = "Wispi Bot:\n--------\n* Evenements:\n" \
          "Rechercher un evènement: 'Trouve moi quelquechose a Paris | Nice'\n" \
          "Rechercher par thème: 'Trouve moi moi un concert a Paris\n" \
          "* Centres d'intérets:\n" \
          "Lister: list\n" \
          "Ajouter: ajoute business\n" \
          "Supprimer: supprime business\n"
    page.send(user, out)


def handle(user, msg, page):
    helpMsg = ["help", "aide"]
    for h in helpMsg:
        if h in msg:
            return sendHelp(user, page)

    typeOfHandle, theme, city = anal.analyzeSentence(msg)

    if typeOfHandle == keywords.SentenceType.SEARCH_EVENT:
        printReturnKW(city, theme)
        out = "Veuillez reformuler"
        tList = []
        if city is None:
            out = "Veuillez spécifier une ville"
            page.send(user, out)
            return
        else:

            if theme is not None:
                db.tastes.update_one({'userId': user}, {'$addToSet': {'previsionTheme': theme, 'previsionCity': city}}, True)

            getEv = ev.getEvent(city, '5', theme)
            if getEv is None:
                page.send(user, "Désolé il n'y a aucun evenement a cet endroit")
                return
            for tmp in getEv:
                eventName, eventDate, eventLink, eventAdress, eventCity, eventId = ev.formatEvent(tmp)
                if eventAdress is not None:
                    tList.append(addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity, eventId))
                else:
                    tList.append(addTemplate(eventName, eventDate, eventLink, city, city, eventId))
            r = page.send(user, Template.Generic(tList))
            if not r.ok:
                page.send(user, "Il y a eu un problème lors de l'envoi du message")

    elif typeOfHandle == keywords.SentenceType.GET_TASTE:
        page.send(user, tastes.getTastes(user))

    elif typeOfHandle == keywords.SentenceType.ADD_TASTE:
        page.send(user, tastes.addTaste(user, theme))

    elif typeOfHandle == keywords.SentenceType.DELETE_TASTE:
        page.send(user, tastes.removeTaste(user, theme))
