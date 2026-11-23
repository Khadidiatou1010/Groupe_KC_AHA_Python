# # intern/ihf/bd_forests/

"""
/*******************************************************************************
   plot.py
Here are the functions to plot the data from the vegetation files. We will use the functions in this file
to create visualizations of the extracted data.

********************************************************************************/
"""

# # Third Party Imports
import matplotlib.pyplot as plt
import contextily as cx

# # Module Imports
from intern.ihf.utils import p  # import the global variable positron variable p from utils.py

def plot_bd_forests_data(gdf):
    """
    Function to plot the vegetation data on a map.
    :param gdf: GeoDataFrame containing the vegetation data
    :return: None
    """
    gdf = gdf.to_crs(epsg=3857)

    ax = gdf.plot(
        figsize=(10, 10),
        facecolor="forestgreen", 
        alpha=0.6, 
        edgecolor='k',
        linewidth=0.25,
        )
    cx.add_basemap(ax, source=p)
    ax.set_axis_off()











