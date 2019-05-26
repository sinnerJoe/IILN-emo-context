#!/usr/bin/env python3
import nltk
from nltk import WordNetLemmatizer
import re
import json
from nltk.wsd import lesk
import utility_lib as utils

 
# nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')


parsed_lines = []
lemmatizer = WordNetLemmatizer()
with open("devsetwithlabels/dev.txt", encoding="utf-8") as file:
    replacer = re.compile("^d+\t([^\t]+)\t([^\t]+)\t([^\t]+)?[ \t](angry|sad|other|happy)$")
    next(file)
    for line in file:
        split = line.split("\t")
        del split[0]
        if '\n' in split[-1]:
            split[-1] = split[-1][:-1]
        parsed_lines.append(split)

# print(parsed_lines)


def line_to_dict(line):
    res = dict()
    replies = [utils.tokenize_emojis(reply) for reply in line[:-1]]
    pos_replies = map(nltk.pos_tag, replies)

    lemmatized_replies = []
    for reply in pos_replies:
        objs = list(map(lambda arg: { "pos": arg[1], "word": utils.reduce_repeated_chars(arg[0]) }, reply))
        lemmatized_replies.append(objs)
    res["replies"] = lemmatized_replies
    res["emotion"] = line[3][0]
    return res

def lemmatize(line_dict):
    for reply in line_dict["replies"]:
        for wordObj in reply:
            print(wordObj)
            wordObj["lemma"] = lemmatizer.lemmatize(wordObj["word"].lower(), utils.get_wordnet_pos(wordObj["pos"]))



parsed_lines = map(lambda quadruplet: list(map(nltk.word_tokenize, quadruplet)), parsed_lines)
parsed_lines = list(map(line_to_dict, parsed_lines))




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
            print(wordObj)
            utils.populate_synonym_db(wordObj, synonymDB, line["emotion"])

utils.calculate_dictionary(parsed_lines)

for line in parsed_lines:
    utils.lda_topic_detect(line)

with open("frequencies.json", "w", encoding="utf-8") as freq:
    json.dump(synonymDB, freq, indent = 4, ensure_ascii=False)

with open("parsed_dataset.json", "w", encoding="utf-8") as dataset:
    json.dump(parsed_lines, dataset, indent=4, ensure_ascii=False)
