import json


def save_dict_as_json(question_words, filename):
    str_json = json.dumps(question_words)
    extended_json = json.loads(str_json)
    with open(filename, 'w') as f:
        json.dump(extended_json, f)


def generate_question_words(filename):
    """
    save question words as resource dictionary
    :return: updated_dictionary
    """
    pattern_dict = dict()
    que_words = ['what', 'when', 'where', 'would', 'want', 'do', 'whats', 'is', 'who', 'whos', 'are', 'how', 'will',
                 'which', 'did', 'should']
    what_words = ['favorite', 'for', "to", 'want']
    what_ptrns = [1, 1, 1, 0]
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
    will_words = ['you', 'be', 'in', 'it']
    will_ptrns = [1, 0, 0, 0]
    which_words = ['the', 'your', 'you', 'is', 'more']
    which_ptrns = [1, 1, 1, 1, 0]
    did_words = ['at', 'with', 'if', 'to', 'for', 'as', 'you']
    did_ptrns = [0, 0, 0, 0, 0, 0, 1]
    should_words = ['go', 'at', 'we', 'you']
    should_ptrns = [1, 0, 1, 1]

    second_words = [what_words, when_words, where_words, would_words, want_words, do_words, what_words, is_words,
                    who_words, whos_words, are_words, how_words, will_words, which_words, did_words, should_words]
    patterns = [what_ptrns, when_ptrns, where_ptrns, would_ptrns, want_ptrns, do_ptrns, what_ptrns, is_ptrns, who_ptrns,
                whos_ptrns, are_ptrns, how_ptrns, will_ptrns, which_ptrns, did_ptrns, should_ptrns]
    for i in range(len(que_words)):
        pattern_dict[que_words[i]] = dict()
        for j in range(len(second_words[i])):
            pattern_dict[que_words[i]][second_words[i][j]] = patterns[i][j]

    save_dict_as_json(pattern_dict, filename)
    return pattern_dict


def load_question_words():
    filename = "./resources/phrase_parse_vocabulary.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            vocab = json.loads(f.read())
    except FileNotFoundError:
        vocab = generate_question_words(filename)

    return vocab


load_question_words()