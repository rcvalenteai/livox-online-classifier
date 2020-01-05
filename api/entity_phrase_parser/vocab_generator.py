import json

from labels import MySQLDB
from api.entity_phrase_parser.WordEmbedding import WordEmbedding


def get_labels_from_db():
    db = MySQLDB.init_db()
    stmt = "SELECT DISTINCT label FROM Labels"
    cur = db.query(stmt)
    labels = cur.fetchall()
    return labels


def filter_ngram_labels(labels, min_ngram, max_ngram):
    vocabulary = dict()
    for result in labels:
        words = result[0].split()
        num_of_words = len(words)
        if min_ngram < num_of_words <= max_ngram:
            vocabulary[result[0].lower()] = 0
    return vocabulary


def save_dict_as_json(vocabulary, filename):
    str_json = json.dumps(vocabulary)
    extended_json = json.loads(str_json)
    with open(filename, 'w') as f:
        json.dump(extended_json, f)


def create_ngram_dict(min_ngram=1, max_ngram=3, filename='./resources/vocabulary.json'):
    """
    create vocabulary of compound words in the tag dataset
    :param min_ngram: include compound words of size greater than this number
    :param max_ngram: include compound words of size less than or equal to this number
    :param filename: where to save generated dictionary in resources
    :return: dictionary of vocabulary
    :rtype: dict
    """
    db_labels = get_labels_from_db()
    vocabulary = filter_ngram_labels(db_labels, min_ngram, max_ngram)
    save_dict_as_json(vocabulary, filename)
    return vocabulary


def word2vec_ngram_dict(min_ngram=1, max_ngram=3, filename='./resources/vocabulary.json'):
    vocabulary = dict()
    count = 0
    model.toggle_word_embedding(local=True)
    print("loaded")
    for item in model.model.vocab:
        words = item.split('_')
        if min_ngram < len(words) <= max_ngram:
            if count < 5:
                print(" ".join(words).lower())
                count += 1
            vocabulary[" ".join(words).lower()] = 0


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


def load_ngram_dict(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        vocab = json.loads(f.read())
    return vocab


def initialize_vocabulary(filename='./resources/vocabulary.json'):
    vocabulary = None
    try:
        vocabulary = load_ngram_dict(filename)
    except FileNotFoundError:
        vocabulary = create_ngram_dict(1)
    return vocabulary


model = WordEmbedding()
