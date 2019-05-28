from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
import json
import numpy as np
import operator

# with open("bayes_prepared.json", "rt", encoding="utf-8") as f:
#     prepared_data = json.load(f)


# features = [prepared_data[emotion] for emotion in ["happy", "angry", "sad", "others"]]

# features = tuple(zip(*features))
# # print(features[1:4])
# # print([len(i) for i in features], len(prepared_data["emotion"]))

# bayes = MultinomialNB()

# bayes.fit(features, prepared_data["emotion"])
# # print(prepared_data["emotion"][:100])
# pred = bayes.predict([(100000.002, 10000.000005, 0.0000003, 0.00002)])

# # print(pred)

def naive_bayes(sentence):
    emotion_probability = {"happy" : 0.1, "angry" : 0.1, "sad" : 0.1, "others" : 0.7}
    tf_idf = json.load(open("tf-idf.json", "rt", encoding="utf-8"))
    for emotion in emotion_probability:
        for word in sentence.split():
            if word not in tf_idf[emotion] or tf_idf[emotion][word] == 0:
                print(emotion, word, 0)
                emotion_probability[emotion] *= 0.0001
            else:
                print(emotion, word, tf_idf[emotion][word])
                emotion_probability[emotion] *= tf_idf[emotion][word]
    print(emotion_probability)
    return sorted(emotion_probability.items(), key=operator.itemgetter(1), reverse = True)[0][0]
