#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
main terminal outputs and interaction
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import time
import glob
import os
from analyser import AiriAnalyser


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
COMPANIES = glob.glob("assets/PDF-Data/*/")
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Application:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        self.__icon: str = self.__read_icon()
        self.__seperator: str = "="*100
        self.__exit: dict = {'r': ['Return', 'Return to previous dialog.'],
                             'x': ['Exit', 'Exit the programm.']
                             }
        self.__options1: dict = {
            '1': ['Data Preprocessing', 'Read and tokenize the data from the pdf-files.'],
            '2': ['Data Analysis', 'Perform a heuristic analysis with the given keywords and the previously created tokens.'],
            '3': ['Data Plotting', 'Plot the previously extracted heuristic data.']
        }
        self.__options2: dict = {
            '1': ['Read PDF (pdfplumber)', "Read in the pdf data with the 'pdfplumber'-library and save as txt-file."],
            '2': ['Read PDF (PyPDF2)', "Read in the pdf data with the 'PyPDF2'-library and save as txt-file."],
            '3': ['Tokenize With NLP', 'Read in the previously extracted texts and lemmatize & tokenize them and save as csv-file.'],
            '4': ['Compare pdfpumber and PyPDF2', 'Read in the previously extracted tokens of both extracted texsts and compare them.'],
            
        }
        self.__options3: dict = {
            '1': ['Start Analysis', 'Perform a heuristic analysis with the given keywords and the previously created tokens.']
        }
        self.__options4: dict = {
            '1': ['Start Plotting', 'Plot the previously extracted heuristic data.']
        }
        self.__options: list = [self.__options1,
                                self.__options2,
                                self.__options3,
                                self.__options4]

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def init_dialog(self):
        is_start_dialog: bool = None
        level: int = 0
        memory: int = level
        user_input: str = None
        print(self.__icon)
        print(self.__seperator)
        while True:
            print("Options: ")
            is_start_dialog = False
            if level == 0:
                is_start_dialog = True
            self.__print_options(self.__options[level], is_start_dialog)
            user_input = input("Please choose an option: ")
            if user_input == '?':
                self.__print_options(
                    self.__options[level], is_start_dialog, 1)
            elif user_input == 'x':
                if self.__quit_program():
                    break
            elif user_input == 'r' and not is_start_dialog:
                level = 0
            elif self.__is_input_valid(user_input, self.__options[level].keys()):
                level = int(user_input)
            if level > 0 and not is_start_dialog:
                print('\n' + self.__seperator)
                self.__execute_program(memory, level)
                print(self.__seperator)
                print("Finished...\n")
                level = 0
            memory = level

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __print_single_option(self, key, value):
        print(f"   [{key}]\t:   {value}")

    def __read_icon(self) -> str:
        icon_path = os.path.join(ABSOLUTE_PATH, 'assets', 'icon.txt')
        with open(os.path.join(icon_path), "r", encoding="utf-8") as text_file:
            icon: str = text_file.read()
        return "          " + icon.strip()

    def __print_options(self, options: dict, is_start_dialog: bool, print_help: bool = False):
        index: int = 0
        if print_help:
            index = 1
        for key in options:
            self.__print_single_option(key, options[key][index])
        self.__print_single_option('?', 'Help')
        if not is_start_dialog:
            self.__print_single_option('r', self.__exit['r'][index])
        self.__print_single_option('x', self.__exit['x'][index])

    def __is_input_valid(self, input_data: str, valid_input: list) -> bool:
        if input_data in valid_input:
            return True
        print('Invalid input.')
        return False

    def __quit_program(self) -> bool:
        while True:
            user_input = input(
                'Do you really want, to exit the program?[y/n] ')
            if user_input in ['y', 'yes']:
                return True
            elif user_input in ['n', 'no']:
                return False
            else:
                print("Invalid input. Please enter 'y'/'yes' or 'n'/'no'.")

    def __execute_program(self, first_value: int, second_value: int):
        analyser = AiriAnalyser()
        durations = []
        method: function = None
        if first_value == 1:
            if second_value == 1:
                print(f"{self.__options2['1'][0]}...")
                method: function = analyser.extract_text_from_pdf
                args = True
            elif second_value == 2:
                print(f"{self.__options2['2'][0]}...")
                method: function = analyser.extract_text_from_pdf
                args = False
            elif second_value == 3:
                print(f"{self.__options2['3'][0]}...")
                while True:
                    user_input = input("Choose between pdfplumber [1] or PyPDF2 [2]: ")
                    if self.__is_input_valid(user_input, ['1', '2']):
                        break
                if user_input == '1':
                    method: function = analyser.tokenize
                    args = True
                elif user_input == '2':
                    method: function = analyser.tokenize
                    args = False
        if method == None:
            print('Need to be implemented, please choose other option :)')
            return
        for i, company in enumerate(COMPANIES):
            start = time.time()
            progressBar(i, len(COMPANIES), 
                        duration=estimate_time(durations, len(COMPANIES)-i))
            company_path = os.path.join(ABSOLUTE_PATH, company, "*")
            analyser.extract_company_data(company_path)
            analyser.analyse_company_data(method, args)
            end = time.time()
            durations.append(int(end-start))
        progressBar(len(COMPANIES), len(COMPANIES),
                    duration=estimate_time(durations, 0))


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def progressBar(current, total, barLength=20, duration: str = 'unknown'):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d %%\tEstimated Excution Time: %s' %
          (arrow, spaces, percent, duration), end='\r')

def estimate_time(durations: list, number_of_iterations_left: int) -> str:
    if durations:
        left_duration = int(sum(durations)/len(durations) * number_of_iterations_left)
        return time.strftime('%H:%M:%S', time.gmtime(left_duration))
    return 'unknown'

def main():
    app = Application()
    app.init_dialog()

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    main()


