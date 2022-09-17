import json
from enum import Enum
import requests
from http import HTTPStatus
import time
from redis import Redis, exceptions
from os import environ

class OxfordDictionary:

    def search(self, word):
        # for more information on how to install requests
        # http://docs.python-requests.org/en/master/user/install/#install

        app_id = environ['APP_ID']
        app_key = environ['APP_KEY']
        # app_id = "bla"
        # app_key = "bla"

        language = 'en-us'
        word_id = word
        fields = 'definitions,examples'
        strictMatch = 'true'

        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;

        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key, 'Accept': 'application/json'})
        if r.status_code != HTTPStatus.OK:
            raise KeyError(f"Cannot find {word} {r.status_code} {r.request.headers}")
        print(f"{r.request.headers}")
        results_json = r.json()
        try:
            return {"word": results_json["results"][0]["id"],
                    "part_of_speech": results_json["results"][0]["lexicalEntries"][0]["lexicalCategory"][
                        "id"],
                    "definition":
                        results_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]
                        ["definitions"][0],
                    "example":
                        results_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]
                        ["examples"][0]["text"] }

        except:
            return {"word": results_json["results"][0]["id"],
                    "part_of_speech": results_json["results"][0]["lexicalEntries"][0]["lexicalCategory"][
                        "id"],
                    "definition":
                        results_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]
                        ["definitions"][0],
                        "example": None}


class DictionarySource(Enum):
    LOCAL = 1
    CACHE = 2
    OXFORD_ONLINE = 3

    def __str__(self):
        return self.name


class DictionaryEntryCache():
    def __init__(self, hostname="lru", port=6379):
        self.r = Redis(host=hostname, port=port)

    def add(self, word, entry):
        if not isinstance(entry, dict):
            raise ValueError
        try:
            self.r.set(word, json.dumps(entry))
        except exceptions.ConnectionError:
            pass

    def search(self, word):
        entry = ""
        try:
            entry = self.r.get(word)
        except exceptions.ConnectionError:
            pass
        if not entry:
            raise KeyError(f"Cannot find {word}")
        return json.loads(entry)


class Dictionary:
    def __init__(self, source=DictionarySource.OXFORD_ONLINE):
        # Local dictionary
        self.dictionary_source = source
        if source == DictionarySource.OXFORD_ONLINE:
            self.dictionary = OxfordDictionary()
        else:
            raise ValueError("Wrong source")
        self.dictionary_entry_cache = DictionaryEntryCache()

    def search(self, word):
        try:
            entry, duration = time_func(self.dictionary_entry_cache.search, word)
            print(DictionarySource.CACHE)
            return entry, DictionarySource.CACHE, duration
        except KeyError:
            # If there's a KeyError, we'll search in local dictionary.
            # This may also fail to find the word, at which point we give up
            # (so allow the exception to be raised)

            entry, duration = time_func(self.dictionary.search, word)

            self.dictionary_entry_cache.add(word, entry)
            return entry, self.dictionary_source, duration


def time_func(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    duration = time.perf_counter() - start
    return result, duration


def main():
    dictionary = Dictionary()
    while True:
        word = input("Enter a word to lookup: ")
        try:
            entry, source, duration = dictionary.search(word)
            print(f"{entry}\n(Found in {source} duration {duration})\n")
        except Exception as e:
            print(f"Error when searching: {str(e)}\n")





if __name__ == '__main__':
    o = OxfordDictionary()
    print(dir(o.search))
