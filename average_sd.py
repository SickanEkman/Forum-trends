from conllu import parse
from collections import defaultdict
import statistics


class PureStatistics(object):
    def __init__(self, document, list_with_files):
        self.corpus_frequency_dict = defaultdict(list)
        self.doc_frequency_dict = defaultdict(int)
        self.get_corpus_word_frequencies(
            self.get_doc_word_frequencies(document, rare_threshold=3),  # where to pass the exclude argument?
            list_with_files,
            )
        self.corpus_mean = {}
        self.corpus_median = {}
        self.corpus_sd = {}
        self.get_corpus_stats(self.corpus_frequency_dict)
        self.compare_doc_and_corpus()

    def get_doc_word_frequencies(self, document, rare_threshold=0):
        """
        Gets frequency ((occurences/number words)*1000) of all words in doc and saves to self.doc_frequency_dict
        :param document: name/path to conllu file
        :param rare_threshold: minimum number of occurences in file for word to be included in analysis
        :return: self.corpus_frequency_dict with k:word-in-file, v:[] (to be modified later)
        """
        word_count = 0
        with open(document, "r") as fin:
            data = fin.read()
            for sentence in parse(data):
                for word in sentence:
                    word_count += 1
                    if word["upostag"] != "PUNCT":
                        lemma = word["lemma"].lower()
                        self.doc_frequency_dict[lemma] += 1
        fin.close()
        for k, v in self.doc_frequency_dict.items():
            if v > rare_threshold:
                self.doc_frequency_dict[k] = (v / word_count) * 1000
            else:
                self.doc_frequency_dict[k] = 0
        self.corpus_frequency_dict = dict.fromkeys([k for k, v in self.doc_frequency_dict.items()], [])
        return self.corpus_frequency_dict

    def get_corpus_word_frequencies(self, words_in_corpus, files_in_corpus, ):
        """
        Gets frequency in each file, for all words in doc
        :param words_in_corpus: dict with k:word-in-file, v:[]
        :param files_in_corpus: list of file names/paths
        :return: dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
        """
        for file_name in files_in_corpus:
            word_count = 0
            dict_corpus_freq = defaultdict(int)
            with open(file_name, "r") as fin:
                data = fin.read()
                for sentence in parse(data):
                    for word in sentence:
                        word_count += 1
                        lemma = word["lemma"].lower()
                        if lemma in words_in_corpus:
                            dict_corpus_freq[lemma] += 1
            for k, v in words_in_corpus.items():
                if k in dict_corpus_freq:
                    words_in_corpus[k] = words_in_corpus[k] + [(dict_corpus_freq[k] / word_count) * 1000]
                else:
                    words_in_corpus[k] = words_in_corpus[k] + [0]

    def get_corpus_stats(self, corpus_occurences, ):
        """
        get mean, median and (population)standard deviation for all words
        :param corpus_occurences: dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
        :return: modifies attributes dictionaries corpus_mean, corpus_median, corpus_sd
        """
        for k, v in corpus_occurences.items():
            self.corpus_mean[k] = statistics.mean(v)
            self.corpus_median[k] = statistics.median(v)
            self.corpus_sd[k] = statistics.pstdev(v, self.corpus_mean[k])  # pstdev = population standard deviation

    def compare_doc_and_corpus(self, median=False):
        """
        prints the words with frequency > mean+sd*2
        :param median: default=False. Otherwise prints words with frequency > median+sd*2
        """
        for k, v in self.doc_frequency_dict.items():
            if v > self.corpus_mean[k] + (self.corpus_sd_mean[k]*2):
                print(k)  # todo:save this somehow
            if median:
                if v > self.corpus_median[k] + (self.corpus_sd_mean[k] * 2):
                    print(k)  # todo:save this somehow
