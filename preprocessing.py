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
import os
import spacy
import re
from string import punctuation
from DataHandler.csv_handler import CsvHandler


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class NlpPreprocessor:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self):
        self.__nlp = spacy.load("de_dep_news_trf")
        self.__content: list = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: list):
        self.__content = value

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def tokenize_and_lemmatize(self, text: str) -> list:
        lemmas = []
        preprocessed_text = self.__preprocess_text(text)
        # max length for model 512 tokens
        slices = slice_string(preprocessed_text, 512)
        # tokenize and lemmanize
        for seq in slices:
            doc = self.__nlp(seq)
            lemmas += [w.lemma_ for w in doc if not w.is_stop]
        self.content = lemmas
        return lemmas
    
    def save_tokens(self, subdirectory: str=None):
        token_path = os.path.join(ABSOLUTE_PATH,
                                  "ExtractedData",
                                  "ExtractedTokens",
                                  subdirectory,
                                  f"token_{self.__company}_{self.__current_year}.csv")
        handler = CsvHandler(token_path)
        handler.save_content(self.contenttokens)

    def read_tokens(self) -> list:
        token_path = os.path.join(ABSOLUTE_PATH,
                                  "ExtractedData",
                                  "ExtractedTokens",
                                  f"token_{self.__company}_{self.__current_year}.csv")
        handler = CsvHandler(token_path)
        handler.read_in_csv_data()
        return handler.content

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __preprocess_text(self, text: str) -> str:
        # lower case
        text = text.lower()
        # Remove punctuation
        text = re.sub(f"[{re.escape(punctuation)}]", "", text)
        # Remove extra spaces, tabs, and new lines
        text = " ".join(text.split())
        return text

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
