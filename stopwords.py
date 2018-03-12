from conllu import parse
from collections import Counter


class Stopwords():
    def __init__(self, list_with_files, number=100):
        """
        Creates a list with stopwords INCLUDING punctuation
        :param list_with_files: list with paths to all conllu files in corpus
        :param number: Number stopwords to extract, default=100
        """
        self.files = list_with_files
        self.frequency_dict = self.count_frequency(self.files)
        self.stopword_list = self.create_stopwords(self.frequency_dict, number)

    def count_frequency(self, files):
        """
        Count frequencies for all lemmas in corpus
        :param files: list with paths to all conllu files in corpus
        :return: dict with k=lemma, v=total number occurences in corpus
        """
        list_of_words = []
        for file in files:
            with open(file, "r") as fin:
                data = fin.read()
                for sentence in parse(data):
                    for word in sentence:
                        list_of_words.append(word["lemma"])
            fin.close()
        counted = Counter(list_of_words)
        return counted

    def create_stopwords(self, frequency_dict, number):
        """
        Pick the n number lemmas for stopword
        :param frequency_dict: dict with k=lemma, v=total number occurences in corpus
        :param number: number stopwords to extract, default=100
        :return: list with n number stopwords (lemmas)
        """
        frequency_list = sorted(
                                frequency_dict,
                                key=frequency_dict.__getitem__,
                                reverse=True
                                )
        stoplist = frequency_list[:number]
        return stoplist
