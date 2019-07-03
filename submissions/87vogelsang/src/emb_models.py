#    Copyright (C) 2019  Jonas Winkler, Jannis Grönberg, Andreas Vogelsang
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from gensim.models import Word2Vec
import logging

class WordEmbeddingModel(object):
    def get_embeddings(self):
        raise NotImplementedError()

    def get_vocab(self):
        raise NotImplementedError()

    def get_index2word(self):
        raise NotImplementedError()

    def get_embeddings_size(self):
        return self.get_embeddings().shape[1]

    def get_vocab_size(self):
        return self.get_embeddings().shape[0]


class PretrainedGenSimWordEmbeddingModel(WordEmbeddingModel):
    def __init__(self, filename):
        logging.getLogger(__name__).info("Loading w2v model...")
        self._model = Word2Vec.load(filename)
        self._vocab = {key: value.index for (key, value) in self._model.wv.vocab.items()}

    def get_embeddings(self):
        return self._model.wv.syn0

    def get_vocab(self):
        return self._vocab

    def get_index2word(self):
        return self._model.wv.index2word


class GenSimWordEmbeddingModel(WordEmbeddingModel):
    def __init__(self, corpus_file, size, min_count, window=5, workers=3, iter=5):
        logging.getLogger(__name__).info("Loading w2v corpus...")
        with open(corpus_file, 'r', encoding='utf-8') as f:
            sentences = [l.strip().split(' ') for l in f.readlines()]
        logging.getLogger(__name__).info("Training w2v model...")
        self._model = Word2Vec(sentences, size=size, window=window, min_count=min_count, workers=workers, iter=iter)
        self._vocab = {key: value.index for (key, value) in self._model.wv.vocab.items()}

    def get_embeddings(self):
        return self._model.wv.syn0

    def get_vocab(self):
        return self._vocab

    def get_index2word(self):
        return self._model.wv.index2word
