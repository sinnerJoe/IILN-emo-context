
import json 
import re
import nltk
import utility_lib as utils
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


