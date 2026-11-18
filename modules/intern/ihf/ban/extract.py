

"""
/*******************************************************************************
   extract.py
Here are the functions to extract the data from the IHF BAN files. We will use the functions in this file
to extract the data from the IHF BAN files and store it in a structured format for further analysis.

********************************************************************************/
"""

# # Built-in/Generic Imports
import os

# # Third Party Imports
import pandas as pd

# # global variable : adress files (relative to the environment in which the code is executed)
# # here the data_visualization.ipynb is the one being executed in the main/ihf directory
# # so the relative path to the data directory is ../../data/paca_adress

BAN_ADRESS_FILES = ["../../data/paca_adress/adresses-04/adresses-04.csv",
            "../../data/paca_adress/adresses-05/adresses-05.csv", 
            "../../data/paca_adress/adresses-06/adresses-06.csv", 
            "../../data/paca_adress/adresses-13/adresses-13.csv", 
            "../../data/paca_adress/adresses-83/adresses-83.csv", 
            "../../data/paca_adress/adresses-84/adresses-84.csv"]

# # read_ban_file function

def read_ban_file(path):
    """
    Function to read the IHF BAN file and return the data as a dataframe.
    :param path: path to the IHF BAN file
    :return: pandas DataFrame
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    df = pd.read_csv(path, sep=";") # sep=";" the ihf ban files are semicolon separated
    return df







