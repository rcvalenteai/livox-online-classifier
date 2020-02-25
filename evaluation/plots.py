import matplotlib.pyplot as plt
import numpy as np
import evaluation.mturk_metadata as metadata
import online_api.api
import os
import csv


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

    ax.barh(y_pos, counts, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Frequency Count')
    ax.set_title(title)

    plt.show()


def plot_clustered_bar(dict_counters, title):
    # set width of bar

    types = list(dict_counters.keys())
    bars_types = list()
    labels = list()
    rs = list()
    count = 0

    for key, value in dict_counters.items():
        if count == 0:
            count += 1
            labels = list(value.keys())
            # labels.remove('misc')
            for label in labels:
                bars_types.append(list())
    for key, value in dict_counters.items():
        count2 = 0
        for key2, value2 in value.items():
                bars_types[count2].append(value2)
                count2 += 1
                print(count2)
    # bars_types.append(list(value.values()))
    print(bars_types)
    barWidth = 1 / len(labels)

    bars_types2 = list()
    for bar in bars_types:
        try:
            print(bar)
            # t_bar = [bar[2], bar[3], bar[0], bar[1]]
            # bars_types2.append(t_bar)
        except Exception:
            pass

    # bars_types = bars_types2
    # bars_types = [bars_types[2], bars_types[3], bars_types[0], bars_types[1]]
    print(labels)
    # types = [types[2], types[3], types[0], types[1]]
    plt.legend(loc='')

    #
    # # set height of bar
    # bars1 = [12, 30, 1, 8, 22]
    # bars2 = [28, 6, 16, 5, 10]
    # bars3 = [29, 3, 24, 25, 17]

    # # Set position of bar on X axis
    # rpos = list()
    print("BARS", len(bars_types))
    rq = np.arange(len(bars_types[0]))
    rs.append(rq)
    for i in range(len(bars_types)):
        temp_r = [x + barWidth for x in rs[i]]
        rs.append(temp_r)

    # Make the plot
    temp_csv = list()
    temp_csv.append(types)
    for i in range(len(bars_types)):
        print(len(bars_types[i]))
        temp_csv.append([labels[i]] + bars_types[i])
        # plt.bar(rs[i], bars_types[i], width=barWidth, edgecolor='white', label=labels[i])
    write_list_csv("excel", "conditions.csv", temp_csv)
    print(temp_csv)

    print("DFSFSDFSDFSD")
    # Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars_types[0]))], types)
    plt.title(title)

    # Create legend & Show graphic
    plt.legend()
    plt.show()

def write_list_csv(output_folder, filename, rows):
    output_path = "./" + output_folder + "/"
    filename = output_path + filename
    #print(filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(filename, 'w', newline='', encoding='utf-8') as out:
        csv_cout = csv.writer(out)
        for row in rows:
            csv_cout.writerow(row)

plot_word_frequency("./cleaned/mturk.csv")
plot_ngram_frequency("./cleaned/mturk.csv")
plot_category_frequency("./cleaned/mturk.csv")
