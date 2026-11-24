# # intern/ihf/

"""
/*******************************************************************************
   utils.py
This file contains all global variables that are used across the diffrent module files of the ihf folder

********************************************************************************/
"""

# # Built-in/Generic Imports
import os

# # Third Party Imports
import contextily as cx
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("CARTO_API_KEY")
p = cx.providers.CartoDB.Positron(apikey=KEY)


CRS_M = 2154
D_MAX = 500  # no forest search beyond this (m)
BUFFERS = (50, 100, 200)
R_CLUSTER = 50  # buffer radius used to group dwellings (m)

