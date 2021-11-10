#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-27 16:58:54
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 0.0.1
"""
PDF reader to count specific keywords.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pdfplumber
import os
import glob
import time
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import re

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PDF_PATH = os.path.join(ABSOLUTE_PATH, "PDF-Data", "adidas", "*")

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Analayser:
    #TODO change hardcoded kexwords to read in from file
    keywords = ['Digitalisierung',
                'Künstliche Intelligenz',
                'Technologie',
                'KI',
                'AI',
                'Internet']

    def __init__(self, directory: str) -> None:
        self.files = glob.glob(directory)
        self.company = directory.split('\\')[-2]
        self.__extracted_data = pd.DataFrame(index=self.keywords)
        self.__suspicious_pages = list()

    def analyse_company_data(self):
        for i, file in enumerate(self.files):
            self.__progressBar(i, len(self.files))
            year = re.findall(r"[0-9]{4}", file)[-1]
            file_text: str = self.__extract_text_from_pdf(file)
            self.__extract_data_from_text(file_text, year)
        self.__progressBar(len(self.files), len(self.files))
        self.__print_files_for_double_check()

    def export_data_to_excel(self):
        df = self.__get_transposed_extracted_data()
        filename = f'output_{self.company}.xlsx'
        path = os.path.join(ABSOLUTE_PATH, "extracted_data", filename)
        df.to_excel(path, engine='xlsxwriter')

    def plot_extracted_data(self, debug=True):
        df = self.__get_transposed_extracted_data()
        # bar chart
        ax = df.plot.bar(rot=0,
                        grid=True,
                        title=self.company,
                        colormap="winter",
                        figsize=(8, 4))
        ax.set_xlabel("year")
        ax.set_ylabel("occurence")
        
        # line chart
        annual_sum_up = df.sum(axis=1).reset_index()
        annual_sum_up.rename({0: "sum"}, inplace=True, axis=1)
        annual_sum_up.plot( y='sum',
                            color='orange', 
                            secondary_y=True,
                            ax=ax, 
                            xlim=ax.get_xlim(), 
                            legend=False)
        plt.ylabel('absolute occurence of technical terms',
                    rotation=-90, 
                    labelpad=15)
        plt.legend(loc='upper left')
        
        for p in ax.patches:
            ax.annotate(p.get_height(),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        size=5,
                        xytext=(0, 5),
                        textcoords='offset points'
                        # ,rotation= 90
                        )
        
        if not debug:
            filename = f'output_{self.company}.png'
            path = os.path.join(ABSOLUTE_PATH, "plots", filename)
            plt.savefig(path, dpi=250)
        plt.show()
        
    def read_in_excel_data(self, file: str) -> None:
        self.__extracted_data = pd.read_excel(
            file, index_col=0, header=0, engine='openpyxl').T

    def __extract_data_from_text(self, text: str, year: str):
        word_frequencies = list()
        for elem in self.keywords:
            word_frequencies.append(text.count(elem.lower()))
        self.__add_new_extracted_data(word_frequencies, year)

    def __extract_text_from_pdf(self, file: str) -> str:
        text = ''
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    text += '\n'+page.extract_text().lower()
                except AttributeError:
                    self.__suspicious_pages.append((file, i))
        return text

    def __get_transposed_extracted_data(self) -> pd.DataFrame:
        return self.__extracted_data.T

    def __add_new_extracted_data(self, new_data: list, year: str) -> None:
        self.__extracted_data[year] = pd.Series(new_data, index=self.keywords)
        
    def __progressBar(self, current, total, barLength=20):
        percent = float(current) * 100 / total
        arrow = '-' * int(percent/100 * barLength - 1) + '>'
        spaces = ' ' * (barLength - len(arrow))
        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
        
    def __print_files_for_double_check(self):
        if self.__suspicious_pages:
            print("There are some suspicious pages where no text was found.\nPlease double check and adjust the exported data.")
            print("                            FILE                                ||                            PAGE                                ")
            for file, page in self.__suspicious_pages:
                print(file, page)
    
    
    
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

def timing(func):
    """
    Measures working time of a function

    Parameters
    ----------
    func : function
        function where the time is measured
    """
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = func(*args, **kwargs)
        time2 = time.time()
        delta = time2-time1
        conversion = datetime.timedelta(seconds=delta)
        print(f'{func.__name__} function took {conversion}')
        return ret
    return wrap



@timing
def main(analyse_pdf = True):
    analyser = Analayser(PDF_PATH)
    if analyse_pdf:
        analyser.analyse_company_data()
    else:
        filename = f'output_{analyser.company}.xlsx'
        path = os.path.join(ABSOLUTE_PATH, "extracted_data", filename)
        analyser.read_in_excel_data(path)
    analyser.export_data_to_excel()
    analyser.plot_extracted_data(debug=False)

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    main(analyse_pdf=False)

