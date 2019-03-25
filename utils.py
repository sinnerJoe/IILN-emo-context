import nltk
import math
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

# Use of get_wordnet_pos
# for tweet in tweets:
#         print([wordnet_lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(tweet)])
    

def tf_idf(tweets_dicts):
    tf = {
        "happy" : {},
        "sad" : {},
        "angry" : {},
        "others" : {}
    }
    emo = {
        "happy" : 0,
        "sad" : 0,
        "angry" : 0,
        "others" : 0
    }
    idf = {}
    for dic in tweets_dicts:
        freq = {}
        [tweet1, tweet2, tweet3, aux] = dic["replies"]
        for word_dic in tweet1:
            if word_dic["lemma"] not in freq:
                freq[word_dic["lemma"]] = 1
            else:
                freq[word_dic["lemma"]] += 1
        for word_dic in tweet2:
            if word_dic["lemma"] not in freq:
                freq[word_dic["lemma"]] = 1
            else:
                freq[word_dic["lemma"]] += 1
        for word_dic in tweet3:
            if word_dic["lemma"] not in freq:
                freq[word_dic["lemma"]] = 1
            else:
                freq[word_dic["lemma"]] += 1
        
        for word in freq.keys():
            if word not in idf:
                idf[word] = 1
            else:
                idf[word] += 1
            if word not in tf[dic["emotion"]]:
                tf[dic["emotion"]][word] = freq[word]
            else:    
                tf[dic["emotion"]][word] += freq[word]
        
        
        emo[dic["emotion"]] += 1
    
    for emotion in tf.keys():
        for word in tf[emotion].keys():
            tf[emotion][word] /= emo[emotion]
    
    for word in idf.keys():
        idf[word] = math.log(len(tweets_dicts)/idf[word])

    for emotion in tf.keys():
        for word in tf[emotion].keys():
            tf[emotion][word] *= idf[word]
    
    s = json.dumps(tf)
    open("tf-idf.json", "wt").write(s)
    print(tf)


tf_idf(json.load(open("parsed_dataset.json", "rt")))
