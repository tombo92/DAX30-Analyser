#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
csv file handler
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import csv

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class CsvHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, file_path: str):
        self.file_path: str = file_path
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
    def save_content(self):
        with open(self.file_path, 'w', encoding="UTF8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.content)

    def read_in_excel_data(self, index_column: bool = True):
        with open(self.file_path, 'r', encoding="UTF8") as csv_file:
            self.__content = csv.reader(csv_file)
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
