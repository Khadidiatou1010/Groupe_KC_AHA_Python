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

# # global variable

BD_FORESTS_FILE = ["../../data/vegetation/occupation-du-sol-region-sud-2019Polygon.shp"]


def read_bd_forests_file(path):
    """
    Function to read the vegetation file and return the data as a GeoDataFrame.
    :param path: path to the vegetation file
    :return: GeoDataFrame
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    gdf = gpd.read_file(path)
    return gdf












