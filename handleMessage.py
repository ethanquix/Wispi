import event
import keywords
from app import printReturnKW

ev = event.EventAPI()
anal = keywords.WispiKeywords()


def handle(user, msg, page):
    theme, city = anal.analyzeSentence(msg)
    printReturnKW(theme, city)
    out = "Veuillez reformuler"

    if city is None:
        out = "Veuillez spécifier une ville"

    if city is None and theme is None:
        page.send(user, out)
        return "ok", 200
    else:
        getEv = ev.getEvent(city, '5', theme)
        out = ev.parseTitle(getEv)

    page.send(user, out)
