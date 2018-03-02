import os
from conllu import parse
from collections import Counter
import math


class Tfidf():
    def __init__(self, document, list_with_file_names):
        """
        :param document: path to document of interest
        :param list_with_file_names: paths to all conllu formatted docs in corpus, NOT INCLUDING DOCUMENT OF INTEREST
        :return: prints TF*IDF for alla words in document
        """
        self.corpus_dict = self.parse_corpus_docs(list_with_file_names)
        self.document = document
        self.tf = self.count_tf(self.document)
        self.idf = self.count_idf(self.tf, self.corpus_dict)
        self.tfidf = self.count_tfidf(self.tf, self.idf)
        print(self.tfidf)

    def parse_corpus_docs(self, list_with_file_names):
        """
        extract lemma occurences (Y/N) from conllu files
        :param list_with_file_names: docs in conllu format
        :return: dict with k=filename, v=set of all lemmas in the doc
        """
        self.corpus_dict = {}
        for file_name in list_with_file_names:
            with open(file_name, "r") as fin:
                data = fin.read()
                set_words = set()
                for sentence in parse(data):
                    for word in sentence:
                        if word["upostag"] != "PUNCT":
                            set_words.add(word["lemma"])
                self.corpus_dict[file_name] = set_words
        return self.corpus_dict

    def count_tf(self, document):
        """
        extracts lemmas and counts Term Frequency from doc of interest
        :param document: path to doc of interest
        :return: dict with k=lemma, v=TF
        """
        with open(document, "r") as fin:
            data = fin.read()
            list_of_words = []
            for sentence in parse(data):
                for word in sentence:
                    if word["upostag"] != "PUNCT":
                        list_of_words.append(word["lemma"])
            counted = Counter(list_of_words)
            max_occ = max(counted.values())
            self.tf = {k: (v / max_occ) for (k, v) in counted.items()}
        fin.close()
        return self.tf

    def count_idf(self, tf, corpus_dict):
        """
        Counts Inverse Document Frequency for all word in doc of interest
        :param tf: dict with k=lemma, v=TF for doc of interest
        :param corpus_dict: dict with k=filename, v=set of all lemmas in the doc
        :return: dict with k=lemma, v=IDF for doc of interest
        """
        num_docs = len(corpus_dict) + 1
        self.idf = {}
        for word, frequency in tf.items():
            doc_occurences = 1
            for doc, word_set in corpus_dict.items():
                if word in word_set:
                    doc_occurences += 1
            self.idf[word] = math.log2(num_docs/doc_occurences)
        return self.idf

    def count_tfidf(self, tf, idf):
        """
        Counts TF*IDF for each lemma in doc of interest
        :param tf: dict with k=lemma, v=TF for doc of interest
        :param idf: dict with k=lemma, v=IDF for doc of interest
        :return: dict with k=lemma, v=TF*IDF for doc of interest
        """
        self.tfidf = {}
        for word, value in tf.items():
            self.tfidf[word] = value * idf[word]
        return self.tfidf

document = "k_months/k_2013-08.conllu"

directory_name = "k_months/"
list_with_file_strings = []
for dirpath, dirnames, f_names in os.walk(directory_name):
    for f in f_names:
        if f.endswith("conllu"):
            if f in document:
                pass
            else:
                list_with_file_strings.append(os.path.join(dirpath, f))
my_tfidf_model = Tfidf(document, list_with_file_strings)
