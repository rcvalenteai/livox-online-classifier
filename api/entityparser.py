import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from labels import MySQLDB

import gc
import sys
import gensim
import json

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stop_words.discard('and')


class NGramException(Exception):
    """
    Raised when attempting to created an n-gram where n > the length of words
    """

    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.message = "NGramException: n-gram length " + str(n) + " is longer than words length " + str(k) + \
                 "\nRaised when attempting to created an n-gram where n > the length of words "
        sys.stderr.write(self.message)


class WordEmbedding(object):
    def __init__(self):
        self.model = []

    def toggle_word_embedding(self, toggle=True, local=False):
        if self.model == [] and toggle:
            if local:
                self.model = gensim.models.KeyedVectors.load_word2vec_format(
                    './GoogleNews-vectors-negative300.bin',
                    binary=True)
            self.model = gensim.models.KeyedVectors.load_word2vec_format(
                'https://elasticbeanstalk-us-east-1-362049109890.s3.amazonaws.com/GoogleNews-vectors-negative300.bin',
                binary=True)
            return toggle
        elif self.model != [] and not toggle:
            model = []
            gc.collect()
            return toggle


def create_ngram_dict(n, filename='./resources/vocabulary.json', withw2v=False):
    """
    create vocabulary of compound words in the tag dataset
    :param n: include compound words of size greater than this number
    :return: dictionary of vocabulary
    :rtype: dict
    """
    db = MySQLDB.init_db()
    stmt = "SELECT DISTINCT label FROM Labels"
    cur = db.query(stmt)
    results = cur.fetchall()
    vocabulary = dict()
    counters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for result in results:
        words = result[0].split()
        # greater than 1 word
        if len(words) > n:
            vocabulary[result[0].lower()] = 0
            counters[len(words)] += 1
    if withw2v:
        count = 0
        model.toggle_word_embedding(local=True)
        print("loaded")
        for item in model.model.vocab:
            words = item.split('_')
            if len(words) > n:
                if count < 5:
                    print(" ".join(words).lower())
                    count += 1
                vocabulary[" ".join(words).lower()] = 0
                try:
                    counters[len(words)] += 1
                except IndexError:
                    pass
    print(counters)
    str_json = json.dumps(vocabulary)
    extended_json = json.loads(str_json)
    with open(filename, 'w') as f:
        json.dump(extended_json, f)
    return vocabulary


