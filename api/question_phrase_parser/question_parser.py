import api.question_phrase_parser.question_words_generator as word_gen

pattern_dict = word_gen.load_question_words()


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
    return [invocation_phrase, list_phrase]


def question_classifier(phrase):
    """
    classifies if a question is a list question
    :param phrase: phrase to test
    :return: if the question is a classifier
    :rtype: bool
    """
    words = phrase.split()
    if 'or' in words:
        if any(x in words for x in pattern_dict.keys()):
            return True
    return False
