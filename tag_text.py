# -*- coding: utf-8 -*-
import os
import ufal.udpipe


class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []
        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)
        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""
        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()
        return output


# English: "english-ud-2.0-170801.udpipe"
# Swedish: "swedish-ud-2.0-170801.udpipe"
training_file = "swedish-ud-2.0-170801.udpipe"
directory_name = "k_months/"

model = Model(training_file)
for dirpath, dirnames, filenames in os.walk(directory_name):
    file_list = [os.path.join(dirpath, filename) for filename in filenames]
    for f in file_list:
        with open(f, "r") as fin:
            forum_text = fin.read()
            sentences = model.tokenize(forum_text)
            for s in sentences:
                model.tag(s)
            conllu = model.write(sentences, "conllu")
            outfile_name = f[9:18] + ".conllu"
            print(dirpath + outfile_name)
            with open(os.path.join(dirpath, outfile_name), "w") as fout:
                fout.write(conllu)
            fout.close()
        fin.close()
