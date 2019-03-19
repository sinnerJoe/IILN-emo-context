
import nltk
import math
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from itertools import chain


def get_wordnet_pos(pos):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(pos[0], wordnet.NOUN)


def find_best_synonyms(reply):
    sentence = 
    for wordObj in reply:
        synonyms = wordnet.synsets(wordObj["lemma"])
        for i in synonyms:
            print("------", i, "-------")
            print(i.definition())
            print(i.lemma_names())

def lesk(word, sentence):
    context = set(sentence)
    max_overlap = 0
    synonyms = wordnet.synsets(word)
    best_sense = None if len(synonyms) == 0 else synonyms[0]
    if len(synonyms) <= 1:
        return best_sense
    


def populate_synonym_db(wordObj, database: dict, emotion):
    synonyms = wordnet.synsets(wordObj["lemma"])
    
    lemmas = chain.from_iterable([word.lemma_names() for word in synonyms])
    wordObj["synonyms"] = list(set(lemmas))
    add_lemma(wordObj["lemma"], wordObj["synonyms"], database, emotion)


def add_lemma(lemma, synonyms, database: dict, emotion):
    weight = 1
    if lemma in database:
            if isinstance(database[lemma], str):
                weight = 0.8
                counter = database[database[lemma]]
            else:
                counter = database[lemma]
    else:
        presentSynonyms = [
            synonym for synonym in synonyms if synonym in database]
        if len(presentSynonyms) == 0:
            counter = {
                "angry": 0,
                "others": 0,
                "happy": 0,
                "sad": 0
            }
            database[lemma] = counter
        else:
            weight = 0.8
            counter = None
            while counter == None:
                foundSyns = []
                for syn in presentSynonyms:
                    if not isinstance(database[syn], str):
                        counter = database[syn]
                        database[lemma] = syn
                        break
                    foundSyns.append(database[syn])
                presentSynonyms = foundSyns

    counter[emotion] += weight
