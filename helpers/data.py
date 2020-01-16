import random


# split data test_split = .8 = 80% train set 20% test set
# returns tuple of 2 tuples
def split_data(data, train_split):
    random.shuffle(data)
    pivot = round(train_split * len(data))
    train_set = data[:pivot]
    test_set = data[pivot:]
    return train_set, test_set


# split into X and Y sets
def split_xy(data):
    x_set = list()
    y_set = list()
    for row in data:
        x_set.append(row[1:-1])
        y_set.append(row[-1])
    return x_set, y_set