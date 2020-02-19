import gzip
import gensim
from gensim.models.phrases import Phrases, Phraser


def create_model(zip, n):

    # build vocabulary and train model
    model = gensim.models.Word2Vec(
        zip,
        size=150,
        window=10,
        min_count=2,
        workers=8,
        iter=10
    )