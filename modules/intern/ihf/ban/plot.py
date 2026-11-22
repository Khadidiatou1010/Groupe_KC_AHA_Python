# # intern/ihf/ban/

"""
/*******************************************************************************
   plot.py
Here are the functions to visualize the data from the IHF BAN files. We will use the functions in this file
to create maps and visualizations of the extracted data.

********************************************************************************/
"""

# # Third Party Imports
import geopandas as gpd
import contextily as cx

# # Module Imports
from intern.ihf.utils import p  # import the global variable positron variable p from utils.py

def plot_ban_data(df):
    """
    Function to plot the IHF BAN data on a map.
    :param df: pandas DataFrame containing the IHF BAN data
    :return: None
    """
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326",
    ).to_crs(epsg=3857)

    ax = gdf.plot(markersize=2, color="red", figsize=(10, 10))
    cx.add_basemap(ax, source=p)
    ax.set_axis_off()

