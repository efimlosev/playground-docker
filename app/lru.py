import json
from enum import Enum
import requests
from http import HTTPStatus
import time
from redis import Redis, exceptions
from os import environ
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']


class OxfordDictionary:

    def search(self, word):
        # for more information on how to install requests
        # http://docs.python-requests.org/en/master/user/install/#install

        app_id = environ['APP_ID']
        app_key = environ['APP_KEY']

        language = 'en-us'
        word_id = word
        fields = 'definitions,examples'
        strictMatch = 'true'

        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;

        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key, 'Accept': 'application/json'})
        if r.status_code != HTTPStatus.OK:
            raise KeyError(f"Cannot find {word} {r.status_code}")
        # print("code {}\n".format(r.status_code))
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
                        ["examples"][0]["text"]}

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


class ReusableForm(Form):
    name = StringField('Word:', validators=[validators.input_required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    dictionary = Dictionary()

    form = ReusableForm(request.form)


    if request.method == 'POST':
        word = request.form['name']

    if form.validate():
        # Save the comment here.
        try:
            entry, source, duration = dictionary.search(word)
            flash(entry)
            flash(f"Found in {source}")
            flash(f"Duration  {duration}")
        except Exception as e:
            flash(f"Error when searching: {str(e)}\n")
    else:
        flash('All the form fields are required. ')

    return render_template('hello.html', form=form)


if __name__ == '__main__':
    # main()
    app.run(host='0.0.0.0', port=5000)
    # d = OxfordDictionary()
    # d.search("cat")
