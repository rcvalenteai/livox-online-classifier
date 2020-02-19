"""
@author: Richard Valente <rcvalente@wpi.edu>
@date: 1/4/2020
@contributors: rcvalenteai

EntityScore

Handles scoring of ngram entities using generated/loaded dictionary vocabulary
"""
from api.entity_phrase_parser.vocab_generator import *


def get_ngram_score(word):
    """
    offline scoring mechanism for prioritizing larger compound words, references dictionary of keys
    :param word: word to check if exists
    :return: score of word, (1 for unigram, > 1 for identified ngrams, < 1 for unidentified ngrams)
    """
    recognized_ngram_offset = 0.10
    unknown_ngram_offset = 0.15
    words_count = len(word.split())
    score = 1
    if words_count > 1:
        if word in ngram_vocab.keys():
            score += (recognized_ngram_offset * words_count)
        else:
            score -= (unknown_ngram_offset * words_count)
    return score


ngram_vocab = initialize_vocabulary()
