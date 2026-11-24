# # intern/ihf/bd_forests/

"""
/*******************************************************************************
   extract.py
Here are the functions to extract the data from the vegetation files. We will use the functions in this file
to extract the data from the vegetation files and store it in a structured format for further analysis.

********************************************************************************/
"""

# # Built-in/Generic Imports
import os

# # Third Party Imports
import geopandas as gpd

# # Project Imports
from intern.ats import chargement, parametres

# # global variable

BD_FORESTS_FILE = ["../../data/forests/occupation-du-sol-region-sud-2019Polygon.shp"]


def read_bd_forests_file(path=BD_FORESTS_FILE[0]):
    """
    Function to read the vegetation file and return the data as a GeoDataFrame.
    If the file is not on the computer, it is first downloaded from its online copy.
    :param path: path to the vegetation file
    :return: GeoDataFrame
    """
    folder = os.path.dirname(path)
    filename = os.path.basename(path)
    
    filepath = chargement.telecharger_et_dezipper(parametres.URL_FORETS, folder, filename)

    gdf = gpd.read_file(filepath)
    return gdf