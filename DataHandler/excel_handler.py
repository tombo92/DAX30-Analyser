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

    def __init__(self, file_path: str = None):
        self.__file_path: str = file_path
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

    @property
    def path(self):
        return self.__file_path

    @path.setter
    def path(self, value: str):
        self.__file_path = os.path.join(
            ABSOLUTE_PATH, "ExtractedData", "HeuristicData", value)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def save_content(self, sheets: list = ['Sheet1'],
                     additional_content: list = [None]):
        writer = pd.ExcelWriter(self.__file_path, engine="xlsxwriter")
        try:
            os.makedirs(os.path.dirname(self.__file_path))
        except FileExistsError:
            # directory already exists
            pass
        contents: list = [self.content] + additional_content
        if len(contents) > len(sheets):
            sheets += [f'Sheet{i}' for i in range(len(contents) - len(sheets))]
        for i, content in enumerate(contents):
            content.to_excel(writer, sheet_name=sheets[i])
            self._auto_adjust_column_width(writer, sheets[i])
        writer.save()
        writer.close()

    def read_data(self, index_column: bool = True):
        if index_column:
            self.content = pd.read_excel(
                self.__file_path, index_col=0, header=0, engine='openpyxl')
        else:
            self.content = pd.read_excel(
                self.__file_path, header=0, engine='openpyxl')

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _auto_adjust_column_width(self, writer: pd.ExcelWriter, sheet: str):
        for column in self.content:
            column_width = max(self.content[column].astype(
                str).map(len).max(), len(column))
            col_idx = self.content.columns.get_loc(column)
            writer.sheets[sheet].set_column(col_idx, col_idx, column_width)

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
