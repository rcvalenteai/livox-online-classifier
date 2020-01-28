import matplotlib.pyplot as plt
import numpy as np
import evaluation.mturk_metadata as metadata


def plot_word_frequency(filename):
    word_frequency = metadata.question_word_frequency(filename)
    plot_horizontal_dictionary_counter(word_frequency, "Question Word Frequency Count")


def plot_ngram_frequency(filename):
    ngram_frequency = metadata.ngram_frequency(filename)
    plot_dictionary_counter(ngram_frequency, "Ngram Frequency Count")


def plot_category_frequency(filename):
    category_frequency = metadata.category_frequency(filename)
    plot_horizontal_dictionary_counter(category_frequency, "Category Frequency Count")


def plot_dictionary_counter(dict_counter, title):
    dict_counter = {k: v for k, v in sorted(dict_counter.items(), key=lambda item: item[1], reverse=True)}
    plt.bar(range(len(dict_counter)), list(dict_counter.values()), align='edge')
    plt.xticks(range(len(dict_counter)), list(dict_counter.keys()))
    plt.title(title)
    plt.show()


def plot_horizontal_dictionary_counter(dict_counter, title):
    dict_counter = {k: v for k, v in sorted(dict_counter.items(), key=lambda item: item[1], reverse=True)}
    plt.rcdefaults()
    fig, ax = plt.subplots()

    categories = list(dict_counter.keys())
    y_pos = np.arange(len(categories))
    counts = list(dict_counter.values())

    ax.barh(y_pos, counts , align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Frequency Count')
    ax.set_title(title)

    plt.show()


plot_word_frequency("./cleaned/mturk-r3ab.csv")
plot_ngram_frequency("./cleaned/mturk-r3ab.csv")
plot_category_frequency("./cleaned/mturk-r3ab.csv")
