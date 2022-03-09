#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-03-07 18:49:42
# @Author  : Liadan & Tom
# @Python  : 3.8.6
# @Link    : link
# @Version : 2.0.0
"""
data plotter
"""
# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
from main import ABSOLUTE_PATH
import matplotlib.pyplot as plt
import pandas as pd


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Plotter:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, colormap: str, title: str, data: dict, labels: dict):
        super().__init__()
        self.colormap: str = colormap
        self.title: str = title
        self.data: dict = data
        self.labels: dict = labels
        self.figsize: tuple = (8, 4)
        self.line_color: str = 'orange'

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def plot_bar_chart_with_sum_up(self):
        ax = self.__plot_bar_chart(x_label=self.labels["x_label"],
                                   y_label=self.labels["y_bar_label"],
                                   data=self.data['single'])
        self.__plot_line_chart(x_label=self.labels["x_label"],
                               y_label=self.labels["y_line_label"],
                               data=self.data['total'],
                               axis=ax)

        # Create empty plot with blank marker containing the extra label
        ax.plot([], [], color=self.line_color, label="line")
        ax.legend(loc='upper left')

    def show(self):
        plt.show()

    def save_figure(self, file_name: str):
        path = os.path.join(ABSOLUTE_PATH, "ExtractedData", "plots", file_name)
        plt.savefig(path, dpi=250)
        plt.close()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __plot_line_chart(self,
                          x_label: str,
                          y_label: str,
                          data: pd.DataFrame,
                          axis: plt.axes = None):
        xlim = None
        if axis:
            xlim = axis.get_xlim()
        data.plot(y='sum',
                  color=self.line_color,
                  secondary_y=True,
                  ax=axis,
                  xlim=xlim,
                  legend=False)
        plt.ylabel(y_label, rotation=-90, labelpad=15)
        plt.xlabel(x_label)

    def __plot_bar_chart(self,
                         x_label: str,
                         y_label: str,
                         data: pd.DataFrame) -> plt.axes:
        ax = data.plot.bar(rot=0,
                           grid=True,
                           title=self.title,
                           colormap=self.colormap,
                           figsize=self.figsize)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        self.__position_bar_chart_labels(axis=ax)
        return ax

    def __position_bar_chart_labels(self, axis: plt.axes):
        for p in axis.patches:
            axis.annotate(p.get_height(),
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center',
                          size=5,
                          xytext=(0, 5),
                          textcoords='offset points')


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass