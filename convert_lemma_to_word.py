from conllu import parse
from collections import defaultdict


class MapLemmas():
    def __init__(self, document):
        self.document = document
        self.temporary_mapping_dict = self.save_mapping(self.document)
        self.mapping_dict = {}
        self.count_most_common(self.temporary_mapping_dict)

    def save_mapping(self, document):
        """
        Saves all forms of word mapped to same lemma
        :param document: path/name of conllu file
        :return: dict with k:lemma, v:[type1, type2, type2, type1, type3, ...]
        """
        dict_lemma_to_form = defaultdict(lambda:defaultdict(int))
        with open(document, "r") as fin:
            data = fin.read()
            for sentence in parse(data):
                for word in sentence:
                    if word["upostag"] != "PUNCT":
                        lemma = word["lemma"].lower()
                        not_lemma = word["form"].lower()
                        dict_lemma_to_form[lemma][not_lemma] += 1
        fin.close()
        return dict_lemma_to_form

    def count_most_common(self, temporary_mapping_dict):
        """
        Save the most common original form of word mapped to each lemma
        :param temporary_mapping_dict: dict with k:lemma, v:[type1, type2, type2, type1, type3, ...]
        :return: dict with k:lemma, v:the-most-common-form-present-in-the-doc
        """
        for k, v in temporary_mapping_dict.items():
            s = sorted(v, key=v.get, reverse=True)
            self.mapping_dict[k] = s[0]
