#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
Excel file handler
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import pandas as pd


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.dirname(os.path.abspath('main.py'))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class ExcelHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.__content: pd.DataFrame = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: pd.DataFrame):
        self.__content = value

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def save_content(self, new_file_path: str):
        new_path = os.path.join(
            ABSOLUTE_PATH, "ExtractedData", "HeuristicData", new_file_path)
        try:
            os.makedirs(new_path)
        except FileExistsError:
            # directory already exists
            pass
        self.content.to_excel(new_path, engine="xlsxwriter")

    def read_data(self, index_column: bool = True):
        if index_column:
            self.content = pd.read_excel(
                self.file_path, index_col=0, header=0, engine='openpyxl')
        else:
            self.content = pd.read_excel(
                self.file_path, header=0, engine='openpyxl')
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
