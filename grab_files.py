"""This is a module that contains various functions to read in and parse relatively large 
data files. Specifically designed for the outputs of Rockstar and ConsistentTrees.

Functions
---------
reader
data
"""

import numpy as np
import pandas as pd
from astropy.table import Table

def reader(filename, skiprows):
    """Creates a reader object to parse a large data file

    Parameters
    ----------
    filename : string
    skiprows : tuple
        A tuple that contains the min and max row to skip, (min, max)
        All rows in between those value will be omitted from the reader object.

    Returns
    -------
        A pandas object that can be accessed in chunks via reader.get_chunk(size)
    """
    rows = np.linspace(skiprows[0], skiprows[1], skiprows[1])
    reader = pd.read_table(filename, delim_whitespace=True, skiprows=rows, iterator=True)
    
    return reader


def data(filename, skiprows=[1, 57], chunk=10):
    """Creates a pandas DataFrame that is a subset of the entire file

    Parameters
    ----------
    filename : string
    skiprows : tuple
        A tuple that contains the min and max row to skip, (min, max)
        All rows in between those value will be omitted from the reader object.
    chunk : int
        The number of rows to grab in the first chunk.
        Future versions will allow this to be looped over to work through the entire file.

    Returns
    -------
        pd.DataFrame that is a subset of the entire file
    """
    read_data = reader(filename, skiprows)
    data_chunk = read_data.get_chunk(chunk)

    return data_chunk


def tree_chunk(halochunk, location, forest):
    """
    Parameters
    ----------
    halochunk : pd.DataFrame
    location : pd.DataFrame
    forest : pd.DataFrame

    Returns
    -------
        treechunk : pd.DataFrame
        The chunk of the entire tree file
    """

    haloid = halochunk['Tree_root_ID(29)']
    filename = location['Filename'].iloc[np.where(location['#TreeRootID'] == bighalo['Tree_root_ID(29)'])[0]].iloc[0]

    treechunk = data(filename, chunk=25)

    return treechunk
