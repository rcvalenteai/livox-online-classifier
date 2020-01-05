"""
@author: Richard Valente <rcvalente@wpi.edu>
@date: 1/4/2020
@contributors: rcvalenteai

StopWords
loads and preporcesses stopwords from nltk for the purpose of entity phrase parsing
"""
import nltk
from nltk.corpus import stopwords


def initialize_stop_words():
    """
    initialize the stop words for entity parser
    :return:
    """
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))
    stop_words.discard('and')
    return stop_words


STOP_WORDS = initialize_stop_words()
