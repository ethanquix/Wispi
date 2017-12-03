import unittest

import data_collect.searchImage
import eventManager.event
import eventManager.eventful_api_implem_perso
import config


class EventFull(unittest.TestCase):
    def testGetEventInParis(self):
        ev = eventManager.event.EventAPI()
        tmp = ev.getEvent("Paris", '1', None)
        for x in tmp:
            eventName, eventDate, eventLink, eventAdress, eventCity, eventId = ev.formatEvent(x)
            self.assertTrue("paris" in eventCity.lower())

    def testGetCategories(self):
        ev = eventManager.event.EventAPI()
        tmp = ev.getListCategories()
        self.assertTrue("music" in tmp)


class DataCollect(unittest.TestCase):
    def testGetResult(self):
        self.assertNotEqual(data_collect.searchImage.getImageUrl("Shaka Ponk"), None)

    def testIsResultIMG(self):
        r = data_collect.searchImage.getImageUrl("Shaka Ponk")
        self.assertTrue(True)

    def testIsAnIMG(self):
        r = data_collect.searchImage.getImageUrl("Shaka Ponk")
        self.assertTrue(True)


class EventFullAPI(unittest.TestCase):
    def testWrongAPICall(self):
        api = eventManager.eventful_api_implem_perso.API(config.API_KEY_EVENTFULL)
        try:
            api.call("FALSE")
        except eventManager.eventful_api_implem_perso.APIError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def testGoodAPICall(self):
        api = eventManager.eventful_api_implem_perso.API(config.API_KEY_EVENTFULL)
        try:
            api.call('/events/search', l='Nice')
        except eventManager.eventful_api_implem_perso.APIError:
            self.assertTrue(False)
            return
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
