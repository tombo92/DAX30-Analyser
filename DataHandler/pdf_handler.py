#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
The PdfReader class can be used to extract texts from pdf-files.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import PyPDF2
import pdfplumber
from pikepdf import Pdf

from DataHandler.txt_handler import TxtHandler


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class PdfHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.__encoded_file: str = file_path.encode('UTF-8')
        self.__content: str = None
        self.__decrypt_pdf_file(self.file_path)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def content(self):
        return self.__content

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def extract_data_with_pdf_plumber(self):
        self.__content = ''
        with pdfplumber.open(self.__encoded_file) as pdf:
            for _, page in enumerate(pdf.pages):
                try:
                    self.__content += '\n' + page.extract_text()
                except TypeError or AttributeError:
                    #TODO improve exeption handling
                    pass

    def extract_data_with_pypdf2(self):
        self.__content = ''
        with open(self.__encoded_file, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            for _, page in enumerate(reader.pages):
                try:
                    self.__content += '\n' + page.extractText()
                except Exception as e:
                    #TODO improve exeption handling
                    pass

    def write_to_txt_file(self, directory: str):
        txt_file = self.file_path.split('\\')[-1].replace('pdf', 'txt')
        handler = TxtHandler(txt_file)
        handler.content = self.content
        handler.save_content(directory)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __decrypt_pdf_file(self, file: str):
        pdf = Pdf.open(file, allow_overwriting_input=True)
        pdf.save(file)


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
