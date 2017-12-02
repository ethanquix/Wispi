import eventful_api_implem_perso as eventful

API_KEY_EVENTFULL = 'xxML6LLwcZLP7GfH'


class EventAPI(object):
    def __init__(self):
        self._api = eventful.API(API_KEY_EVENTFULL)

    def getEvent(self, cityOfEvent, nbElem='50', typeOfEvent=None):
        if typeOfEvent is not None:
            events = self._api.call('/events/search', l=cityOfEvent, page_size=nbElem, q=typeOfEvent)
        else:
            events = self._api.call('/events/search', l=cityOfEvent, page_size=nbElem)
        for event in events['events']['event']:
            print(event)
            return 0
            # print("%s at %s" % (event['title'], event['venue_name']))

        return events

    def getListCategories(self):
        cat = self._api.call('categories/list')
        for c in cat["category"]:
            print(c['id'])

    def parseTitle(self, events):
        out = ""
        if events is None:
            return None
        for event in events['events']['event']:
            out += event['title'] + "\n"
        return out

    def formatEvent(self, eventToFormat):
        eventName = eventToFormat['title']
        eventDate = eventToFormat['start_time']
        eventLink = eventToFormat['venue_url']
        eventAdress = eventToFormat['venue_address']
        eventCity = eventToFormat['city_name']
        return eventName, eventDate, eventLink, eventAdress, eventCity


if __name__ == '__main__':
    ev = EventAPI()
    # ev.getListCategories()
    ev.getEvent("Nice")
