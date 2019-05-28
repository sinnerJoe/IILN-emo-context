#!/usr/bin/env python3
import nltk

import re
import json
from nltk.wsd import lesk
import utility_lib as utils

 
# nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')


parsed_lines = []

with open("starterkitdata/train.txt", encoding="utf-8") as file:
    # replacer = re.compile("^d+\t([^\t]+)\t([^\t]+)\t([^\t]+)?[ \t](angry|sad|other|happy)$")
    next(file)
    for line in file:
        split = line.split("\t")
        del split[0]
        if '\n' in split[-1]:
            split[-1] = split[-1][:-1]
        parsed_lines.append(split)

# print(parsed_lines)





parsed_lines = map(lambda quadruplet: list(map(nltk.word_tokenize, quadruplet)), parsed_lines)
parsed_lines = list(map(utils.line_to_dict, parsed_lines))





for line in parsed_lines:
    utils.lemmatize(line)
    utils.remove_frequent_words(line["replies"])
    utils.remove_punctuation(line)
    # utils.best_synonym(line["replies"])
    # utils.detect_capslock(line)
    # utils.ner_words(line)
    for reply in line["replies"]:
        for wordObj in reply:
            print(wordObj)
            utils.find_synonyms(wordObj)

utils.calculate_dictionary(parsed_lines)

for line in parsed_lines:
    utils.lda_topic_detect(line)


with open("parsed_dataset.json", "w", encoding="utf-8") as dataset:
    json.dump(parsed_lines, dataset, indent=4, ensure_ascii=False)
