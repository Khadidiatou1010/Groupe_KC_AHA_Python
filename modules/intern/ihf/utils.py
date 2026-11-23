# # intern/ihf/

"""
/*******************************************************************************
   utils.py
This file contains all global variables that are used across the diffrent module files of the ihf folder

********************************************************************************/
"""

# # Third Party Imports
import contextily as cx

p = cx.providers.CartoDB.Positron(apikey="cb1_5bwe_1_9ba5234936bb78fffbab1218")


CRS_M = 2154
D_MAX = 500                      # no forest search beyond this (m)
BUFFERS = (50, 100, 200)
R_CLUSTER = 50                   # buffer radius used to group dwellings (m)

