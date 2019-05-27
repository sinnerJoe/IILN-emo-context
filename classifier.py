from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
import json
import numpy as np

with open("bayes_prepared.json", "rt", encoding="utf-8") as f:
    prepared_data = json.load(f)


features = [prepared_data[emotion] for emotion in ["happy", "angry", "sad", "others"]]

features = tuple(zip(*features))
print(features[1:4])
# print([len(i) for i in features], len(prepared_data["emotion"]))

bayes = MultinomialNB()

bayes.fit(features, prepared_data["emotion"])
print(prepared_data["emotion"][:100])
pred = bayes.predict([(100000.002, 10000.000005, 0.0000003, 0.00002)])

print(pred)