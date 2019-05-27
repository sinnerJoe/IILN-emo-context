#!/usr/bin/env python3
import nltk
from nltk import WordNetLemmatizer
import re
import json
from nltk.wsd import lesk
import utility_lib as utils
<<<<<<< HEAD
import utils as utlis2
import threading
#use gazeteer 
=======

 
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144
# nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')
<<<<<<< HEAD
print("new print")
parsed_lines = []
lemmatizer = WordNetLemmatizer()
with open("devsetwithlabels/dev.txt", encoding="utf8") as file:
=======


parsed_lines = []
lemmatizer = WordNetLemmatizer()
with open("devsetwithlabels/dev.txt", encoding="utf-8") as file:
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144
    replacer = re.compile("^d+\t([^\t]+)\t([^\t]+)\t([^\t]+)?[ \t](angry|sad|other|happy)$")
    next(file)
    for line in file:
        split = line.split("\t")
        del split[0]
        if '\n' in split[-1]:
            split[-1] = split[-1][:-1]
        parsed_lines.append(split)

<<<<<<< HEAD

def line_to_dict(line, sentiments):
    res = dict()
    pos_replies = map(nltk.pos_tag, line)
    # lemmatized_replies = [(w,p) for reply in pos_replies for w,p in reply if reply[0]]

    lemmatized_replies = []
    for reply in pos_replies:
        objs = list(map(lambda arg: { "pos": arg[1], "word": arg[0]}, reply))
        lemmatized_replies.append(objs)
    res["replies"] = lemmatized_replies
    # print(res["replies"])
    res["emotion"] = line[3][0]
    res["sentiments"] = sentiments
=======
# print(parsed_lines)


def line_to_dict(line):
    res = dict()
    replies = [utils.fix_spelling(reply) for reply in line[:-1]]
    replies = [utils.tokenize_emojis(reply) for reply in replies]
    pos_replies = map(nltk.pos_tag, replies)

    lemmatized_replies = []
    for reply in pos_replies:
        objs = list(map(lambda arg: { "pos": arg[1], "word": utils.reduce_lengthening(arg[0]) }, reply))
        lemmatized_replies.append(objs)
    res["replies"] = lemmatized_replies
    res["emotion"] = line[3][0]
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144
    return res

def lemmatize(line_dict):
    for reply in line_dict["replies"]:
        for wordObj in reply:
<<<<<<< HEAD
            # print(wordObj)
            wordObj["lemma"] = lemmatizer.lemmatize(wordObj["word"].lower(), utils.get_wordnet_pos(wordObj["pos"]))

save_lock = threading.Lock()
def requestEmotions(tweets, index, save_location):
    global save_lock
    emotions = []
    for tweet in tweets:
        try:
            emotions.append(utlis2.emo_detection(tweet))
        except Exception as err:
            emotions.append("unknown")
    save_lock.acquire()
    save_location[index] = emotions
    save_lock.release()


detected_emotions = [None] * len(parsed_lines)
tweets_processed = 0
threads = []

for i in range(0, len(parsed_lines)):

    t = threading.Thread(target=requestEmotions, args=(parsed_lines[i][:3], i, detected_emotions))
    t.start()
    threads.append(t)
    

    tweets_processed += 1
    print("Processed tweets for emotions:", tweets_processed)
    # print(utlis2.emo_detection(tweet1), utlis2.emo_detection(tweet2), utlis2.emo_detection(tweet3), emo)

for t in threads:
    t.join()
print("____________JOB DONE_______________")

parsed_lines = map(lambda quadruplet: list(map(nltk.word_tokenize, quadruplet)), parsed_lines)
parsed_lines = list(map(line_to_dict, parsed_lines, detected_emotions))
=======
            print(wordObj)
            wordObj["lemma"] = lemmatizer.lemmatize(wordObj["word"].lower(), utils.get_wordnet_pos(wordObj["pos"]))



parsed_lines = map(lambda quadruplet: list(map(nltk.word_tokenize, quadruplet)), parsed_lines)
parsed_lines = list(map(line_to_dict, parsed_lines))
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144




synonymDB = dict()

for line in parsed_lines:
    lemmatize(line)
    utils.remove_frequent_words(line["replies"])
    utils.remove_punctuation(line)
    utils.best_synonym(line["replies"])
    utils.detect_capslock(line)
    utils.ner_words(line)
    for reply in line["replies"]:
        for wordObj in reply:
<<<<<<< HEAD
            # print(wordObj)
=======
            print(wordObj)
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144
            utils.populate_synonym_db(wordObj, synonymDB, line["emotion"])

utils.calculate_dictionary(parsed_lines)

for line in parsed_lines:
    utils.lda_topic_detect(line)

<<<<<<< HEAD
utils.print_metrics()

with open("frequencies.json", "w") as freq:
    json.dump(synonymDB, freq, indent = 4)

with open("parsed_dataset.json", "w") as dataset:
    json.dump(parsed_lines, dataset, indent=4)
=======
with open("frequencies.json", "w", encoding="utf-8") as freq:
    json.dump(synonymDB, freq, indent = 4, ensure_ascii=False)

with open("parsed_dataset.json", "w", encoding="utf-8") as dataset:
    json.dump(parsed_lines, dataset, indent=4, ensure_ascii=False)
>>>>>>> cc7b216acc57f5b75a6af6423651aa1348553144
