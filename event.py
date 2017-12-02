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
            print(event['title'])
            # print("%s at %s" % (event['title'], event['venue_name']))

        return events


ev = EventAPI()
ev.getEvent("Nice")
