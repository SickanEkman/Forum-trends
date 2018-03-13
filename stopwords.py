from conllu import parse
from collections import Counter
import pickle


class Stopwords():
    def __init__(self, list_with_files, directory_name, forum_nick):
        """
        Create a list with type frequencies INCLUDING punctuations
        :param list_with_files: list with paths to all conllu files in corpus
        :param directory_name: directory name, ending with "/"
        :param forum_nick: name of forum, to use for file naming
        """
        self.outfile_name = directory_name + forum_nick + "_stoplist.pkl"
        self.frequency_list = self.count_frequency(list_with_files)
        self.pickle_frequency_list(self.frequency_list, self.outfile_name)

    def count_frequency(self, files):
        """
        Count frequencies for all lemmas in corpus
        :param files: list with paths to all conllu files in corpus
        :return: list with all types in corpus, sorted descending by frequency
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
        frequency_list = sorted(
            counted,
            key=counted.__getitem__,
            reverse=True
        )
        return frequency_list

    def pickle_frequency_list(self, frequency_list, outfile_name):
        """
        pickle the frequency list and write it to file
        :param frequency_list: list with all types in corpus, sorted descending by frequency
        :param outfile_name: name of output file, including path
        :return: file with pickled frequency list
        """
        with open(outfile_name, "wb") as fout:
            pickle.dump(frequency_list, fout)
        fout.close()

