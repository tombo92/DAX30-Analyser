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
import csv
import os
import sys

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

    def __init__(self, file_path: str, content: list = None):
        self.file_path: str = file_path
        self.__content: list = content
        

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
        path, _ = os.path.split(self.file_path)
        try:
            os.makedirs(path)
        except FileExistsError:
            # directory already exists
            pass
        with open(self.file_path, 'w', encoding="UTF8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.content)

    def read_data(self):
        with open(self.file_path, 'r', encoding="UTF8") as csv_file:
            self.__content = sum(list(csv.reader(csv_file)), [])
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
