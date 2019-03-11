import nltk
from nltk import WordNetLemmatizer
import re
import json
# nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

parsed_lines = []
lemmatizer = WordNetLemmatizer()
with open("devsetwithlabels/dev.txt") as file:
    replacer = re.compile("^d+\t([^\t]+)\t([^\t]+)\t([^\t+])?[ \t](angry|sad|other|)$")
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
    pos_replies = map(nltk.pos_tag, line)
    # lemmatized_replies = [(w,p) for reply in pos_replies for w,p in reply if reply[0]]

    lemmatized_replies = []
    for reply in pos_replies:
        objs = list(map(lambda arg: { "pos": arg[1], "word": arg[0]}, reply))
        lemmatized_replies.append(objs)
    res["replies"] = lemmatized_replies
    # print(res["replies"])
    res["emotion"] = line[3][0]
    return res

def lemmatize(line_dict):
    for reply in line_dict["replies"]:
        for wordObj in reply:
            print(wordObj)
            wordObj["lemma"] = lemmatizer.lemmatize(wordObj["word"])




parsed_lines = map(lambda quadruplet: list(map(nltk.word_tokenize, quadruplet)), parsed_lines)
parsed_lines = list(map(line_to_dict, parsed_lines))

for line in parsed_lines:
    lemmatize(line)


with open("parsed_dataset.json", "w") as dataset:
    json.dump(parsed_lines, dataset, indent=4)
