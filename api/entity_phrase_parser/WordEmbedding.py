import gc
import gensim


class WordEmbedding(object):
    def __init__(self):
        self.model = []

    def toggle_word_embedding(self, toggle=True, local=False):
        if self.model == [] and toggle:
            if local:
                self.model = gensim.models.KeyedVectors.load_word2vec_format(
                    './GoogleNews-vectors-negative300.bin',
                    binary=True)
            self.model = gensim.models.KeyedVectors.load_word2vec_format(
                'https://elasticbeanstalk-us-east-1-362049109890.s3.amazonaws.com/GoogleNews-vectors-negative300.bin',
                binary=True)
            return toggle
        elif self.model != [] and not toggle:
            model = []
            gc.collect()
            return toggle