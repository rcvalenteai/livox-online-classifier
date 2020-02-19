"""
@author: Richard Valente <rcvalente@wpi.edu>
@date: 1/4/2020
@contributors: rcvalenteai

Entity Phrase Parser
Given a string of words, this class returns the most likely combination of entities,
including single word and compound words, interfaces through parse function
"""
from nltk.tokenize import word_tokenize
import online_api.api.entity_phrase_parser.entity_score as EntityScore
from online_api.api.entity_phrase_parser.stopwords import STOP_WORDS


class EntityPhrase(object):

    def __init__(self, entity_phrase, ngram_threshold=2):
        """
        contains functions for entity phrase, pre-processing, ngram detection, combination optimization
        :param entity_phrase: list phrase containing list of entities to be parsed
        :param ngram_threshold: limit of ngrams to look for, 'hot dog' is a bi-gram
        """
        self.entity_phrase = entity_phrase
        self.ngram_threshold = ngram_threshold

    def clean_entity_phrase(self):
        """
        pre processing step to clean entity_phrase
        """
        clean_phrase = self.entity_phrase.replace(" and ", "_and_")
        word_tokens = word_tokenize(clean_phrase)
        self.entity_phrase = [w for w in word_tokens if not w in STOP_WORDS]

    def ngrams(self):
        """
        returns all possible combinations of ngrams for the entity_phrase
        :return: list of lists of possible entity combinations
        """
        entity_combinations = []
        for i in range(self.ngram_threshold):
            entity_combinations.append(self.ngram_of_size(i+1))
        return entity_combinations

    def ngram_of_size(self, ngram_size):
        """
        create list of possible compound word entities
        of specific ngram size from adjacent words of entity phrase
        :param ngram_size: ngram size, 1 = unigram, 2 = bigram, 3 = trigram
        :return: list of ngrams
        """
        phrase_length = len(self.entity_phrase)
        if phrase_length < ngram_size:
            ngram_size = phrase_length
        ngrams = []
        for i in range(phrase_length - (ngram_size - 1)):
            entity = ""
            for j in range(ngram_size):
                entity += self.entity_phrase[i + j] + " "
            entity = entity[:-1]
            ngrams.append(entity)
        return ngrams

    def entity_combinations(self, ngrams):
        """
        returns all possible entities between the n-grams 2D words list
        :param ngrams: list of ngram entities
        :return: list of entity combinations
        """
        combinations = self.entity_combinations_helper(0, len(self.entity_phrase), ngrams, list())
        return combinations

    def entity_combinations_helper(self, starting_point, phrase_length, words, path):
        """
        recursive function that returns all possible entities between the n-grams 2D words list
        :param starting_point: starting spot
        :param phrase_length: size of phrase
        :param words: 2D list of n-grams
        :param path: words used up until this part of the phrase
        :return: returns a list of <lists of entities> of each possible phrase combination
        """
        combinations = []
        if starting_point == phrase_length:
            return [path]
        for gram_count in range(self.ngram_threshold):
            if starting_point + (gram_count + 1) <= phrase_length:
                current_word_path = path + [words[gram_count][starting_point]]
                new_combinations = self.entity_combinations_helper(starting_point + (gram_count + 1), phrase_length,
                                                                   words, current_word_path)
                combinations += new_combinations
            else:
                return combinations
        return combinations

    @staticmethod
    def best_entities(ent_list):
        """
        find most similar batch of phrases through ngram vocabulary list scoring
        :param ent_list: a list of all combinations of entities, list<list<str>>
        :return: one sub-list of entities
        :rtype: list<str>
        """
        if ent_list == [[]]:
            return []
        scores = []
        for entities in ent_list:
            comb_sum = 0.0
            for entity in entities:
                comb_sum += EntityScore.get_ngram_score(entity)
            try:
                scores.append(comb_sum / len(entities))
            except ZeroDivisionError:
                print(ent_list)
                print(entities)

        best_comb = ent_list[scores.index(max(scores))]
        best_comb = [comb.replace("_and_", " and ") for comb in best_comb]
        return best_comb


def parse(entity_phrase, ngram_threshold=2):
    """
    parse phrase for most likely combination of entities
    :param entity_phrase: list phrase containing list of entities to be parsed
    :param ngram_threshold: limit of ngrams to look for, 'hot dog' is a bi-gram
    :return: list of entities
    :rtype: list<str>
    """
    phrase_object = EntityPhrase(entity_phrase, ngram_threshold)
    phrase_object.clean_entity_phrase()
    all_ngrams = phrase_object.ngrams()
    entity_combinations = phrase_object.entity_combinations(all_ngrams)
    best_combination = phrase_object.best_entities(entity_combinations)
    return best_combination
