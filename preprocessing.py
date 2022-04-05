#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
data preprocessing
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from abc import ABC, abstractmethod
import os
import string
import spacy
import re
from string import punctuation
from DataHandler.csv_handler import CsvHandler
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Preprocessor(ABC):


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        self._content: list = None
        self._suffix: str = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def content(self):
        return self._content

    @property
    def processor_type(self):
        return self._suffix

    @content.setter
    def content(self, value: list):
        self._content = value

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    @abstractmethod
    def tokenize_and_lemmatize(self, text: str) -> list:
        pass

    def save_tokens(self, company: str, year: str, subdirectory: str = None):
        token_path = os.path.join(ABSOLUTE_PATH,
                                  "ExtractedData",
                                  "ExtractedTokens",
                                  subdirectory,
                                  self._suffix,
                                  f"token_{self._suffix}_{company}_{year}.csv")
        handler = CsvHandler(token_path, self.content)
        handler.save_content()

    def read_tokens(self, company: str, year: str, subdirectory: str = None) -> list:
        token_path = os.path.join(ABSOLUTE_PATH,
                                  "ExtractedData",
                                  "ExtractedTokens",
                                  subdirectory,
                                  self._suffix,
                                  f"token_{self._suffix}_{company}_{year}.csv")
        handler = CsvHandler(token_path)
        handler.read_data()
        return handler.content

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _preprocess_text(self, text: str) -> str:
        # lower case
        text = text.lower()
        # Remove punctuation
        text = re.sub(f"[{re.escape(punctuation)}]", "", text)
        # Remove extra spaces, tabs, and new lines
        text = " ".join(text.split())
        return text


class SpacyPreprocessor(Preprocessor):


    def __init__(self):
        Preprocessor.__init__(self)
        self._suffix = 'spacy'
        self.__nlp = spacy.load("de_dep_news_trf")


    def tokenize_and_lemmatize(self, text: str) -> list:
        lemmas = []
        preprocessed_text = self._preprocess_text(text)
        # max length for model 512 tokens
        slices = slice_string(preprocessed_text, 512)
        # tokenize and lemmanize
        for seq in slices:
            doc = self.__nlp(seq)
            lemmas += [w.lemma_ for w in doc if not w.is_stop]
        self.content = lemmas
        return lemmas


class NltkPreprocessor(Preprocessor):

    def __init__(self):
        Preprocessor.__init__(self)
        nltk.download('wordnet', quiet=True)
        self._suffix = 'nltk'
        self.__lemmatizer = WordNetLemmatizer()
        self.__stopwords: set = set(
            (stopwords.words('german')) + list(string.punctuation))


    def tokenize_and_lemmatize(self, text: str) -> list:
        lemmas = []
        preprocessed_text = self._preprocess_text(text)
        # max length for model 512 tokens
        slices = slice_string(preprocessed_text, 512)
        # tokenize and lemmanize
        for seq in slices:
            doc = word_tokenize(seq)
            lemmas += [self.__lemmatizer.lemmatize(w) for w in doc if w not in self.__stopwords]
        self.content = lemmas
        return lemmas


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def slice_string(text: str, chunk_length: int) -> list:
    items = text.split(' ')
    slices = []
    while len(items) > chunk_length:
        slices.append(' '.join(items[:chunk_length]))
        items = items[chunk_length:]
    return slices

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
