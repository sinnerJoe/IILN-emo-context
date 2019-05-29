
import nltk
import math
import json
from nltk.wsd import lesk
# from nltk.stem import WordNetLemmatizer
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from itertools import chain
import gensim
from gensim import corpora 
import re
import pickle
import emoji
nltk.download("stopwords")
nltk.download('punkt')
import functools
import operator

def flatten(lst): return list(functools.reduce(operator.iconcat, lst, []))

def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)


def fix_spelling(reply):
    return [reduce_lengthening(word) for word in reply]

def reduce_repeated_chars(word):
    new_word = ""
    i = 0
    while i < len(word):
        reps = 1
        for j in range(i+1, len(word)):
            if word[i] == word[j]:
                reps += 1
            else:
                break
        if reps == 2:
            new_word += word[i:i+2]
        else: 
            new_word += word[i]
        i+=reps    
    return new_word

def get_wordnet_pos(pos):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(pos[0], wordnet.NOUN)


def best_synonym(replies):
    words = tuple([i for reply in replies for i in reply])
    words_str = tuple([i["lemma"] for i in words])
    # print(words_str)
    for i in range(0, len(words)):
        # print(words[i])
        try:
            best_syn = lesk(words_str, words_str[i], get_wordnet_pos(words[i]["pos"]))
            # print(best_syn)
            lemma_names = best_syn.lemma_names()
            if isinstance(lemma_names, list):
                words[i]["best_syn"] = lemma_names[0]
                 
        except:
            print("Except ", words_str[i])


el_punct_regex = re.compile(r"[,.!?_:+=*/\\;\[\]{}()@/$^\"]")
def eliminate_punctation(sentence):
    res = []
    for word in sentence:
        split_words = filter(lambda lst: len(lst) > 0, el_punct_regex.split(word))
        res.extend(list(split_words))
    return res

def line_to_dict(line, with_emotion = True):
    res = dict()
    replies_without_emotions = line[:-1] if with_emotion else line
    replies = [fix_spelling(reply) for reply in replies_without_emotions]
    replies = [eliminate_punctation(reply) for reply in replies]
    replies = [tokenize_emojis(reply) for reply in replies]
    pos_replies = map(nltk.pos_tag, replies)

    lemmatized_replies = []
    for reply in pos_replies:
        objs = list(
            map(lambda arg: {"pos": arg[1], "word": arg[0]}, reply))
        lemmatized_replies.append(objs)
    res["replies"] = lemmatized_replies
    if with_emotion:
        res["emotion"] = line[3][0]
    return res


lemmatizer = WordNetLemmatizer()
def lemmatize(line_dict):
    for reply in line_dict["replies"]:
        for wordObj in reply:
            # print(wordObj)
            wordObj["lemma"] = lemmatizer.lemmatize(
                wordObj["word"].lower(), get_wordnet_pos(wordObj["pos"]))


words_without_synononyms = 0
def find_synonyms(wordObj):
    global words_without_synononyms
    synonyms = wordnet.synsets(wordObj["lemma"])
    
    lemmas = chain.from_iterable([word.lemma_names() for word in synonyms])
    wordObj["synonyms"] = list(set(lemmas))
    if len(wordObj["synonyms"]) == 0:
        words_without_synononyms += 1
    # add_lemma(wordObj["lemma"], wordObj["synonyms"], database, emotion)



stop_words = set(nltk.corpus.stopwords.words('english'))
total_frequent_words_removed = 0
def remove_frequent_words(replies):
    global total_frequent_words_removed 
    for reply in replies:
        i = 0
        while i < len(reply):
            if reply[i]["lemma"].lower() in stop_words:
                del reply[i]
                total_frequent_words_removed += 1
            else:
                i+=1
capslock_detected = 0
def detect_capslock(line):
    global capslock_detected
    i = 0
    total = 0
    for reply in line["replies"]:
        total+=len(reply)
        for word in reply:
            if word["word"] == word["word"].upper():
                i+=1
    line["capslock"] = total / 3 < i
    if total / 3 < i:
        capslock_detected += 1
        
