import matplotlib.pyplot as plt
import evaluation.mturk_metadata as metadata


def plot_word_frequency(filename):
    word_frequency = metadata.question_word_frequency(filename)
    plot_dictionary_counter(word_frequency)


def plot_ngram_frequency(filename):
    ngram_frequency = metadata.ngram_frequency(filename)
    plot_dictionary_counter(ngram_frequency)


def plot_dictionary_counter(dict_counter):
    dict_counter = {k: v for k, v in sorted(dict_counter.items(), key=lambda item: item[1], reverse=True)}
    plt.bar(range(len(dict_counter)), list(dict_counter.values()), align='edge')
    plt.xticks(range(len(dict_counter)), list(dict_counter.keys()))
    plt.show()


plot_word_frequency("./cleaned/mturk.csv")
plot_ngram_frequency("./cleaned/mturk.csv")