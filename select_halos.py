"""

"""

import numpy as np
import pandas as pd
from astropy.table import Table
import grab_files as grab

def centrals(userpath, halofile, mass_range=[1.e12, 1.e15], chunk=100):
    """This function will select all halos in the simulation
    based on the mass range specified.

    Parameters
    ----------
    userpath : string
        the directory path that points to where the outputs will be stored
    halofile : string
        the input halo catalog file
    mass_range : tuple
        min_mass, max_mass

    Returns
    -------
    centrals : pd.DataFrame
        A pandas.DataFrame that contains all of the input columns

    """
    #initialize masstest
    assert mass_range[1] > mass_range[0]
    masstest = mass_range[1]

    #grab the halo catalog
    rows = [1, 47]
    read_halo = grab.reader(halofile, skiprows=rows)

    while masstest >= mass_range[0]:

        datachunk = read_halo.get_chunk(chunk)
        keys = datachunk.keys()
        
        selectcentral = np.where(np.logical_and(datachunk[keys[11]] >= mass_range[0],
                                                    datachunk[keys[11]] <= mass_range[1]))

        centralchunk = datachunk.iloc[selectcentral]
        centrals.append(centralchunk, columns=keys)

        masstest = np.min(centralchunk[keys[11]])

    centrals.to_csv(userpath+'_'+halofile+'_centrals.csv')

    return centrals
