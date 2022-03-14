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
from typing import Callable

import pandas as pd
from DataHandler.excel_handler import ExcelHandler
from DataHandler.pdf_handler import PdfHandler
from DataHandler.plotter import Plotter
from DataHandler.txt_handler import TxtHandler
from preprocessing import NltkPreprocessor, Preprocessor, SpacyPreprocessor

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
    def __init__(self, preprocessor_type:str="spacy"):
        self.__keywords: pd.DataFrame = self.__read_in_keywords(
            os.path.join(ABSOLUTE_PATH, 'assets', 'keywords.xlsx'))
        self.__header: list = [
            col for col in self.__keywords.columns if "Unnamed" not in col]
        self.__extracted_data: pd.DataFrame = pd.DataFrame(index=self.__header)
        self.__files: str = None
        self.__company: str = None
        self.__word_countings: pd.DataFrame = None
        self.__current_year = None
        self.__preprocessor: Preprocessor = None
        self.__pdf_extractor: str = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def company(self):
        return self.__company

    @property
    def extractor(self):
        return self.__pdf_extractor

    @extractor.setter
    def extractor(self, value:str):
        self.__pdf_extractor = value

    @property
    def preprocessor(self):
        return self.__preprocessor

    @preprocessor.setter
    def preprocessor(self, preprocessor_type:str):
        if preprocessor_type == 'spacy':
            self.__preprocessor: SpacyPreprocessor = SpacyPreprocessor()
        elif preprocessor_type == 'nltk':
            self.__preprocessor: NltkPreprocessor = NltkPreprocessor()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def extract_company_data(self, directory: str):
        self.__files: list = glob.glob(directory)
        self.__company: str = directory.split('\\')[-2]
        self.__word_countings: pd.DataFrame = self.__get_word_counting_dataframe()

    def analyse_company_data(self, method: Callable, kwargs: dict):
        for file in self.__files:
            self.__current_year = re.findall(r"[0-9]{4}", file)[-1]
            kwargs['file'] = file
            method(**kwargs)
        if not self.__extracted_data.empty:
            self.__export_heuristic_data()

    def extract_text_from_pdf(self, file: str) -> str:
        handler = PdfHandler(file)
        if self.__pdf_extractor == 'pdfplumber':
            handler.extract_data_with_pdf_plumber()
        elif self.__pdf_extractor == 'pypdf2':
            handler.extract_data_with_pypdf2()
        handler.write_to_txt_file(os.path.join(
            self.__pdf_extractor, self.__company))
        return handler.content

    def tokenize(self, file: str):
        _, file_name = os.path.split(file)
        handler = TxtHandler(file_name.replace('pdf', 'txt'))
        handler.read_data(os.path.join(self.__pdf_extractor, self.company))
        self.__preprocessor.tokenize_and_lemmatize(handler.content)
        self.__preprocessor.save_tokens(self.__company, self.__current_year, self.extractor)

    def analyse_keyword_occurences(self, file: str):
        tokens: list = self.__preprocessor.read_tokens(
            self.__company, self.__current_year, self.extractor)
        self.__heuristic_analysis(tokens)

    def create_plots(self, file: str):
        df: pd.DataFrame = self.__read_heuristic_data()
        annual_sum_up: pd.DataFrame = df.sum(axis=1).reset_index()
        annual_sum_up.rename({0: "sum"}, inplace=True, axis=1)
        data: dict = {'single': df,
                      'total': annual_sum_up}

        labels = {
            "x_label": "year",
            "y_bar_label": 'occurence',
            "y_line_label": 'absolute occurence of technical terms'
        }
        plotter = Plotter(colormap="tab20",
                          title=self.__company,
                          data=data,
                          labels=labels)
        plotter.plot_bar_chart_with_sum_up()
        plotter.save_figure(file_name=f'output_{self.company}.png')

    def compare_technologies(self):
        #TODO has to be implemented
        pass

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

    def __read_in_keywords(self, file: str) -> pd.DataFrame:
        handler = ExcelHandler(file)
        handler.read_data(index_column=False)
        return handler.content

    def __add_new_extracted_data(self, new_data: list) -> None:
        self.__extracted_data[self.__current_year] = pd.Series(new_data, index=self.__header)

    def __heuristic_analysis(self, tokens: list):
        word_frequencies = []
        for col in self.__keywords.columns:
            if not "Unnamed" in col:
                keywords_list = self.__keywords[col].dropna().tolist()
                temp_word_frequencies = []
                for elem in keywords_list:
                    word_frequency: int = tokens.count(elem.lower())
                    temp_word_frequencies.append(word_frequency)
                    self.__word_countings.loc[self.__word_countings.keywords == elem,
                                              self.__company] += word_frequency
                word_frequencies.append(sum(temp_word_frequencies))
            else:
                break
        self.__add_new_extracted_data(word_frequencies)

    def __export_heuristic_data(self):
        handler = ExcelHandler()
        # export company data
        handler.path = f'output_{self.__company}.xlsx'
        handler.content = self.__extracted_data.T
        handler.save_content()
        # export keyword validation
        handler.path = os.path.join("KeywordFrequency",
                                    'keyword_validation.xlsx')
        if os.path.isfile(handler.path):
            handler.read_data(True)
            handler.content = handler.content.join(self.__word_countings[self.__company])
        else:
            handler.content = self.__word_countings
        handler.save_content()

    def __read_heuristic_data(self) -> pd.DataFrame:
        handler = ExcelHandler()
        handler.path = f'output_{self.__company}.xlsx'
        handler.read_data(index_column=True)
        return handler.content

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

