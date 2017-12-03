from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost")
db = client.wispi


def getTastes(userId):
    out = "Tes centres d'interets:\n"
    result = db.tastes.find_one({'userId': userId})
    if result is None:
        return "Tu n'a pas encore spécifié de centre d'interets"
    if 'taste' not in result:
        return "Tu n'a pas encore spécifié de centre d'interets"
    for tmp in result['taste']:
        out += tmp + '\n'
    return out


def addTaste(userId, taste):
    db.tastes.update_one({'userId': userId}, {'$addToSet': {'taste': taste}}, True)
    return "Centre d'interet ajouté !"


def removeTaste(userId, taste):
    db.tastes.update_one({'userId': userId}, {'$pull': {'taste': taste}})
    return "Centre d'interet supprimé !"


if __name__ == '__main__':
    addTaste("TEST_USER", "music")
    addTaste("TEST_USER", "art")
    print(getTastes("TEST_USER"))
    removeTaste("TEST_USER", "art")
    getTastes("TEST_USER")
