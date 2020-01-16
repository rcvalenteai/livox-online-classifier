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
    print(word_counter)
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
    print(ngram_counter)
    return ngram_counter


question_word_frequency("./cleaned/mturk.csv")
ngram_frequency("./cleaned/mturk.csv")