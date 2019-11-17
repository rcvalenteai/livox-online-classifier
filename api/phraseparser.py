import csv


def add_question_words():
    """
    pattern_dict with question words and patterns
    :return: updated_dictionary
    """
    pattern_dict = dict()
    que_words = ['what', 'when', 'where', 'would', 'want', 'do', 'whats','is', 'who', 'whos', 'are', 'how']
    what_words = ['favorite', 'for', 'want']
    what_ptrns = [1, 1, 0]
    when_words = ['going', 'go']
    when_ptrns = [0, 0]
    where_words = ['for', 'go', 'from', 'to', 'going']
    where_ptrns = [1, 0, 0, 1, 0]
    would_words = ['rather', 'to', 'want']
    would_ptrns = [0, 1, 0]
    want_words = ['have']
    want_ptrns = [0]
    do_words = ['go', 'to', 'want']
    do_ptrns = [0, 1, 0]
    is_words = ['favorite', 'it', 'your']
    is_ptrns = [1, 0, 1]
    who_words = ['more', 'less']
    who_ptrns = [0, 0]
    whos_words = ['better', 'worse', 'faster', 'slower', 'stronger', 'weaker', 'it']
    whos_ptrns = [1, 1, 1, 1, 1, 1, 0]
    are_words = ['you']
    are_ptrns = [0]
    how_words = ['your', 'today', 'feeling']
    how_ptrns = [1, 0, 0]

    second_words = [what_words, when_words, where_words, would_words, want_words, do_words, what_words, is_words, who_words, whos_words, are_words, how_words]
    patterns = [what_ptrns, when_ptrns, where_ptrns, would_ptrns, want_ptrns, do_ptrns, what_ptrns, is_ptrns, who_ptrns, whos_ptrns, are_ptrns, how_ptrns]
    for i in range(len(que_words)):
        pattern_dict[que_words[i]] = dict()
        for j in range(len(second_words[i])):
            pattern_dict[que_words[i]][second_words[i][j]] = patterns[i][j]
    # print(pattern_dict)
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
    # print(invocation_phrase)
    # print(list_phrase)
    return [invocation_phrase, list_phrase]


def question_classifier(phrase):
    que_words = ['what', 'when', 'where', 'would', 'want', 'do', 'whats', 'is', 'who', 'whos', 'are', 'how']
    words = phrase.split()
    if 'or' in words:
        if any(x in words for x in que_words):
            return True
    return False
