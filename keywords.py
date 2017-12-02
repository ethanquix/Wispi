import json
import event

ev = event.EventAPI()

DATA_CITIES_NAME = "data/cities.json"


class WispiKeywords(object):
    def __init__(self):
        self.kwords = self.fillKwords()
        self.cities = self.parseCities()

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

    def wordIsTopic(self, word):
        for topic, value in self.kwords.items():
            if word.lower() in value:
                return topic
        return None

    def analyzeSentence(self, sentence):
        theme = None
        city = None
        for word in sentence.split(" "):
            if theme is None:
                theme = self.wordIsTopic(word)
            if city is None:
                city = self.citiesExist(word)
        return theme, city


if __name__ == '__main__':
    w = WispiKeywords()
    print(w.citiesExist("Paris"))
    print(w.citiesExist("Londres"))
    print(w.citiesExist("London"))
    print(w.citiesExist("diroriori"))
    print(w.wordIsTopic("concert"))
    print(w.wordIsTopic("BONJOUR"))
    print(w.analyzeSentence("Je cherche un concert a Paris"))
    print(w.analyzeSentence("Je cherche un artiste a londres"))
    print(w.analyzeSentence("Je cherche un musée a nioiioioidoiroriroriorice"))
    print(w.analyzeSentence("Je cherche un truc musical a Nice"))
    print(w.analyzeSentence("qsdfghjkjhfxxcvbnjjsryuiknbv4584234"))