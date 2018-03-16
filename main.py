# order:
# 1. prepare_original_files. ALL FILES PREPARED ALREADY!
# 2. tag_text
# 3 create stopwords.
# 4. extract!
import tag_text
from tfidf import PureTfidf
from stopwords import Stopwords
import os
import rake_tfidf
from rake_only import Rake
import pickle
from conllu import parse
from average_sd import PureStatistics
from convert_lemma_to_word import MapLemmas

def create_list_of_files(dir, document, skip_doc_of_interest=True):
    """
    create list with file names of files to be analyzed in methods
    :param dir: the directory name, ending with "/"
    :param document: the full path/name of document of interest # todo: make this param optional
    :param skip_doc_of_interest: If True, doc will not be included in final list
    :return: list with file names (str)
    """
    list_with_file_strings = []
    for dirpath, dirnames, f_names in os.walk(dir):
        for f in f_names:
            if f.endswith("conllu"):
                if skip_doc_of_interest:
                    if f in document:
                        pass
                    else:
                        list_with_file_strings.append(os.path.join(dirpath, f))
                elif not skip_doc_of_interest:
                    list_with_file_strings.append(os.path.join(dirpath, f))
                else:  # This shouldn't happen
                    print("Eh, do u want to skip the document or not?")
    if len(list_with_file_strings) > 0:
        return list_with_file_strings
    else:
        print("No conllu files in directory")
        return None

def txt_file_to_string(conllu_doc):
    """
    Convert txt-file content to a string, to be sent to analyze
    :param conllu_doc: the full path/name of corresponding conllu document in same folder as .txt # todo: this seems stupid, change this
    :return: a string with content of the document of interest
    """
    txt_doc = conllu_doc[:-6] + "txt"
    with open(txt_doc, "r") as fin:
        data = fin.read()
    fin.close()
    return data

def conllu_file_to_string(conllu_doc):
    """
    Convert conllu-file content to a string, to be sent to analyze
    :param conllu_doc: the full path/name of conllu document to be converted
    :return: a string with content of the document of interest
    """
    with open(conllu_doc, "r") as fin:
        data = fin.read()
        fin.close()
        list_words = []
        for sentence in parse(data):
            for word in sentence:
                list_words.append(word["lemma"])
        conllu_as_string = " ".join(list_words)
        return conllu_as_string

def unpickle_stopwords(directory, forum_nick, number=100):
    """
    :param directory: the directory name, ending with "/"
    :param forum_nick: The forum name, ex "t"
    :param number: number of words in the resulting stoplist. Default = 100
    :return: list with n number of stop words
    """
    filename = directory + forum_nick + "_stoplist.pkl"
    try:
        with open(filename, "rb") as fin:
            frequency_list = pickle.load(fin)
            fin.close()
            stoplist = frequency_list[:number]
            return stoplist
    except FileNotFoundError:
        print("Can't find '%s' in directory '%s'" % (filename, directory))

def tag_forums(directory, language="Swedish"):
    """
    Perform POS-tagging for files
    :param directory: relative path to directory with .txt files
    :param language: default = Swedish. Optional = English
    :return: saves conllu file for each file, in same directory
    """
    if language == "Swedish":
        tag_text.create_tagged_files("swedish-ud-2.0-170801.udpipe", directory)
    elif language == "English":
        tag_text.create_tagged_files("english-ud-2.0-170801.udpipe", directory)
    else:
        print("No language model found")

def rake_tfidf_combined(stopwords, doc_of_interest):
    pass
    #todo: continue here! Maybe..?

forum_nick = "t"
directory = forum_nick + "_months/"
doc_of_interest = directory + forum_nick + "_2016-09.conllu"


if __name__ == "__main__":
    #tag_forums(directory)  # language="English" if not Swedish
    #list_with_conllu_files = create_list_of_files(directory, doc_of_interest,)
                                                                # skip_doc_of_interest=False if not True
    #Stopwords(list_with_conllu_files, directory, forum_nick,)
    #stopword_list = unpickle_stopwords(directory, forum_nick,)  # number=x if not 100

    MapLemmas(doc_of_interest)

    #simple_tfidf = PureTfidf(doc_of_interest, list_with_conllu_files,).tfidf
    #txt_as_string = txt_file_to_string(doc_of_interest, )
    #conllu_as_string = conllu_file_to_string(doc_of_interest)

    #simple_rake = Rake(stopwords=stopword_list, language="swedish",)
    #simple_rake.extract_keywords_from_text(conllu_as_string,)
    #print(simple_rake.ranked_phrases,)
    #PureStatistics(doc_of_interest, list_with_conllu_files)
    #todo: everything above is working!
    # rake_tfidf_combined(stopwords, doc_of_interest,)
