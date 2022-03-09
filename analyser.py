#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
airi data analyser
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import glob
import os
import re
from string import punctuation

import pandas as pd
from DataHandler.excel_handler import ExcelHandler
from DataHandler.pdf_handler import PdfHandler
from DataHandler.txt_handler import TxtHandler
from main import ABSOLUTE_PATH
import spacy
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class AiriAnalyser:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, read_pdf: bool):
        self.__keywords: pd.DataFrame = self.__read_in_keywords(
            os.path.join(ABSOLUTE_PATH, 'assets', 'keywords.xlsx'))
        self.__header: list = [
            col for col in self.__keywords.columns if "Unnamed" not in col]
        self.__extracted_data: pd.DataFrame = pd.DataFrame(index=self.__header)
        self.__read_pdf: bool = read_pdf
        self.__nlp = spacy.load("de_dep_news_trf")
        self.__files: str = None
        self.__company: str = None
        self.__word_countings: pd.DataFrame = None
        self.__current_year = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def extract_company_data(self, directory: str):
        self.__files: list = glob.glob(directory)
        self.__company: str = directory.split('\\')[-2]
        self.__word_countings: pd.DataFrame = self.__get_word_counting_dataframe()

    def analyse_company_data(self):
        """
        start analysis for the company data:
            - if the text from pdf is already extracted
              the ressource is a txt file
            - else extract the text from the pdf, write it to
              a txt file and analyse it
        """
        for file in self.__files:
            self.__current_year = re.findall(r"[0-9]{4}", file)[-1]
            file_text: str = ''
            if self.__read_pdf:
                file_text = self.__extract_text_from_pdf(file)
            else:
                file_text = self.__extract_text_from_txt(file)
            tokens = self.__tokenize_with_nlp(file_text)
            self.__heuristic_analysis(tokens)
            break
        #self.__print_files_for_double_check()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_word_counting_dataframe(self) -> pd.DataFrame:
        keywords = []
        for head in self.__header:
            keywords += self.__keywords[head].tolist()
        countings = [0 for i in range(len(keywords))]
        keywords = [k for k in keywords if isinstance(k, str)]

        return pd.DataFrame(list(zip(keywords, countings)),
                            columns=['keywords', self.__company])

    def __extract_text_from_txt(self, file: str) -> str:
        txt_file = file.split('\\')[-1].replace('pdf', 'txt')
        handler = TxtHandler(txt_file)
        handler.extract_data(self.__company)
        return handler.content

    def __extract_text_from_pdf(self, file: str) -> str:
        handler = PdfHandler(file)
        handler.extract_data_with_pdf_plumber()
        handler.write_to_txt_file(self.__company)
        return handler.content

    def __read_in_keywords(self, file: str) -> pd.DataFrame:
        handler = ExcelHandler(file)
        handler.read_in_excel_data(index_column=False)
        return handler.content

    def __tokenize_with_nlp(self, text: str) -> list:
        lemmas = []
        preprocessed_text = self.__preprocess_text(text)
        # max length for model 512 tokens
        slices = slice_string(preprocessed_text, 512)
        # tokenize and lemmanize
        for seq in slices:
            doc = self.__nlp(seq)
            lemmas += [w.lemma_ for w in doc if not w.is_stop]
        return lemmas

    def __heuristic_analysis(self, tokens: list):
        print(tokens)
        return
        word_frequencies = list()
        for col in self.__keywords.columns:
            if not "Unnamed" in col:
                keywords_list = self.__keywords[col].dropna().tolist()
                temp_word_frequencies = list()
                for elem in keywords_list:
                    word_frequency: int = tokens.count(elem.lower())
                    temp_word_frequencies.append(word_frequency)
                    self.__word_countings.loc[self.__word_countings.keywords == elem,
                                            self.__company] += word_frequency
                word_frequencies.append(sum(temp_word_frequencies))
            else:
                break
        self.__add_new_extracted_data(word_frequencies)

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
    for company in glob.glob("assets/PDF-Data/*/"):
        company_path = os.path.join(ABSOLUTE_PATH, company, "*")
        analyser = AiriAnalyser(False)
        analyser.extract_company_data(company_path)
        analyser.analyse_company_data()

        break