punct_re = re.compile(r"^(\?|\.|,| |\(|\))+$")


punctuation_removed = 0
def remove_punctuation(line):
    global punctuation_removed
    for reply in line["replies"]:
        i = 0
        while i < len(reply):
            if punct_re.match(reply[i]["word"]):
                del reply[i]
                punctuation_removed += 1
                # print("PUNCTUATION REMOVED")
            else:
                i+=1


def ner_words(line):
    replies = line["replies"]
    for reply in replies:
        tagged_words = [(wordObj["word"][0]+ wordObj["word"][1:], wordObj["pos"]) for wordObj in reply]
        ner_tags = nltk.ne_chunk(tagged_words)
        for chunk in ner_tags:
            if hasattr(chunk, "label") and chunk.label:
                name_value = ' '.join(child[0] for child in chunk.leaves())
                # print("------------------------------------")
                # print(name_value, chunk.label())
                for i in range(0, len(reply)):
                    wordObj = reply[i]
                    if wordObj['word'] == name_value:   
                        wordObj["ner_tag"] = chunk.label()
                        break


def reply_to_array_of_strings(reply):
    return list(map(lambda wordObj: wordObj["lemma"], reply))

total_words = 0
total_long_words = 0
total_tweet_nr = 0
dictionary = None
ldamodel = None
possible_topics = None
def calculate_dictionary(train_data):
    global total_words, total_long_words, total_tweet_nr
    global dictionary
    global ldamodel
    global possible_topics
    all_lines = [ flatten(map(reply_to_array_of_strings, i["replies"])) for i in train_data]
    all_words = []
    total_tweet_nr = len(train_data) * 3
    for line in all_lines:
        # all_words.append([word for word in line if len(word) > 4])
        sentence = []
        for word in line:
            total_words+=1
            if len(word) > 4:
                sentence.append(word)
                total_long_words += 1
        all_words.append(sentence)
    dictionary = corpora.Dictionary(all_words)
    all_words = [ dictionary.doc2bow(word) for word in all_words ]
    ldamodel = gensim.models.ldamodel.LdaModel(all_words, num_topics=20, id2word=dictionary, passes=15)
    possible_topics = ldamodel.print_topics(20)
    print("Possible topics", possible_topics)




def lda_topic_detect(instance):
    global possible_topics
    words = list(map(reply_to_array_of_strings, instance["replies"]))
    new_doc = list(map(dictionary.doc2bow, words))
    # print(ldamodel.get_document_topics(new_doc))
    top_index = ldamodel.get_document_topics(new_doc)[0]
    # best_topics = sorted(key=(lambda el: el[0]), iterable=top_index, reverse=True)[:4]
    top_index.sort(key=lambda el: el[0], reverse=True)
    index, prob = top_index[0]
    instance["topics"] = possible_topics[index][1]

def print_metrics():
    global total_frequent_words_removed, total_words, total_tweet_nr, punctuation_removed, capslock_detected, total_long_words
    global words_without_synononyms, capslock_detected
    print("Punctuation removed: ", punctuation_removed)
    print("Total frequent words removed: ", total_frequent_words_removed)
    print("Total words: ", total_words)
    print("Total long words: ", total_long_words)
    print("Words without synonyms: ", words_without_synononyms)
    print("Capslock detected: ", capslock_detected)
    print("Total tweets: ", total_tweet_nr)


emojis = emoji.UNICODE_EMOJI_ALIAS



def tokenize_emojis(reply):
    tokens = []
    for i in range(0, len(reply)):
        word = reply[i]
        more_emojis = True
        while more_emojis:
            more_emojis = False
            for j in range(0, len(word)):
                if word[j] in emojis:
                    more_emojis = True
                    if j > 0:
                        tokens.append(word[:j])
                        word = word[j:] 
                    tokens.append(emojis[word[0]])
                    word = word[1:] if len(word) > 0 else ""
                    break
        if len(word) > 0:
            tokens.append(word)
    return tokens
