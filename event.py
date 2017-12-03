import pprint
import eventful_api_implem_perso as eventful

DEFAULT_IMG_URL = "http://www.bloggingtips.com/wp-content/uploads/2014/12/Event-Blogging-Strategies.jpg"
API_KEY_EVENTFULL = 'xxML6LLwcZLP7GfH'


class EventAPI(object):
    def __init__(self):
        self._api = eventful.API(API_KEY_EVENTFULL)

    def getEventImg(self, idEvent):
        try:
            if idEvent is None:
                return DEFAULT_IMG_URL
            ret = self._api.call('/events/get', id=idEvent)
            if ret is None:
                return
            if "images" in ret:
                img = ret["images"]
                if img is None:
                    return
                pprint.pprint(ret["images"]["image"])
                return ret["images"]["image"]["medium"]["url"]
            return DEFAULT_IMG_URL
        except:
            return DEFAULT_IMG_URL

    def getEventByLocation(self, location, nbElem='5', typeOfEvent=None):
        if typeOfEvent is not None:
            events = self._api.call('/events/search', l=location, page_size=nbElem, q=typeOfEvent, within=5)
        else:
            events = self._api.call('/events/search', l=location, page_size=nbElem, within=5)
        out = []

        if events is None:
            return None
        if events['events'] is None:
            return None
        if events['events']['event'] is None:
            return None
        for event in events['events']['event']:
            out.append(event)
        return out

    def getEvent(self, cityOfEvent, nbElem='5', typeOfEvent=None):
        if typeOfEvent is not None:
            events = self._api.call('/events/search', l=cityOfEvent, page_size=nbElem, q=typeOfEvent)
        else:
            events = self._api.call('/events/search', l=cityOfEvent, page_size=nbElem)
        out = []

        if events is None:
            return None
        if events['events'] is None:
            return None
        if events['events']['event'] is None:
            return None
        for event in events['events']['event']:
            out.append(event)
        return out

    def getListCategories(self):
        cat = self._api.call('categories/list')
        for c in cat["category"]:
            print(c['id'])

    def parseTitle(self, events):
        out = ""
        if events is None:
            return None
        for event in events:
            out += event['title'] + "\n"
        return out

    def formatEvent(self, eventToFormat):
        eventName = eventToFormat['title']
        eventDate = eventToFormat['start_time']
        eventLink = eventToFormat['venue_url']
        eventAdress = eventToFormat['venue_address']
        eventCity = eventToFormat['city_name']
        eventId = eventToFormat['id']
        return eventName, eventDate, eventLink, eventAdress, eventCity, eventId


if __name__ == '__main__':
    ev = EventAPI()
    tmp = ev.getEvent("Paris")
    for x in tmp:
        eventName, eventDate, eventLink, eventAdress, eventCity, eventId = ev.formatEvent(x)
        print(eventName, ev.getEventImg(eventId))
