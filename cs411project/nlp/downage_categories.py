import numpy as np

class DownageCategories:

    @classmethod
    def calculate_word_probabilities(cls, bow_corpus, id2token, mu=0.001):
        """Calculate word probabilities for an entire corpus
        
            Parameters:
                bow_corpus: The corpus as in BOW form (list of lists)
                id2token: A Python dictionary mapping a BOW id to a token
                mu: (optional) Smoothing parameter for additive smoothing
                
            Returns:
                (tokens, word_probabilities) where
                
                    tokens: A numpy array of strings where tokens[i] is the token with BOW id i in id2token
                    word_probabilities: A numpy array of probabilities where word_probabilities[i] is the
                        probability of the token with BOW id of i occuring in the corpus
        """
        # The BOW ids and indices into corpus_wide_word_counts are the same
        num_words = len(id2token)
        corpus_wide_word_counts = np.zeros(num_words)

        for bow_doc in bow_corpus:
            for bow_tup in bow_doc:
                bow_id = bow_tup[0]
                bow_num_occurrences = bow_tup[1]

                corpus_wide_word_counts[bow_id] += bow_num_occurrences


        sum_corpus_word_count = np.sum(corpus_wide_word_counts)

        # Perform additive smoothing to avoid zero-probabilities
        word_probabilities = np.array([(count + mu) / (sum_corpus_word_count + mu*num_words) for count in corpus_wide_word_counts])
        

        tokens = np.array([id2token[idx] for idx in np.arange(num_words)])
        return (tokens, word_probabilities)

    # Return a tuple of (sorted_tokens, word_probs_of_sorted_tokens), sorting
    #   by descending probabilities
    @classmethod
    def sort_tokens_by_probability(cls, tokens, word_probs):
        sorted_order = word_probs.argsort()[::-1]
        return (tokens[sorted_order], word_probs[sorted_order])

    @classmethod
    def determine_downage_categories(cls, corpus_bow, machine_of_comment, id2token, num_categories, alpha, mu=0.0001):
        """Determine the downage categories for each machine
        
           To determine downage categories for machine M, we partition the corpus into two disjoin corpora:
            the corpus of comments made for machine M and the corpus of all other comments. 
           We then compute the probabilities of each token occuring in each corpus independently to have
            2 "vocabulary distributions"
           Then we combine the 2 vocabulary distributions into a final vocabulary distribution where
            the probability of token w is given as:
            
                p(w) = p(w, z = M)p(alpha) * p(w, z = notM)p(1-alpha)
                
            where p(w, z = M) is the probability of token w being chosen from the vocabulary distribution
            of the corpus of documents for machine M.
            
           The downage categories are the most likely num_categories tokens w.r.t. the final vocabulary distribution
            
            
            Parameters:
                corpus_bow: The complete corpus in BOW format
                machine_of_comment: An array of length len(corpus_bow) such that machine_of_comment[i] contains
                    the machine id (assumed to be numeric and in the range [1, number of total machines] )
                    that the comment of corpus_bow[i] is associated with. 
                id2token: A dictionary mapping BOW ids to tokens of the corpus
                num_categories: The number of downage categories to find for each machine
                alpha: The probability of choosing the vocabulary distribution for comments made for machine M
                    alpha > 0.5 -> Favor the vocabulary distribution for comments made for machine M
                    alpha < 0.5 -> Favor the vocabulary distribution for comments NOT made for machine M
                    Note that alpha=0.5 does not mean that we treat words from comments for machine M as equally
                        as words from all other comments (since we compute vocabulary distributions indepenently
                        for comments for machine M vs all other comments)
                mu: The psuedocount to use for additive smoothing. Set to 0 for no smoothing
                
            Returns: 
                A numpy array s.t. the i'th element contains a tuple (category_tokens, word_probs) for the machine with 
                the i'th smallest id where
                    category_tokens: The tokens associated with the top num_categories downage categories
                    word_probs: The probabilities in the final vocabulary distribution for each token in category_tokens
        """
        
        # np.unique() already sorts the unique values it finds
        all_machine_ids = np.unique(machine_of_comment)

        
        downage_categories = []
        
        for M_id in all_machine_ids:
            # Split corpus based on whether the comments were made for machine M or not
            M_corpus = np.array(corpus_bow)[machine_of_comment == M_id]
            notM_corpus = np.array(corpus_bow)[machine_of_comment != M_id]
            
            sorted_tokens, sorted_word_probs = DownageCategories._determine_downage_categories_for_machine(
                M_corpus,
                notM_corpus,
                id2token,
                alpha,
                mu
            )
            
            downage_categories.append((sorted_tokens[:num_categories], sorted_word_probs[:num_categories]))
            
            
        return np.array(downage_categories)
            

    @classmethod
    def _determine_downage_categories_for_machine(cls, M_corpus, notM_corpus, id2token, alpha, mu):
        """Helper function to return the combined vocabulary distribution, sorted in descending order of probability
        
            Parameters:
                M_corpus: The BOW corpus for all comments made for machine M
                notM_corpus: The BOW corpus for all comments NOT made for machine M
                id2token: See determine_downage_categories
                alpha: See determine_downage_categories
                mu: See determine_downage_categories
                
            Returns:
                The tuple (sorted_tokens, sorted_word_probs) where
                    sorted_tokens: All of the tokens of the combined vocabulary distribution, sorted in descending
                        order of probability
                    sorted_word_probs: The probabilities for each token in sorted_tokens
        """

        # Note that tokens_M and token_not_M refer to the same list of tokens since they both use the same id2token
        tokens_M, word_probs_M = DownageCategories.calculate_word_probabilities(M_corpus, id2token, mu=mu)
        tokens_not_M, word_probs_not_M = DownageCategories.calculate_word_probabilities(notM_corpus, id2token, mu=mu)

        # Probability of choosing each topic distribution
        topic_probs = np.array([alpha, (1 - alpha)])

        # A list of lists, where vocabulary_probabilities[i][j] gives the probability
        #   of choosing token j using topic distribution i
        #
        # Note that the inner arrays should be referencing the same vocabulary
        # (e.g. vocabulary_probabilities[i][j] and vocabulary_probabilities[k][j] 
        #    contain the probability of selecting the SAME token j from topics i and k, respectively)
        vocabulary_probabilities = np.array([word_probs_M, word_probs_not_M])
        combined_vocabulary_probs = topic_probs.dot(vocabulary_probabilities)
        
        return DownageCategories.sort_tokens_by_probability(tokens_M, combined_vocabulary_probs)

