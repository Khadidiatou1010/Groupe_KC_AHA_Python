# # intern/ihf/analysis/

"""
/*******************************************************************************
   utilities.py
In this file, we will define the utility functions that are used in the analysis of the IHF data. 
These functions will be used to process the data and extract useful information 
from it for the analysis notebook.

********************************************************************************/
"""

# # Third Party Imports
import numpy as np
import geopandas as gpd
import contextily as cx

from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


# # get the nearest polygon from a set of polygons to a set of points
def nearest(points, polys, dmax=None, cols=("geometry",)):
    j = gpd.sjoin_nearest(points[["geometry"]], polys[list(cols)], how="left",
                          max_distance=dmax, distance_col="d")
    return j[~j.index.duplicated()]  # ties create duplicates

# # get the share of forest within a buffer around each point
def forest_share(pts, forest_typed, r):
    buf = pts[["geometry"]].copy()
    buf["geometry"] = buf.buffer(r, resolution=8)
    buf["pid"] = buf.index
    inter = gpd.overlay(buf, forest_typed[["lib3_19", "geometry"]],
                        how="intersection", keep_geom_type=True)
    inter["a"] = inter.area
    share = (inter.groupby("pid")["a"].sum() / buf.area).reindex(pts.index).fillna(0)
    dom = (inter.groupby(["pid", "lib3_19"])["a"].sum().reset_index()
                .sort_values("a").drop_duplicates("pid", keep="last")
                .set_index("pid")["lib3_19"])
    return share, dom.reindex(pts.index)

# # identify clusters of points based on spatial proximity
def cluster_size(xy, r):
    tree = cKDTree(xy)
    pairs = tree.query_pairs(2 * r, output_type="ndarray")   # buffers overlap iff distance <= 2r
    A = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(xy),) * 2)
    _, lab = connected_components(A, directed=False)
    return np.bincount(lab)[lab], lab












