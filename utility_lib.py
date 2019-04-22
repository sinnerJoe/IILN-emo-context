
import nltk
import math
import json
from nltk.wsd import lesk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from itertools import chain
import gensim
from gensim import corpora 
import re
import pickle

nltk.download("stopwords")

stop_words = set(nltk.corpus.stopwords.words('english'))


def reduce_repeated_chars(word):
    new_word = ""
    i=0
    while i < len(word):
        reps = 1
        for j in range(i+1, len(word)):
            if word[i] == word[j]:
                reps += 1
            else:
                break
        if reps == 2:
            new_word += word[i:i+2]
        else: 
            new_word += word[i]
        i+=reps    
    return new_word

def get_wordnet_pos(pos):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(pos[0], wordnet.NOUN)


def best_synonym(replies):
    words = tuple([i for reply in replies for i in reply])
    words_str = tuple([i["lemma"] for i in words])
    # print(words_str)
    for i in range(0, len(words)):
        # print(words[i])
        try:
            best_syn = lesk(words_str, words_str[i], get_wordnet_pos(words[i]["pos"]))
            # print(best_syn)
            lemma_names = best_syn.lemma_names()
            if isinstance(lemma_names, list):
                words[i]["best_syn"] = lemma_names[0]
                 
        except:
            print("Except ", words_str[i])

words_without_synononyms = 0
def populate_synonym_db(wordObj, database: dict, emotion):
    global words_without_synononyms
    synonyms = wordnet.synsets(wordObj["lemma"])
    
    lemmas = chain.from_iterable([word.lemma_names() for word in synonyms])
    wordObj["synonyms"] = list(set(lemmas))
    if len(wordObj["synonyms"]) == 0:
        words_without_synononyms += 1
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



frequent_words = { 
    "a", "an", "he", "she", "it", "you", "be", "the", "i", "u", "to", "from", "of", "your", "his", "her"
    
}
total_frequent_words_removed = 0
def remove_frequent_words(replies):
    global total_frequent_words_removed 
    for reply in replies:
        i = 0
        while i < len(reply):
            if reply[i]["lemma"] in frequent_words or reply[i]["word"].lower() in frequent_words:
                del reply[i]
                total_frequent_words_removed += 1
            else:
                i+=1
capslock_detected = 0
def detect_capslock(line):
    global capslock_detected
    i = 0
    total = 0
    for reply in line["replies"]:
        total+=len(reply)
        for word in reply:
            if word["word"] == word["word"].upper():
                i+=1
    line["capslock"] = total / 3 < i
    if total / 3 < i:
        capslock_detected += 1
        
punct_re = re.compile(r"^(\?|\.|,| |\(|\))+$")


punctuation_removed = 0
def remove_punctuation(line):
    global punctuation_removed
    for reply in line["replies"]:
        i = 0
        while i < len(reply):
            if punct_re.match(reply[i]["word"]):
                del reply[i]
                punctuation_removed += 1
                # print("PUNCTUATION REMOVED")
            else:
                i+=1


def ner_words(line):
    replies = line["replies"]
    for reply in replies:
        tagged_words = [(wordObj["word"][0]+ wordObj["word"][1:], wordObj["pos"]) for wordObj in reply]
        ner_tags = nltk.ne_chunk(tagged_words)
        for chunk in ner_tags:
            if hasattr(chunk, "label") and chunk.label:
                name_value = ' '.join(child[0] for child in chunk.leaves())
                print("------------------------------------")
                print(name_value, chunk.label())
                for i in range(0, len(reply)):
                    wordObj = reply[i]
                    if wordObj['word'] == name_value:   
                        wordObj["ner_tag"] = chunk.label()
                        break


def reply_to_array_of_strings(reply):
    return list(map(lambda wordObj: wordObj["lemma"], reply))

total_words = 0
total_long_words = 0
total_tweet_nr = 0
dictionary = None
ldamodel = None
possible_topics = None
def calculate_dictionary(train_data):
    global total_words, total_long_words, total_tweet_nr
    global dictionary
    global ldamodel
    global possible_topics
    all_lines = [ flatten(map(reply_to_array_of_strings, i["replies"])) for i in train_data]
    all_words = []
    total_tweet_nr = len(train_data) * 3
    for line in all_lines:
        # all_words.append([word for word in line if len(word) > 4])
        sentence = []
        for word in line:
            total_words+=1
            if len(word) > 4:
                sentence.append(word)
                total_long_words += 1
        all_words.append(sentence)
    dictionary = corpora.Dictionary(all_words)
    all_words = [ dictionary.doc2bow(word) for word in all_words ]
    ldamodel = gensim.models.ldamodel.LdaModel(all_words, num_topics=20, id2word=dictionary, passes=15)
    possible_topics = ldamodel.print_topics(20)
    print("Possible topics", possible_topics)


def flatten(lst):
    res = []
    for el in lst:
        res.extend(el)
    return res

def lda_topic_detect(instance):
    global possible_topics
    words = list(map(reply_to_array_of_strings, instance["replies"]))
    new_doc = list(map(dictionary.doc2bow, words))
    # print(ldamodel.get_document_topics(new_doc))
    top_index = ldamodel.get_document_topics(new_doc)[0]
    # best_topics = sorted(key=(lambda el: el[0]), iterable=top_index, reverse=True)[:4]
    top_index.sort(key=lambda el: el[0], reverse=True)
    index, prob = top_index[0]
    instance["topics"] = possible_topics[index][1]

def print_metrics():
    global total_frequent_words_removed, total_words, total_tweet_nr, punctuation_removed, capslock_detected, total_long_words
    global words_without_synononyms, capslock_detected
    print("Punctuation removed: ", punctuation_removed)
    print("Total frequent words removed: ", total_frequent_words_removed)
    print("Total words: ", total_words)
    print("Total long words: ", total_long_words)
    print("Words without synonyms: ", words_without_synononyms)
    print("Capslock detected: ", capslock_detected)
    print("Total tweets: ", total_tweet_nr)