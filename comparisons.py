# -*- coding: utf-8 -*-
import sys


"""
This module contains various text-comparison algorithms
designed to compare one statement to another.
"""

# Use python-Levenshtein if available
try:
    from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher


class Comparator:

    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare(self, statement_a, statement_b):
        return 0

    def get_initialization_functions(self):
        """
        Return all initialization methods for the comparison algorithm.
        Initialization methods must start with 'initialize_' and
        take no parameters.
        """
        initialization_methods = [
            (
                method,
                getattr(self, method),
            ) for method in dir(self) if method.startswith('initialize_')
        ]

        return {
            key: value for (key, value) in initialization_methods
        }


class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, statement, other_statement):
        """
        Compare the two input statements.

        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """

        PYTHON = sys.version_info[0]

        # Return 0 if either statement has a falsy text value
        if not statement.text or not other_statement.text:
            return 0

        # Get the lowercase version of both strings
        if PYTHON < 3:
            statement_text = unicode(statement.text.lower()) # NOQA
            other_statement_text = unicode(other_statement.text.lower()) # NOQA
        else:
            statement_text = str(statement.text.lower())
            other_statement_text = str(other_statement.text.lower())

        similarity = SequenceMatcher(
            None,
            statement_text,
            other_statement_text
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent



class JaccardSimilarity(Comparator):
    """
    Calculates the similarity of two statements based on the Jaccard index.

    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent.
    Here are two sample sentences:

        The young cat is hungry.
        The cat is very hungry.

    When we parse these sentences to remove stopwords, we end up with the following two sets:

        {young, cat, hungry}
        {cat, very, hungry}

    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.
    Given our similarity threshold above, we would consider this to be a match.

    .. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
    """

    SIMILARITY_THRESHOLD = 0.5

    def initialize_nltk_wordnet(self):
        """
        Download the NLTK wordnet corpora that is required for this algorithm
        to run only if the corpora has not already been downloaded.
        """
        from .utils import nltk_download_corpus

        nltk_download_corpus('corpora/wordnet')

    def compare(self, statement, other_statement):
        """
        Return the calculated similarity of two
        statements based on the Jaccard index.
        """
        from nltk.corpus import wordnet
        import nltk
        import string

        a = statement.text.lower()
        b = other_statement.text.lower()

        # Get default English stopwords and extend with punctuation
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.extend(string.punctuation)
        stopwords.append('')
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

        def get_wordnet_pos(pos_tag):
            if pos_tag[1].startswith('J'):
                return (pos_tag[0], wordnet.ADJ)
            elif pos_tag[1].startswith('V'):
                return (pos_tag[0], wordnet.VERB)
            elif pos_tag[1].startswith('N'):
                return (pos_tag[0], wordnet.NOUN)
            elif pos_tag[1].startswith('R'):
                return (pos_tag[0], wordnet.ADV)
            else:
                return (pos_tag[0], wordnet.NOUN)

        ratio = 0
        pos_a = map(get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(a)))
        pos_b = map(get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(b)))
        lemma_a = [
            lemmatizer.lemmatize(
                token.strip(string.punctuation),
                pos
            ) for token, pos in pos_a if pos == wordnet.NOUN and token.strip(
                string.punctuation
            ) not in stopwords
        ]
        lemma_b = [
            lemmatizer.lemmatize(
                token.strip(string.punctuation),
                pos
            ) for token, pos in pos_b if pos == wordnet.NOUN and token.strip(
                string.punctuation
            ) not in stopwords
        ]

        # Calculate Jaccard similarity
        try:
            ratio = len(set(lemma_a).intersection(lemma_b)) / float(len(set(lemma_a).union(lemma_b)))
        except Exception as e:
            print('Error', e)
        return ratio >= self.SIMILARITY_THRESHOLD


# ---------------------------------------- #


levenshtein_distance = LevenshteinDistance()
jaccard_similarity = JaccardSimilarity()
