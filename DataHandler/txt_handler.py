#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
Short Introduction
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.dirname(os.path.abspath('main.py'))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class TxtHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.__content: str = None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: str):
        self.__content = value

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def read_data(self, directory: str = ''):
        path = os.path.join(
            ABSOLUTE_PATH, "ExtractedData", "ExtractedTexts", directory)
        with open(os.path.join(path, self.file_path), "r", encoding="utf-8") as text_file:
            self.__content = text_file.read()

    def save_content(self, directory: str = ''):
        new_path = os.path.join(
            ABSOLUTE_PATH, "ExtractedData", "ExtractedTexts", directory)
        try:
            os.makedirs(new_path)
        except FileExistsError:
            # directory already exists
            pass
        with open(os.path.join(new_path, self.file_path), "w", encoding="utf-8") as text_file:
            text_file.write(self.content)
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
