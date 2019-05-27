
import json

emotion_labels = {
    "happy": 0,
    "sad": 1,
    "angry": 2,
    "others": 3
}

def prepare_data(parsed_dataset, tf_idf_dataset):

    prepared_data = {
        "happy": [],
        "sad": [],
        "angry": [],
        "others": [],
        "emotion": []
    }
    for tweet_group in parsed_dataset:
        all_words = []
        for reply in tweet_group["replies"]:
            all_words.extend(reply)
        
        total_emotion = [0, 0, 0, 0] #happy=0, sad=1, angry=2, other=3
        for word in all_words:
            lemma= word["lemma"]
            total_emotion[0] += tf_idf_dataset["happy"].get(lemma, 0)
            total_emotion[1] += tf_idf_dataset["sad"].get(lemma, 0)
            total_emotion[2] += tf_idf_dataset["angry"].get(lemma, 0)
            total_emotion[3] += tf_idf_dataset["others"].get(lemma, 0)

        for label in emotion_labels:
            prepared_data[label].append(total_emotion[emotion_labels[label]])
        prepared_data["emotion"].append(emotion_labels[tweet_group["emotion"]])

    return prepared_data


with open("parsed_dataset.json", "rt", encoding="utf-8") as f:
    parsed_dataset = json.load(f)

with open("tf-idf.json", "rt", encoding="utf-8") as f:
    tf_idf_dataset = json.load(f)

data = prepare_data(parsed_dataset, tf_idf_dataset)
with open("bayes_prepared.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

