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
class DAX30Analyser:
    """
    AI Readiness Index Analyser class
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
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
    def company(self) -> str:
        """
        getter method for company

        Returns
        -------
        str
            company name
        """
        return self.__company

    @property
    def extractor(self) -> str:
        """
        getter method for pdf_extractor

        Returns
        -------
        str
            name of the pdf extractor libary
        """
        return self.__pdf_extractor

    @extractor.setter
    def extractor(self, value: str):
        """
        setter for the pdf_extractor value

        Parameters
        ----------
        value : str
            name of the pdf extractor libary
        """
        self.__pdf_extractor = value

    @property
    def preprocessor(self) -> Preprocessor:
        """
        getter for the preprocessor

        Returns
        -------
        Preprocessor
            preprocessor type
        """
        return self.__preprocessor

    @preprocessor.setter
    def preprocessor(self, preprocessor_type: str):
        """
        setter of the preprocessor

        Parameters
        ----------
        preprocessor_type : str
            name of the preprocessor libary
        """
        if preprocessor_type == 'spacy':
            self.__preprocessor: SpacyPreprocessor = SpacyPreprocessor()
        elif preprocessor_type == 'nltk':
            self.__preprocessor: NltkPreprocessor = NltkPreprocessor()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def extract_company_data(self, pdf_directory: str):
        """
        extract the main company data out of the pdf path and sets:
        - the pathes of all files in that directory
        - the company name
        - the dataframe word_countings to its initial state

        Parameters
        ----------
        pdf_directory : str
            directory of the pdf files of one company
        """
        self.__extracted_data: pd.DataFrame = pd.DataFrame(index=self.__header)
        self.__files: list = glob.glob(pdf_directory)
        self.__company: str = pdf_directory.split('\\')[-2]
        self.__word_countings: pd.DataFrame = self.__get_word_counting_dataframe()

    def analyse_company_data(self, method: Callable, kwargs: dict):
        """
        analyse the company with a given method and gives parameters

        Parameters
        ----------
        method : Callable
            method that analyses company data
        kwargs : dict
            parameters of the given method
        """
        for file in self.__files:
            self.__current_year = re.findall(r"[0-9]{4}", file)[-1]
            kwargs['file'] = file
            method(**kwargs)
        if not self.__extracted_data.empty:
            self.__export_heuristic_data()

    def extract_text_from_pdf(self, file: str) -> str:
        """
        extracts text elements from a pdf file

        Parameters
        ----------
        file : str
            filename of the pdf

        Returns
        -------
        str
            text that is extracted
        """
        handler = PdfHandler(file)
        if self.__pdf_extractor == 'pdfplumber':
            handler.extract_data_with_pdf_plumber()
        elif self.__pdf_extractor == 'pypdf2':
            handler.extract_data_with_pypdf2()
        handler.write_to_txt_file(os.path.join(
            self.__pdf_extractor, self.__company))
        return handler.content

    def tokenize(self, file: str):
        """
        tokenizes and lemmatizes a given text and exports it as a csv file

        Parameters
        ----------
        file : str
            path of the basic pdf-file
        """
        _, file_name = os.path.split(file)
        handler = TxtHandler(file_name.replace('pdf', 'txt'))
        handler.read_data(os.path.join(self.__pdf_extractor, self.company))
        self.__preprocessor.tokenize_and_lemmatize(handler.content)
        self.__preprocessor.save_tokens(self.__company, self.__current_year, self.extractor)

    def analyse_keyword_occurences(self, _):
        """
        count the given keywords in a list of tokens

        Parameters
        ----------
        file : str
            unused variable, can not be removed
            conservation of the used Callable structure
        """
        tokens: list = self.__preprocessor.read_tokens(
            self.__company, self.__current_year, self.extractor)
        self.__heuristic_analysis(tokens)

    def create_plots(self, _):
        """
        create plots out of the statistic data

        Parameters
        ----------
        _
            unused variable, can not be removed
            conservation of the used Callable structure
        """
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
        plotter.save_figure(file_name=os.path.join(self.extractor,
                                                   self.preprocessor.processor_type,
                                                   f'output_{self.company}.png'))

    def summarize_absolute_keyword_occurence(self):
        """
        sums up the total the keyword occurence and saves it in a file
        """
        if not (self.__word_countings[self.__company] == 0).all():
            print(self.__word_countings, self.__word_countings.empty)
            handler = ExcelHandler()
            handler.path = os.path.join(self.extractor,
                                        self.preprocessor.processor_type,
                                        "KeywordFrequency",
                                        'keyword_validation.xlsx')
            handler.read_data(True)
            handler.content['Sum'] = handler.content.sum(axis=1)
            handler.save_content()

    def compare_technologies(self, file: str):
        """
        compare the used analysis technologies and sum up the results
        in plots

        Parameters
        ----------
        file: str
            unused variable, can not be removed
            conservation of the used Callable structure
        """
        path = os.path.join(ABSOLUTE_PATH, 'ExtractedData',
                            'plots', 'technology_comparison',
                            f'comparison_{self.company}.png')
        if os.path.isfile(path):
            return
        data_collection: dict = self.__collect_data_from_different_technologies()
        labels = {
            "x_label": "year",
            "y_bar_label": 'occurence',
            "y_line_label": 'total occurence'
        }
        plotter = Plotter(colormap="tab20",
                          title=self.__company,
                          data=None,
                          labels=labels,
                          suptitle='Technology Comparison')
        plotter.plot_subplots(
            2, 2, plotter.plot_bar_chart_with_sum_up, data_collection)
        plotter.save_figure(file_name=os.path.join('technology_comparison',
                                                   f'comparison_{self.company}.png'))

    def summarize_results(self, file: str):
        """
        summarize the results for different technologies and
        perform a statistic analysis (mean, std). the results
        are saved in a excel file.

        Parameters
        ----------
        file: str
            unused variable, can not be removed
            conservation of the used Callable structure
        """
        path = os.path.join(ABSOLUTE_PATH, 'ExtractedData',
                            'HeuristicData', 'statistic_data',
                            f'{self.company}.xlsx')
        if os.path.isfile(path):
            return
        data_collection: dict = self.__collect_data_from_different_technologies()
        df_concat: pd.DataFrame = pd.DataFrame()
        for technology in data_collection:
            df_concat = pd.concat(
                [df_concat, data_collection[technology]['single']])
        means: pd.DataFrame = df_concat.groupby(df_concat.index).mean()
        # (ddof=0 disables Bessel's Correction
        stds: pd.DataFrame = df_concat.groupby(df_concat.index).std(ddof=0)
        percentage_error: pd.DataFrame = stds.div(means).multiply(100)
        handler = ExcelHandler(path)
        handler.content = means
        handler.save_content(sheets=['mean', 'std', 'std in %'],
                             additional_content=[stds, percentage_error])

    def plot_summarized_results(self, file: str):
        """
        plot the data from the summarized data file

        Parameters
        ----------
        file: str
            unused variable, can not be removed
            conservation of the used Callable structure
        """
        path = os.path.join(ABSOLUTE_PATH,
                            'ExtractedData',
                            'plots',
                            'summarized',
                            f'{self.company}.png')
        if os.path.isfile(path):
            return
        handler = ExcelHandler(os.path.join(ABSOLUTE_PATH, 'ExtractedData',
                                            'HeuristicData', 'statistic_data',
                                            f'{self.company}.xlsx'))
        handler.read_data(index_column=True)
        df: pd.DataFrame = handler.content
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
        plotter.save_figure(file_name=path)

    def create_category_summary(self, file: str):
        """
        sum up the results for all companies and technologies for each
        keyword category over the time. the result is exported as a
        excel file

        Parameters
        ----------
        file: str
            unused variable, can not be removed
            conservation of the used Callable structure
        """
        handler = ExcelHandler()
        for category in self.__header:
            path = os.path.join(ABSOLUTE_PATH,
                                'ExtractedData',
                                'HeuristicData',
                                'statistic_data',
                                'summaries',
                                f'{category}_summary.xlsx')
            if os.path.isfile(path):
                continue
            data_collection: dict = self.__collect_summarized_company_data(category)
            means: pd.DataFrame = pd.DataFrame()
            stds: pd.DataFrame = pd.DataFrame()
            for key in data_collection:
                means = pd.concat(
                    [means,
                     data_collection[key]['mean']], axis=1)
                stds = pd.concat(
                    [stds, data_collection[key]['std']], axis=1)
            means['pooled_mean'] = means.mean(axis=1)
            stds['pooled_std'] = stds.mean(axis=1)
            handler.path = path
            handler.content = means
            handler.save_content(sheets=['mean', 'std'],
                                 additional_content=[stds])

    def plot_category_summary(self, file: str):
        path = os.path.join(ABSOLUTE_PATH, "ExtractedData", "plots")
        file_name = os.path.join('summarized', 'category_overview.png')
        if os.path.isfile(os.path.join(path, file_name)):
            return
        data: dict = self.__pool_summarized_company_data()
        labels = {
            "x_label": "year",
            "y_label": 'occurence'
        }
        plotter = Plotter(colormap="tab20",
                          title='Category Overview',
                          data=data,
                          labels=labels)
        plotter.plot_line_charts(error_bars=False)
        plotter.save_figure(file_name)
        file_name = os.path.join('summarized', 'category_overview_with_errors.png')
        plotter.plot_line_charts(error_bars=True)
        plotter.save_figure(file_name)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_word_counting_dataframe(self) -> pd.DataFrame:
        """
        initital state of a dataframe to count the occurence of keywords

        Returns
        -------
        pd.DataFrame
            dataframe to store heuristic data
        """
        keywords = []
        for head in self.__header:
            keywords += self.__keywords[head].tolist()
        countings = [0 for _ in range(len(keywords))]
        keywords = [k for k in keywords if isinstance(k, str)]

        return pd.DataFrame(list(zip(keywords, countings)),
                            columns=['keywords', self.__company])

    def __read_in_keywords(self, file: str) -> pd.DataFrame:
        """
        reads the keywords from the keyword file and creates a dataframe from it

        Parameters
        ----------
        file : str
            file of the keyword list

        Returns
        -------
        pd.DataFrame
            dataframe of keywords
        """
        handler = ExcelHandler(file)
        handler.read_data(index_column=False)
        return handler.content

    def __add_new_extracted_data(self, new_data: list) -> None:
        """
        adds a row to a existing dataframe with the current year as a key

        Parameters
        ----------
        new_data : list
            row of extracted data
        """
        self.__extracted_data[self.__current_year] = pd.Series(new_data, index=self.__header)

    def __heuristic_analysis(self, tokens: list):
        """
        perform a heuristic analysis and count single keywords in a list of tokens
        and also perform a total count of the keyword occurence over all tokens

        Parameters
        ----------
        tokens : list
            list of tokenized words
        """
        word_frequencies = []
        for col in self.__keywords.columns:
            if "Unnamed" not in col:
                keywords_list = self.__keywords[col].dropna().tolist()
                temp_word_frequencies = []
                for elem in keywords_list:
                    word_frequency: int = self.__count_keyword_occurence(elem, tokens)
                    temp_word_frequencies.append(word_frequency)
                    self.__word_countings.loc[self.__word_countings.keywords == elem,
                                              self.__company] += word_frequency
                word_frequencies.append(sum(temp_word_frequencies))
            else:
                break
        self.__add_new_extracted_data(word_frequencies)

    def __count_keyword_occurence(self, keyword: str, tokens: list) -> int:
        """
        counts the occurence of a given keyword in a list of tokens
        if the keyword consists out of two ore more words the tokens are
        connected to space separeted string and the keyword pattern is
        counted

        Parameters
        ----------
        keyword : str
            keyword that should be counted
        tokens : list
            list of tokenized words

        Returns
        -------
        int
            occurence of the keyword in the tokens
        """
        space_separated_key: str = keyword.replace('-', ' ')
        occurence: int = tokens.count(keyword.lower())
        if occurence == 0 and len(space_separated_key.split(' ')) > 1:
            token_string: str = ' '.join(tokens)
            occurence: int = token_string.count(space_separated_key.lower())
        return occurence

    def __export_heuristic_data(self):
        """
        exports the extracted heuristic data to xlsx files
        """
        handler = ExcelHandler()
        # export company data
        handler.path = os.path.join(self.extractor,
                                    self.preprocessor.processor_type,
                                    f'output_{self.__company}.xlsx')
        handler.content = self.__extracted_data.T
        handler.save_content()
        # export keyword validation
        handler.path = os.path.join(self.extractor,
                                    self.preprocessor.processor_type,
                                    "KeywordFrequency",
                                    'keyword_validation.xlsx')
        if os.path.isfile(handler.path):
            handler.read_data(True)

            handler.content = handler.content.join(self.__word_countings[self.__company])
        else:
            handler.content = self.__word_countings
        handler.save_content()

    def __read_heuristic_data(self) -> pd.DataFrame:
        """
        reads in the heuristic data from xlsx files and converts
        them to a dataframe

        Returns
        -------
        pd.DataFrame
            heuristic data dataframe
        """
        handler = ExcelHandler()
        handler.path = os.path.join(self.extractor,
                                    self.preprocessor.processor_type,
                                    f'output_{self.__company}.xlsx')
        handler.read_data(index_column=True)
        return handler.content

    def __collect_data_from_different_technologies(self) -> dict:
        """
        collect the data for the different used analysis technologies
        by reading the created excel data files

        Returns
        -------
        dict
            data_collection dictionary where each technology and the single/total
            data is included
        """
        data_collection: dict = {}
        technologies: dict = {
            'extractors': ['pdfplumber', 'pypdf2'],
            'preprocessors': ['nltk', 'spacy']
        }
        for extractor in technologies['extractors']:
            for preprocessor in technologies['preprocessors']:
                self.preprocessor = preprocessor
                self.extractor = extractor
                key = f"{preprocessor}/{extractor}"
                df: pd.DataFrame = self.__read_heuristic_data()
                annual_sum_up: pd.DataFrame = df.sum(axis=1).reset_index()
                annual_sum_up.rename({0: "sum"}, inplace=True, axis=1)
                data: dict = {'single': df,
                              'total': annual_sum_up}
                data_collection[key] = data
        return data_collection

    def __collect_summarized_company_data(self, category: str) -> dict:
        data_collection: dict = {}
        handler = ExcelHandler()
        companies: list = [re.findall(r"\\(.*?)\\", x)[0] for x in glob.glob("assets/PDF-Data/*/")]
        for company in companies:
            data_collection[company] = dict()
            path = os.path.join(ABSOLUTE_PATH, 'ExtractedData',
                                'HeuristicData', 'statistic_data',
                                f'{company}.xlsx')
            handler.path = path
            for sheet in ['mean', 'std']:
                handler.read_data(index_column=True, sheet_name=sheet)
                data: pd.DataFrame = handler.content[category]
                data_collection[company][sheet] = data.reset_index().rename(
                    columns={category: company, 'index': 'year'}).set_index('year')
        return data_collection

    def __pool_summarized_company_data(self) -> dict:
        handler = ExcelHandler()
        data: dict = {
            'pooled_mean': pd.DataFrame(),
            'pooled_std': pd.DataFrame()
            }
        for category in self.__header:
            path = os.path.join(ABSOLUTE_PATH,
                                'ExtractedData',
                                'HeuristicData',
                                'statistic_data',
                                'summaries',
                                f'{category}_summary.xlsx')
            handler.path = path
            handler.read_data(sheet_name='mean')
            mean = handler.content['pooled_mean'].reset_index().rename(
                columns={'pooled_mean': category}).set_index('year')
            data['pooled_mean'] = pd.concat(
                [data['pooled_mean'],
                 mean], axis=1)
            handler.read_data(sheet_name='std')
            std = handler.content['pooled_std'].reset_index().rename(
                columns={'pooled_std': category}).set_index('year')
            data['pooled_std'] = pd.concat(
                [data['pooled_std'],
                 std], axis=1)
        return data

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def compare_lists(list1: list, list2: list) -> list:
    """
    compares two given lists and returns the differences

    Parameters
    ----------
    list1 : list
        first list object
    list2 : list
        second list object

    Returns
    -------
    list
        list of the difference, if empty the lists are equal
    """
    return list(set(list1) - set(list2))


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
