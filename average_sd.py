from conllu import parse
from collections import defaultdict
import statistics


class PureStatistics(object):
    def __init__(self, document, list_with_files):
        self.words_in_corpus = self.corpus_occurences(
            self.words_in_doc(document),
            list_with_files,
            )
        self.mean, self.median, self.sd_mean = self.stats(self.words_in_corpus,)

    def words_in_doc(self, document):
        frequency_dict = {}
        with open(document, "r") as fin:
            data = fin.read()
            for sentence in parse(data):
                for word in sentence:
                    if word["upostag"] != "PUNCT":
                        lemma = word["lemma"].lower()
                        frequency_dict[lemma] = []
        fin.close()
        return frequency_dict

    def corpus_occurences(self, words_in_doc, files_in_corpus,):
        for file_name in files_in_corpus:
            word_count = 0
            dict_corpus_freq = defaultdict(int)
            with open(file_name, "r") as fin:
                data = fin.read()
                for sentence in parse(data):
                    for word in sentence:
                        word_count += 1
                        lemma = word["lemma"].lower()
                        if lemma in words_in_doc:
                            dict_corpus_freq[lemma] += 1
            for k, v in words_in_doc.items():
                if k in dict_corpus_freq:
                    words_in_doc[k].append((dict_corpus_freq[k]/word_count)*1000)
                else:
                    words_in_doc[k].append(0)
        print(words_in_doc)
        return words_in_doc

    def stats(self, corpus_occurences,):
        mean_dict = {}
        median_dict = {}
        sd_mean_dict = {}
        sd_median_dict = {}
        for k, v in corpus_occurences.items():
            mean_dict[k] = statistics.mean(v)
            median_dict[k] = statistics.median(v)
            sd_mean_dict[k] = statistics.pstdev(v, mean_dict[k])
            sd_median_dict[k] = statistics.pstdev(v, median_dict[k])
            # thought the stdev would differ with median as "mean". But it gives the same values. Why?
        #print(mean_dict)
        #print(median_dict)
        #print(sd_mean_dict)
        #print(sd_median_dict)
        return mean_dict, median_dict, sd_mean_dict
