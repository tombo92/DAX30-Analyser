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
from typing import Callable
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
import pandas as pd


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.dirname(os.path.abspath('main.py'))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Plotter:
    """
    Class to create plots out of pd.Dataframes
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self,
                 colormap: str,
                 title: str,
                 data: dict,
                 labels: dict,
                 suptitle: str = None):
        self.colormap: str = colormap
        self.title: str = title
        self.data: dict = data
        self.labels: dict = labels
        self.figsize: tuple = (8, 4)
        self.line_color: str = 'orange'
        self.suptitle: str = suptitle

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def plot_bar_chart_with_sum_up(self, axis: plt.axes = None):
        ax = self.__plot_bar_chart(x_label=self.labels["x_label"],
                                   y_label=self.labels["y_bar_label"],
                                   data=self.data['single'],
                                   axis=axis)
        self.__plot_line_chart(x_label=self.labels["x_label"],
                               y_label=self.labels["y_line_label"],
                               data=self.data['total'],
                               axis=ax)

        # Create empty plot with blank marker containing the extra label
        ax.plot([], [], color=self.line_color, label="in total")

        # Shrink current axis's height by 20% on the bottom
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.2,
                         box.width, box.height * 0.8])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.175),
                  fancybox=True, shadow=True, ncol=5)

    def plot_subplots(self, rows: int, colums: int, method: Callable, data_collection: dict):
        fig, axs = plt.subplots(rows, colums)
        plt.suptitle(f"{self.suptitle}: {self.title}" , fontsize="x-large")
        for i in range(rows):
            for j in range(colums):
                key = list(data_collection.keys())[i * rows + j]
                self.data = data_collection[key]
                method(axis=axs[i, j])
                axs[i, j].legend().set_visible(False)
                axs[i, j].tick_params(axis="x", rotation=30)
                if j == 0:
                    plt.ylabel('')


        axs[i, j].legend(loc='upper center', bbox_to_anchor=(-0.1, -0.6),
                         fancybox=True, shadow=True, ncol=5)

        for i, ax in enumerate(axs.flat):
            ax.set_title('')
            x_info, y_info = list(data_collection.keys())[i].split('/')
            ax.set(xlabel=x_info,
                   ylabel=y_info)

        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()

        fig.supxlabel(self.labels["x_label"])
        fig.supylabel(self.labels["y_bar_label"])

    def show(self):
        plt.show()

    def save_figure(self, file_name: str):
        path = os.path.join(ABSOLUTE_PATH, "ExtractedData", "plots")
        try:
            os.makedirs(path)
        except FileExistsError:
            # directory already exists
            pass
        plt.savefig(os.path.join(path, file_name),
                    dpi=300, bbox_inches='tight')
        plt.close()

    def plot_line_charts(self, error_bars=False):
        df = self.data['pooled_mean']
        if error_bars:
            errors = self.data['pooled_std']
            ax = df.plot(colormap=self.colormap,
                         figsize=self.figsize,
                         xticks=df.index,
                         grid=True,
                         title=self.title)
            for i, category in enumerate(list(df)):
                ax.fill_between(
                    df.index,
                    df[category] - errors[category],
                    df[category] + errors[category],
                    alpha=0.25 + 0.05*i,
                    color=ax.get_lines()[i].get_color())
        else:
            df.plot(colormap=self.colormap,
                    figsize=self.figsize,
                    xticks=df.index,
                    grid=True,
                    title=self.title)
        plt.ylabel(self.labels['y_label'])
        plt.xlabel(self.labels['x_label'])


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
                         data: pd.DataFrame,
                         axis: plt.axes = None) -> plt.axes:
        ax = data.plot.bar(rot=0,
                           grid=True,
                           title=self.title,
                           colormap=self.colormap,
                           figsize=self.figsize,
                           ax=axis)
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
