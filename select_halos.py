"""This module has various functions that allow the user to 
choose halos in an N-body simulation using various selection
criteria.

Functions
---------
centrals
subhalos

"""

import numpy as np
import pandas as pd
from astropy.table import Table
import grab_files as grab

def centrals(userpath, halofile, mass_range=[1.e12, 1.e15], chunk=100):
    """This function will select all halos in the simulation
    based on the mass range specified.
    This function assumes the halocatalogs are sorted by virial mass.

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
        A pandas.DataFrame that contains all of the input columns for the 
        selected central halos.

    """
    assert mass_range[1] > mass_range[0]
    i = 0

    #grab the halo catalog
    rows = [1, 57]
    read_halo = grab.reader(halofile, skiprows=rows)
    halo_name = halofile.split('/')[-1]

    #chunk size to test against
    size=chunk

    while chunk == size:

        datachunk = read_halo.get_chunk(chunk)
        keys = datachunk.keys()
        
        selectcentral = np.where(np.logical_and(datachunk['mvir(10)'] > mass_range[0],
                                                    datachunk['mvir(10)'] < mass_range[1]))[0]

        centralchunk = datachunk.iloc[selectcentral]
        
        if i == 0:
            centralgals = centralchunk
        else:
            centralgals = centralgals.append(centralchunk)
        
        i += 1

        print(i)
        chunk = len(datachunk)

    snapshot_sname = snapshot_name.split('.')
    snapshotname = snapshot_sname[0]+'.'+snapshot_sname[1]
    print(haloname)
    centralgals.to_csv(userpath+snapshotname+'_centralhalos.csv')

    return centralgals


def satellites(userpath, halofile, hostfile, mass_range=[1.e10, 1.e14],
                   distlimit=1.0, chunk=100):
    """This function will select all satellites in the simulation
    based on the mass range specified and proximity to the host.
    This function assumes the halocatalogs are sorted by virial mass.

    Parameters
    ----------
    userpath : string
        the directory path that points to where the outputs will be stored
    halofile : string
        the input halo catalog file
    hostfile : string
        the input list of centrals to be used as the host locations
    mass_range : tuple
        min_mass, max_mass
    distlimit : float
        The maximum distance a halo can reside to be considered a satellite.
    chunk : float
        The number of lines to read in at a time.

    Returns
    -------
    satellites : pd.DataFrame
        A pandas.DataFrame that contains all of the input columns for the 
        selected satellite halos.

    """
    assert mass_range[1] > mass_range[0]
    i = 0

    #grab the halo catalog
    rows = [1, 57]
    read_halo = grab.reader(halofile, skiprows=rows)
    snapshot_name = halofile.split('/')[-1]
    snapshot_sname = snapshot_name.split('.')
    snapshotname = snapshot_sname[0]+'.'+snapshot_sname[1]

    #grab central galaxy catalog
    centrals = pd.read_csv(hostfile)
    xcentral = centrals['x(17)'].values.reshape(len(centrals), 1)
    ycentral = centrals['y(18)'].values.reshape(len(centrals), 1)
    zcentral = centrals['z(19)'].values.reshape(len(centrals), 1)
    rvir = centrals['rvir(11)'].values.reshape(len(centrals), 1)
    xone = np.ones_like(xcentral)
    yone = np.ones_like(ycentral)
    zone = np.ones_like(zcentral)

    #chunk size to test against
    size=chunk

    while chunk == size:

        datachunk = read_halo.get_chunk(chunk)
        keys = datachunk.keys()

        satmass = datachunk['mvir(10)'].values.reshape(len(datachunk), 1)
        masscut = np.logical_and(satmass > mass_range[0],
                                     satmass < mass_range[1])

        x = datachunk['x(17)'].values.reshape(len(datachunk), 1)
        y = datachunk['y(18)'].values.reshape(len(datachunk), 1)
        z = datachunk['z(19)'].values.reshape(len(datachunk), 1)
        xmat = np.dot(x, xone.T)
        ymat = np.dot(y, yone.T)
        zmat = np.dot(z, zone.T)

        dx = xmat.T - xcentral
        dy = ymat.T - ycentral
        dz = zmat.T - zcentral

        dist = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        normdist = dist * 1000.0 / rvir

        distcut = normdist <= distlimit
        
        selectsatellite = np.where(np.logical_and(masscut.T, distcut))
        print(selectsatellite[1].shape)
        satchunk = datachunk.iloc[selectsatellite[1]]
        
        if i == 0:
            satellitegals = satchunk
        else:
            satellitegals = satellitegals.append(satchunk)
        
        i += 1

        print(i)
        chunk = len(datachunk)

    
    satellitegals.to_csv(userpath+snapshotname+'_satellitehalos_'+np.str(distlimit)+'Rvir.csv')

    return satellitegals
