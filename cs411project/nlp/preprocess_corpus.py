import numpy as np
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.parsing.porter import PorterStemmer
# Use english stopwords provided in gensim as a baseline for stopword removal
from gensim.parsing.preprocessing import STOPWORDS, preprocess_string, strip_punctuation, strip_numeric, strip_short

# Bigram detection
from gensim.models.phrases import Phrases, Phraser
# The score threshold for determining bigrams (see Phrases class for more info)
BIGRAM_SCORE_THRESHOLD = 1
# The minimum number of times a bigram has to occur to be considered a bigram
BIGRAM_MIN_COUNT = 1


class Preprocessing:

    @classmethod
    def preprocess_corpus(cls, raw_corpus):
        """Preprocess a corpus for the downage categories

            Parameters:
                raw_corpus: A list of strings where each string is a document

            Returns:
                A tuple (dictionary, id2token, corpus_bow) where

                    dictionary: The gensim.corpora.dictionary for the preprocessed corpus
                    id2token: A python dictionary mapping BOW id to token
                    corpus_bow: The preprocessed corpus in BOW form, using BOW ids from `dictionary`
        """

        # Define filters to apply to each word
        # Make each token lowercase
        # Remove punctuation
        # Remove numeric characters
        # Any token less than 2 characters is removed
        FILTERS = [(lambda x: x.lower()), strip_punctuation, strip_numeric, (lambda x: strip_short(x, minsize=2))]

        preprocessed_corpus = [[word for word in preprocess_string(doc, FILTERS) if word not in STOPWORDS]
                      for doc in raw_corpus]

        # Porter stemming
        # porter = PorterStemmer()
        # tweet_corpus = [[porter.stem(word) for word in doc] for doc in tweet_corpus]

        # Discover useful bigrams like "hot dog" via mutual information (see https://svn.spraakdata.gu.se/repos/gerlof/pub/www/Docs/npmi-pfd.pdf)
        # Bigrams will have a _ put between them (so the bigram "hot dog" will be transformed to "hot_dog")
        phrases = Phrases(preprocessed_corpus, min_count=BIGRAM_MIN_COUNT, threshold=BIGRAM_SCORE_THRESHOLD)
        tweet_corpus = phrases[preprocessed_corpus]

        dictionary = Dictionary(preprocessed_corpus)
        dictionary.compactify()

        # So we can convert BOW ids to tokens
        id2token = {bow_id:token for (token, bow_id) in dictionary.token2id.items()}

        corpus_bow = [dictionary.doc2bow(doc) for doc in preprocessed_corpus]
        
        return (dictionary, id2token, corpus_bow)

