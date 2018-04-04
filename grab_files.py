import numpy as np
import pandas as pd
from astropy.table import Table

def reader(filename, skiprows):
    """
    """
    rows = np.linspace(skiprows[0], skiprows[1], skiprows[1])
    reader = pd.read_table(filename, delim_whitespace=True, skiprows=rows, iterator=True)
    
    return reader


def data(filename, skiprows=[1, 57], chunk=10):
    """
    """
    read_data = reader(filename, skiprows)
    data_chunk = read_data.get_chunk(chunk)

    return data_chunk
