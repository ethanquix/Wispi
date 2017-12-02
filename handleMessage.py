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
        return

    page.send(user, Template.Generic([
            Template.GenericElement("rift",
                                    subtitle="Next-generation virtual reality",
                                    item_url="https://www.oculus.com/en-us/rift/",
                                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Google_Images_2015_logo.svg/1200px-Google_Images_2015_logo.svg.png",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                                        Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
                                        Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
                                    ]),
            Template.GenericElement("touch",
                                    subtitle="Your Hands, Now in VR",
                                    item_url="https://www.oculus.com/en-us/touch/",
                                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Google_Images_2015_logo.svg/1200px-Google_Images_2015_logo.svg.png",
                                    buttons=[
                                        Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                                        Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
                                        Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
                                    ])
        ]))
    # else:
    #     getEv = ev.getEvent(city, '5', theme)
    #     print(getEv)
    #     for tmp in getEv:
    #         tList.append(ev.formatEvent(tmp))
    # page.send(user, Template.Generic(tList))
