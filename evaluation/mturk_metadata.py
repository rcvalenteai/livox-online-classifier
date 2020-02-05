import helpers.io as hio


def question_word_frequency(filename):
    mturk_data = hio.load_csv(filename)
    word_counter = dict()
    for line in mturk_data:
        first_word = line[0].split()[0]
        if first_word in word_counter.keys():
            word_counter[first_word] = word_counter[first_word] + 1
        else:
            word_counter[first_word] = 1
    word_counter = remove_outlier_words(word_counter)
    return word_counter


def remove_outlier_words(word_counter):
    for question_word, count in list(word_counter.items()):
        if count == 1:
            del word_counter[question_word]
    return word_counter


def ngram_frequency(filename):
    mturk_data = hio.load_csv(filename)
    ngram_counter = dict()
    for line in mturk_data:
        ngrams = line[1].split(",")
        for ngram in ngrams:
            gram_size = len(ngram.split())
            if gram_size in ngram_counter.keys():
                ngram_counter[gram_size] = ngram_counter[gram_size] + 1
            else:
                ngram_counter[gram_size] = 1
    return ngram_counter


def category_frequency(filename):
    mturk_data = hio.load_csv(filename)
    categories_counter = dict()
    for line in mturk_data:
        category = line[2]
        if category in categories_counter.keys():
            categories_counter[category] = categories_counter[category] + 1
        else:
            categories_counter[category] = 1
    return categories_counter


# question_word_frequency("./cleaned/mturk.csv")
# ngram_frequency("./cleaned/mturk.csv")
# category_frequency("./cleaned/mturk.csv")