def load_ngram_dict(filename='./resources/vocabulary.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        vocab = json.loads(f.read())
    return vocab


def create_extended_vocab(n, filename='./resources/extended_vocab,json'):
    """
    generates a list of extended vocabulary for each word in vocabulary
    :param n: closest n similar words
    :return: dictionary of vocabulary connected to list of words
    :rtype: dict<str:list>
    """
    extended_vocab = dict()
    vocab = load_ngram_dict()
    print("loading word embedding")
    model.toggle_word_embedding(local=True)
    print("loaded word embedding")
    count = 0
    for word in vocab.keys():
        if count == 0:
            print("searching keys")
        word2 = word.replace(" ", "_")
        try:
            words = model.model.similar_by_word(word2, topn=n)
            words2 = list()
            for w in words:
                words2.append({'word': w[0].replace("_", " "), 'sim': w[1]})
            extended_vocab[word] = words2
        except KeyError:
            pass
        if count == 0:
            print(extended_vocab)
            count += 1
    str_json = json.dumps(extended_vocab)
    extended_json = json.loads(str_json)
    with open(filename, 'w') as f:
        json.dump(extended_json, f)


def refine_extended_vocab(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        vocab = json.loads(f.read())
    cleaned = dict()
    for key, value in vocab.items():
        temp = list()
        for v in value:
            temp.append(v['word'])
        cleaned[key] = temp
    str_json = json.dumps(cleaned)
    extended_json = json.loads(str_json)
    with open('./resources/extened-vocab-cleaned.json', 'w') as f:
        json.dump(extended_json, f)

    translate = dict()
    translate_value = dict()
    for key, value in vocab.items():
        for v in value:
            if v['word'] in translate:
                if translate_value[v['word']] < v['sim']:
                    translate[v['word']] = key
                    translate_value[v['word']] = v['sim']
            else:
                translate[v['word']] = key
                translate_value[v['word']] = v['sim']
    str_json = json.dumps(translate)
    extended_json = json.loads(str_json)
    with open('./resources/extened-vocab-translate.json', 'w') as f:
        json.dump(extended_json, f)


def rm_stopwords(phrase):
    """
    removes stop words from given phrase, returns tokenized list of words
    :param phrase: a string containing a list of items including stop words
    :return: tokenized list of words without stop words
    """
    phrase = phrase.replace(" and ", "_and_")
    word_tokens = word_tokenize(phrase)
    filtered = [w for w in word_tokens if not w in stop_words]
    return filtered


def ngrams(words, n=2):
    """
    returns all possible combinations of ngrams from the list of words
    :param words: list of tokenized words
    :param n: n-gram limit, 3 = tri-gram (chocolate chip cookie), 2 = bi-gram (hot dog), 1 = uni-gram (dog)
    :return: list of lists of possible entity combinations
    """
    k = len(words)
    entities = []
    for i in range(n):
        entities.append(specngrams(words, i+1))
    return entities


def specngrams(words, n):
    """
    returns specified ngrams in a list of words, limited by order
    :param words: list of tokenized words
    :param n: ngram to perform computation over
    :return: list of ngrams
    """
    k = len(words)
    if k < n:
        n = k
        # aise NGramException(n, k)
    ngrams = []
    for i in range(k - (n - 1)):
        entity = ""
        for j in range(n):
            entity += words[i+j] + " "
        entity = entity[:-1]
        ngrams.append(entity)
    return ngrams


def entity_combination(i, k, n, words, path):
    """
    returns all possible entities between the n-grams 2D words list
    :param i: starting spot
    :param k: size of phrase
    :param n: size of max n-gram
    :param words: 2D list of n-grams
    :param path: words used up until this part of the phrase
    :return: returns a list of <lists of entities> of each possible phrase combination
    """
    combinations = []
    if i == k:
        return [path]
    for gram_count in range(n):
        if i + (gram_count + 1) <= k:
            temp = path + [words[gram_count][i]]
            see_return = entity_combination(i+(gram_count+1), k, n, words, temp)
            combinations += see_return
        else:
            return combinations
    return combinations


def word2vec(w1, w2):
    """
    get cosine similarity score between two words
    :param w1: word or phrase to compare
    :param w2: word or phrase to compare
    :return: similarity score between -1 and 1
    """
    w1 = w1.replace(" ", "_")
    w2 = w2.replace(" ", "_")
    sim_score = .20
    try:
        sim_score = model.model.similarity(w1, w2)
    except KeyError:
        pass
    return sim_score


def offline_ngram_dict(w1):
    """
    offline scoering mechanism, references dictionary of keys
    :param w1: word to check if exists
    :return: score of word, (1 for unigram, > 1 for identified ngrams, < 1 for unidentified ngrams)
    """
    size = len(w1.split())
    score = 1
    if size > 1:
        if w1 in ngram_vocab.keys():
            score += (0.10 * size)
        else:
            score -= (0.15 * size)
    return score


def offline_best_entities(ent_list):
    """
    find most similar batch of phrases through ngram vocabulary list scoring
    :param ent_list: a list of all combinations of entities, list<list<str>>
    :return: one sub-list of entities
    :rtype: list<str>
    """
    scores = []
    for entities in ent_list:
        comb_sum = 0.0
        for entity in entities:
            comb_sum += offline_ngram_dict(entity)
        scores.append(comb_sum / len(entities))
        # print(entities)
        # print(comb_sum / len(entities))
    best_comb = ent_list[scores.index(max(scores))]
    best_comb = [comb.replace("_and_", " and ") for comb in best_comb]
    return best_comb


def offline_parse_phrase(phrase, n=2):
    """
    parse phrase for most likely combination of entities
    :param phrase: list phrase containing list of entities to be parsed
    :param n: limit of ngrams to look for, 'hot dog' is a bi-gram
    :return: list of entities
    :rtype: list<str>
    """
    cleaned = rm_stopwords(phrase)
    example = ngrams(cleaned, n)
    combinations = entity_combination(0, len(cleaned), n, example, list())
    return offline_best_entities(combinations)


def best_entities(ent_list):
    """
    finds the most similar batch of phrases through cosine similarity
    :param ent_list: a list of all combinations of entities, list<list<str>>
    :return: list of entities
    :rtype: list<str>
    """
    scores = []
    for entities in ent_list:
        sum = 0.0
        size = len(entities)
        if size != 1:
            div = ((size - 1.0) / 2.0) * (size + 1)
        else:
            div = 1
        for i in range(len(entities)):
            for j in range(i+1, len(entities)):
                sum += word2vec(entities[i], entities[j])
        scores.append((sum/div))
    best_comb = ent_list[scores.index(max(scores))]
    return ent_list[scores.index(max(scores))]


def parse_phrase(phrase, n=2):
    """
    parse phrase for most likely combination of entities
    :param phrase: list phrase containing list of entities to be parsed
    :param n: limit of ngrams to look for, 'hot dog' is a bi-gram
    :return: list of entities
    :rtype: list<str>
    """
    cleaned = rm_stopwords(phrase)
    example = ngrams(cleaned, n)
    combinations = entity_combination(0, len(cleaned), n, example, list())
    return best_entities(combinations)


def tester(phrase):
    cleaned = rm_stopwords(phrase)
    example = ngrams(cleaned, 3)
    combinations = entity_combination(0, len(cleaned), 3, example, list())
    print(best_entities(combinations))


# Load Google's pre-trained Word2Vec model.
model = WordEmbedding()
#model.toggle_word_embedding()

ngram_vocab = create_ngram_dict(1)
#ngram_vocab = create_ngram_dict(1, withw2v=True)
#create_extended_vocab(10)
#refine_extended_vocab('./resources/extended_vocab.json')
#ngram_vocab = load_ngram_dict()

# tester("the hot dog the hamburger or the french fries")
# tester("the cat golden retriever or bichon")
# tester("the chocolate chip cookie the pumpkin pie or brownie")
# tester("the park bowling alley or the theatre")
# tester("rich andrew cole or zack")
# example2 =
# #example = "the sugar cookie or brownie"
# cleaned = rm_stopwords(example)
# #print(cleaned)
# example = ngrams(cleaned, 3)
# #print(example)
# #print(type(example))
# combinations = entity_combination(0, len(cleaned), 3, example, list())
# #print(len(combinations))
# print(best_entities(combinations))
# #print(word2vec('man', 'woman'))