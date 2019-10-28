import csv


def add_question_words():
    """
    pattern_dict with question words and patterns
    :return: updated_dictionary
    """
    pattern_dict = dict()
    que_words = ['what', 'when', 'where', 'would', 'want', 'do']
    what_words = ['for', 'want']
    what_ptrns = [1, 0]
    when_words = ['going', 'go']
    when_ptrns = [0, 0]
    where_words = ['for', 'go', 'from', 'to', 'going']
    where_ptrns = [1, 0, 0, 1, 0]
    would_words = ['rather']
    would_ptrns = [0]
    want_words = ['have']
    want_ptrns = [0]
    do_words = ['to', 'want']
    do_ptrns = [1, 0]
    second_words = [what_words, when_words, where_words, would_words, want_words, do_words]
    patterns = [what_ptrns, when_ptrns, where_ptrns, would_ptrns, want_ptrns, do_ptrns]
    for i in range(len(que_words)):
        pattern_dict[que_words[i]] = dict()
        for j in range(len(second_words[i])):
            pattern_dict[que_words[i]][second_words[i][j]] = patterns[i][j]
    print(pattern_dict)
    return pattern_dict


pattern_dict = add_question_words()


def phrase_split(phrase):
    """
    accepts a full phrase string and returns a list of the invocation and list phrase
    :return: returns a list with two strings the invocation phrase and the list phrase
    :rtype: list<str>
    """
    words = phrase.split()
    offset = pattern_dict[words[0]]
    num_offset = 0
    for i in range(len(words[1:])):
        for key, value in offset.items():
            if words[1:][i] == key:
                num_offset = value + i + 2
                break
    invocation_phrase = " ".join(words[:num_offset])
    list_phrase = " ".join(words[num_offset:])
    print(invocation_phrase)
    print(list_phrase)
    return [invocation_phrase, list_phrase]
