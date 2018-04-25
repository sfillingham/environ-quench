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

def reader(filename, skiprows=[1, 57]):
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


def data(reader, chunk=100):
    """Creates a pandas DataFrame that is a subset of the entire file
    based on chunk

    Parameters
    ----------
    reader : pd.DataFrame
        A pandas.DataFrame, use grab_files.reader
    chunk : int
        The number of rows to grab in the first chunk.
        Future versions will allow this to be looped over to work through the entire file.

    Returns
    -------
        pd.DataFrame that is a subset of the entire file
    """
    data_chunk = reader.get_chunk(chunk)

    return data_chunk



