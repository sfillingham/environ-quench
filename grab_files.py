import numpy as np
import pandas as pd
from astropy.table import Table

def reader(filename, skiprows=[1, 57]):
    """
    """
    rows = np.linspace(skiprows[0], skiprows[1], skiprows[1])
    reader = pd.read_table(filename, delim_whitespace=True, skiprows=rows, iterator=True)
    
    return reader


