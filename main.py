# order:
# 1. prepare_original_files. ALL FILES PREPARED ALREADY!
# 2. tag_text
# 3 create stopwords. todo: learn how to pickle!
# 4. extract!
import tag_text
from tfidf import Tfidf
from stopwords import Stopwords
import os
import rake_tfidf
from rake_only import Rake


def create_list_of_files(dir, document, skip_doc_of_interest=True):
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

def txt_file_to_string(document):
    txt_doc = document[:-6] + "txt"
    with open(document, "r") as fin:
        data = fin.read()
    fin.close()
    return data

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

directory = "t_months/"
doc_of_interest = "t_months/k_2009-01.conllu"


if __name__ == "__main__":
    pass
    #tag_forums(directory)  # language="English" if not Swedish
    list_with_conllu_files = create_list_of_files(directory, doc_of_interest)  # skip_doc_of_interest=False if not True
    stopword_list_100 = Stopwords(list_with_conllu_files, number=100).stopword_list
    print("stop1 done")
    stopword_list_200 = Stopwords(list_with_conllu_files, number=200).stopword_list
    print("stop2 done")
    stopword_list_300 = Stopwords(list_with_conllu_files, number=300).stopword_list
    print("stop3 done")
    #simple_tfidf = Tfidf(doc_of_interest, list_with_conllu_files).tfidf
    #rake_tfidf_combined(stopwords, doc_of_interest)
    text_string = txt_file_to_string(doc_of_interest)
    r1 = Rake(stopwords=stopword_list_100, language="swedish")
    r1.extract_keywords_from_text(text_string)
    print(r1.ranked_phrases)
    r2 = Rake(stopwords=stopword_list_200, language="swedish")
    r2.extract_keywords_from_text(text_string)
    print(r2.ranked_phrases)
    r3 = Rake(stopwords=stopword_list_300, language="swedish")
    r3.extract_keywords_from_text(text_string)
    print(r3.ranked_phrases)

