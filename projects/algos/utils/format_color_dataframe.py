"""
Main script for small utility functions for the algos.
"""

import pandas as pd
import numpy as np
from termcolor import colored


def color_dataframe(df):
    # Define the color map
    color_map = {1: 'green', -1: 'red'}

    # Create a new dataframe with colored values
    colored_df = df.applymap(lambda x: colored(x, color_map.get(x, 'white')))

    return colored_df

def color_algo1_loop(list_of_dfs):
    # Apply the color_dataframe function to each dataframe in the list
    colored_dfs = []
    for df in list_of_dfs:
        colored_df = color_dataframe(df)
        colored_dfs.append(colored_df)
    return colored_dfs



