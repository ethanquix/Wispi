import json
import os

from eventManager import event

ev = event.EventAPI()

DATA_CITIES_NAME = os.path.join(os.path.dirname(__file__), "../data/cities.json")


class SentenceType(enumerate):
    SEARCH_EVENT = 0
    GET_TASTE = 1
    ADD_TASTE = 2
    DELETE_TASTE = 3


class WispiKeywords(object):
    def __init__(self):
        self.kwords = self.fillKwords()
        self.cities = self.parseCities()
        self.addTaste = ["ajoute"]
        self.removeTaste = ["supprime", "enleve", "enlève"]
        self.getTaste = ["list", "liste"]

    def fillKwords(self):
        self.kwords = dict()
        self.kwords["music"] = ["concert", "concerts", "musique", "artiste", "artistes", "show", "chanteur",
                                "chanteurs", "chanteuses", "chanteuse", "groupe", "groupes", "musical", "musiques"]
        self.kwords["learning_education"] = ["musée", "musee", "musés", "muses", "musées", "monuments", "monument",
                                             "chateau",
                                             "culture", "cultures", "culturels", "culturel"]

        return self.kwords

    def parseCities(self):
        out = dict()
        f = open(DATA_CITIES_NAME, "r")
        content = json.load(f)
        for tmp in content:
            tmpName = tmp["name"].lower()
            if len(tmpName) > 3:
                out[tmp["name"].lower()] = True

        return out

    def citiesExist(self, citie):
        if citie.lower() in self.cities:
            return citie
        return None

    def citiesExistLONG(self, sentence):
        for tmp in self.cities:
            if tmp in sentence.lower():
                return tmp
        return None

    def wordIsTopic(self, word):
        for topic, value in self.kwords.items():
            if word.lower() in value:
                return topic
        return None

    def tasteEpur(self, sentence, l):
        for x in l:
            sentence = sentence.replace(x, "")
        tmp = sentence.split(" ")
        return tmp[1]

    def isTaste(self, sentence):
        for x in sentence.split(" "):
            if x.lower() in self.addTaste:
                return SentenceType.ADD_TASTE, self.tasteEpur(sentence.lower(), self.addTaste)
            if x.lower() in self.removeTaste:
                return SentenceType.DELETE_TASTE, self.tasteEpur(sentence.lower(), self.removeTaste)
            if x.lower() in self.getTaste:
                return SentenceType.GET_TASTE, ""
        return None, None

    def analyzeSentence(self, sentence):
        x, s = self.isTaste(sentence)
        if x is not None:
            return x, s, None

        theme = None
        city = None
        for word in sentence.split(" "):
            if theme is None:
                theme = self.wordIsTopic(word)
            if city is None:
                city = self.citiesExist(word)
        if city is None:
            city = self.citiesExistLONG(sentence)
        return SentenceType.SEARCH_EVENT, theme, city


if __name__ == '__main__':
    w = WispiKeywords()
    print(w.analyzeSentence("Je cherche un concert a Paris"))
    print(w.analyzeSentence("Je cherche un artiste a londres"))
    print(w.analyzeSentence("Je cherche un musée a nioiioioidoiroriroriorice"))
    print(w.analyzeSentence("Je cherche un truc musical a Nice"))
    print(w.analyzeSentence("qsdfghjkjhfxxcvbnjjsryuiknbv4584234"))
    print("Tests tastes")
    print(w.analyzeSentence("list moi mes interets"))
    print(w.analyzeSentence("ajoute business"))
    print(w.analyzeSentence("supprime sport"))
    print(w.isTaste("list"))
