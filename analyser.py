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

import pandas as pd
from DataHandler.excel_handler import ExcelHandler
from DataHandler.pdf_handler import PdfHandler
from DataHandler.txt_handler import TxtHandler
from preprocessing import NlpPreprocessor

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class AiriAnalyser:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        self.__keywords: pd.DataFrame = self.__read_in_keywords(
            os.path.join(ABSOLUTE_PATH, 'assets', 'keywords.xlsx'))
        self.__header: list = [
            col for col in self.__keywords.columns if "Unnamed" not in col]
        self.__extracted_data: pd.DataFrame = pd.DataFrame(index=self.__header)
        self.__read_pdf: bool = None
        self.__files: str = None
        self.__company: str = None
        self.__word_countings: pd.DataFrame = None
        self.__current_year = None
        self.__preprocessor: NlpPreprocessor = NlpPreprocessor()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def company(self):
        return self.__company

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def extract_company_data(self, directory: str, read_pdf: bool=False):
        self.__files: list = glob.glob(directory)
        self.__company: str = directory.split('\\')[-2]
        self.__word_countings: pd.DataFrame = self.__get_word_counting_dataframe()
        self.__read_pdf: bool = read_pdf

    def analyse_company_data(self, method, *args):
        for file in self.__files:
            self.__current_year = re.findall(r"[0-9]{4}", file)[-1]
            method(file, *args)

    def extract_text_from_pdf(self, file: str, pdf_plumber: bool = True) -> str:
        handler = PdfHandler(file)
        if pdf_plumber:
            handler.extract_data_with_pdf_plumber()
            handler.write_to_txt_file(os.path.join('pdfplumber', self.__company))
        else:
            handler.extract_data_with_pypdf2()
            handler.write_to_txt_file(os.path.join('pypdf2', self.__company))
        return handler.content
    
    def tokenize(self, file: str, pdf_plumber: bool = True):
        directory = 'pypdf2'
        if pdf_plumber:
            directory = 'pdfplumber'
        _, file_name = os.path.split(file)
        handler = TxtHandler(file_name.replace('pdf', 'txt'))
        handler.read_data(os.path.join(directory, self.company))
        self.__preprocessor.tokenize_and_lemmatize(handler.content)
        self.__preprocessor.save_tokens(self.__company, self.__current_year, directory)
        
            
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

    def __read_in_keywords(self, file: str) -> pd.DataFrame:
        handler = ExcelHandler(file)
        handler.read_data(index_column=False)
        return handler.content

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

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def compare_lists(list1 : list, list2: list) -> list:
    return list(set(list1) - set(list2))

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
    
