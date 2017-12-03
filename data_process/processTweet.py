import inspect
import os
import sys

from fbmq import Page, Template

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import secret
import handleMessage
import datetime

from pymongo import MongoClient

client = MongoClient("localhost")
db = client.wispi

page = Page(secret.PAGE_ACCESS_TOKEN)


def process(tweet):
    if "pitch" in tweet:
        cursor = db.tastes.find({'taste': 'business'})
        for document in cursor:
            tList = []

            page.send(document["userId"],
                      "Tu m'a dit aimer tout ce qui est en relation avec le commerce / business / entreprenariat n'est ce pas ? J'ai trouvé pour toi un évenement qui pourrait te plaire !")

            eventName, eventDate, eventLink, eventAdress, eventCity, eventId = "Pitch a l'EDHEC", datetime.datetime.now(), "wispi.tk", "393 Prom. des Anglais, 06200 Nice", "Nice", "0x4984987"
            tList.append(handleMessage.addTemplate(eventName, eventDate, eventLink, eventAdress, eventCity, eventId))
            r = page.send(document["userId"], Template.Generic(tList))
            if not r.ok:
                page.send(document["userId"], "Il y a eu un problème lors de l'envoi du message")


if __name__ == '__main__':
    process("pitch")
    # process(sys.argv[1])
