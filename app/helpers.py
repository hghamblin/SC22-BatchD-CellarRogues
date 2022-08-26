from better_profanity import profanity
import os
from random import choice, randint
from difflib import SequenceMatcher
from datetime import datetime as dt
# import json
import csv

months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
id_chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ1234567890"


def fix_headline(headline):
    return censor(capitalize(single_headline(headline)))


def single_headline(headline):
    return headline.split('\n')[0]


articles = ['a', 'an', 'of', 'the', 'is', 'for', 'in', 'at', 'to']
allCaps = ["dui"]


def capitalize(headline):
    return ' '.join([word.lower() if word.lower() in articles and i > 0 else (word.upper() if word.lower() in allCaps else (word[0] + word[1:].capitalize() if len(word) > 0 and ('"' == word[0] or "'" == word[0]) else word.capitalize())) for i, word in enumerate(headline.split(' '))])


def censor(headline):
    return profanity.censor(headline)


def get_mugshot(headline):
    image_dict = {
        "man": os.listdir("static/img/mugshots/man"),
        "woman": os.listdir("static/img/mugshots/woman")
    }

    if headline[:13] == "Florida Woman":
        return "../static/img/mugshots/woman/" + choice(image_dict["woman"])
    elif headline[:11] == "Florida Man":
        return "../static/img/mugshots/man/" + choice(image_dict["man"])
    else:
        key = choice(image_dict)
        return "../static/img/mugshots/" + key + '/' + choice(image_dict[key])

def get_date():
    year = dt.today().year
    return f'{choice(months)} {randint(1, 28)}, {randint(year + 1, year + 1500)}'

def add_headline_txt(headline):
    headline_id = 1
    while os.path.exists(f'./headlines/{headline_id}.txt'):
        headline_id += 1
    with open(f'./headlines/{headline_id}.txt', 'w') as f:
        f.write('\n'.join([str(i) for i in headline]))
    return headline_id