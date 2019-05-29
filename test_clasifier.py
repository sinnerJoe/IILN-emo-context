import operator
import functools
import json
import re
import nltk
import utility_lib as utils
import utils as utils2
import numpy as np
from prepare_for_bayes import prepare_test_data_row


def load_from_csv_file(path="starterkitdata/train.txt", delete_emotions = True):
    data_rows = []
    with open(path, encoding="utf-8") as file:
        next(file)
        for line in file:
            split = line.split("\t")
            del split[0]
            if '\n' in split[-1]:
                split[-1] = split[-1][:-1]
            if delete_emotions:
                del split[-1] #use only if dataset has assigned emotions
            data_rows.append(split)
    return [prepare_test_data_row(row) for row in data_rows]


def load_from_json_file(path="starterkitdata/train.txt"):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def flatten(lst): return list(functools.reduce(operator.iconcat, lst, []))

result = load_from_csv_file("devsetwithlabels/dev.txt")
# result = load_from_json_file("parsed_dataset.json")
result = [utils2.bayes(flatten(line["replies"])) for line in result]

wrong = 0
expectation_set = load_from_csv_file("devsetwithlabels/dev.txt", delete_emotions=False)
# expectation_set = load_from_json_file("parsed_dataset.json")

for i in range(0, len(expectation_set)):
    if(expectation_set[i]["emotion"] != result[i]):
        wrong += 1

total = len(expectation_set)
right = total - wrong


print("Wrong classifications:", wrong)
print("Right classifications:", right)
print("Precision(%)", 100 * (right) / total)

import baseline


def transform_output_data(output):
    result = []

    for el in output:
        classified_arr = [0, 0, 0, 0]
        classified_arr[baseline.emotion2label[el]] = 1
        result.append(classified_arr)
    return np.array(result)
expected = transform_output_data([el["emotion"] for el in expectation_set])
result = transform_output_data(result)


baseline.getMetrics(result, expected)

