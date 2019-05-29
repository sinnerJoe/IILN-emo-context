
import json 
import re
import nltk
import utility_lib as utils
import operator

import functools
emotion_labels = {
    "happy": 0,
    "sad": 1,
    "angry": 2,
    "others": 3
}

# def prepare_data(parsed_dataset, tf_idf_dataset):

#     prepared_data = {
#         "happy": [],
#         "sad": [],
#         "angry": [],
#         "others": [],
#         "emotion": []
#     }
#     for tweet_group in parsed_dataset:
#         all_words = []
#         for reply in tweet_group["replies"]:
#             all_words.extend(reply)
        
#         total_emotion = [0, 0, 0, 0] #happy=0, sad=1, angry=2, other=3
#         for word in all_words:
#             lemma= word["lemma"]
#             total_emotion[0] += tf_idf_dataset["happy"].get(lemma, 0)
#             total_emotion[1] += tf_idf_dataset["sad"].get(lemma, 0)
#             total_emotion[2] += tf_idf_dataset["angry"].get(lemma, 0)
#             total_emotion[3] += tf_idf_dataset["others"].get(lemma, 0)

#         for label in emotion_labels:
#             prepared_data[label].append(total_emotion[emotion_labels[label]])
#         prepared_data["emotion"].append(emotion_labels[tweet_group["emotion"]])

#     return prepared_data


# with open("parsed_dataset.json", "rt", encoding="utf-8") as f:
#     parsed_dataset = json.load(f)

with open("tf-idf.json", "rt", encoding="utf-8") as f:
    tf_idf_dataset = json.load(f)

# data = prepare_data(parsed_dataset, tf_idf_dataset)
# with open("bayes_prepared.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=2)



def prepare_test_data_row(data_row:list):
    tokenized_replies = [nltk.word_tokenize(reply) for reply in data_row[:3]]
    line_dict = utils.line_to_dict(tokenized_replies, with_emotion=False)

    utils.lemmatize(line_dict)
    utils.remove_frequent_words(line_dict["replies"])
    utils.remove_punctuation(line_dict)
    # utils.best_synonym(line_dict["replies"])
    if len(data_row) == 4:
        line_dict["emotion"] = data_row[3]
    for reply in line_dict["replies"]:
            for wordObj in reply:
                utils.find_synonyms(wordObj)
    return line_dict


def tf_idf_alternative(tweet_convos):
    word_occurences = {
        "happy": {},
        "sad": {},
        "angry": {},
        "others": {}
    }

    
    def calculate_emotion_prob(emotion): 
        return functools.reduce(lambda acc, convo: acc if convo["emotion"] != emotion else acc + 1, tweet_convos, 0) / len(tweet_convos)
        
    emo_probs = {
        "happy": calculate_emotion_prob("happy"),
        "sad": calculate_emotion_prob("sad"),
        "angry": calculate_emotion_prob("angry"),
        "others": calculate_emotion_prob("others")
    }

    total_words_per_category = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "others": 0
    }
    
    for convo in tweet_convos:
        emotion = convo["emotion"]
        for wordObj in utils.flatten(convo["replies"]):
            lemma = wordObj["lemma"]
            word_occurences[emotion][lemma] = word_occurences[emotion].get(lemma, 0) + 1
            total_words_per_category[emotion] += 1
    
    total_unique_words = set()
    for word_dict in word_occurences.values():
        total_unique_words.update(set(word_dict.keys()))
    total_unique_words = len(total_unique_words)

    for emotion in word_occurences: #likelyhood
        for word in word_occurences[emotion]:
            word_occurences[emotion][word] /= total_words_per_category[emotion]
    
    
    
    s = json.dumps(word_occurences, ensure_ascii=False, indent=2)
    open("tf-idf.json", "wt", encoding="utf-8", ).write(s)
    print(word_occurences)


if __name__ == "__main__":
    tf_idf_alternative(json.load(open("parsed_dataset.json", "rt", encoding="utf-8")))
