"""This is a module that contains various functions to select the main
branch of a merger tree. Specifically designed for the outputs of 
Rockstar and ConsistentTrees.

Functions
---------
tree_chunk
tree_evolution

"""

import numpy as np
import pandas as pd

def tree_chunk(halochunk, location, forest):
    """Given a halo TreeRootID identify and grab the appropriate tree data
    in order to construct the evolutionary history of the halo properties.

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
    treename = location['Filename'].iloc[np.where(location['#TreeRootID'] == haloid)[0]].iloc[0]
    filename = '/Users/tmc/bolshoi/bolshoisims/trees/'+treename
    treechunk = data(filename, chunk=25)

    return treechunk


def tree_evolution(halocat, locationfile, forestfile, filename, keylist=['x', 'y', 'z']):
    """Given a list of halos in the halocat, this will return the evolution of the parameters
    listed in the keylist.

    Parameters
    ----------
    halocat : pd.DataFrame
    locationfile : string
        The directory and file that contains the mapping between the
        TreeRootID and the merger tree file
    forestfile : string
        Same as locationfile except for the forest
    filename : string
        The name of the output file that will be saved
    keylist : tuple
        A list of the DataFrame.keys() to be part of the ouput

    Returns
    -------
    output : pd.DataFrame
        A pd.DataFrame that contains the temporal evolution for every paramter listed
        in the keylist.

    """
    location = pd.read_table(locationfile)
    forest = pd.read_table(forestfile)
    
    haloid = halocat['Tree_root_ID(29)']
    treename = location.iloc[np.where(location['#TreeRootID'] == haloid)[0]]
    uniquetree = np.unique(treename)
    print(len(uniquetree))
    rows = np.linspace(1, 47, 47)

    #define empty dictionary that will contain all of the mainbranches
    dictionary = {}

    for i in range(len(uniquetree)):
        print(uniquetree[i])
        halos = halocat.iloc[np.where(haloid == uniquetree[i])[0]]
        treeID = halos['Tree_root_ID(29)']
        lastleafID = halos['Last_mainleaf_depthfirst_ID(34)']
        
        filename = '/Users/tmc/bolshoi/bolshoisims/trees/'+uniquetree[i]
        tree = pd.read_table(filename, skiprows = np.linspace(1, 47, 47), delim_whitespace=True)

        for j in range(len(halos)):
            print(treeID[j])
            branch = tree.iloc[np.where(np.logical_and(treeID[j] == tree['Tree_root_ID(29)'],
                                                           lastleafID[j] == tree['Last_mainleaf_depthfirst_ID(34)']))[0]]

            mainbranch = branch.iloc[np.where(branch['mmp?(14)'] == 1)[0]]

            cols = ['#scale(0)', 'id(1)', 'mvir(10)', 'rvir(11)', 'rs(12)',
                        'vmax(16)', 'x(17)', 'y(18)', 'z(19)', 'vx(20)', 'vy(21)', 'vz(22)']

            mainsubset = mainbranch[cols].copy()
            mainsubset_label = mainsubset['id(1)'].iloc[0]

            dictionary[np.str(mainsubset_label)] = mainsubset

    #concatenate the dictionary into a pd.DataFrame
    output = pd.concat(dictionary)

    #write the output DataFrame to a csv file
    output.to_csv(filename)

    return output

#Identify host halos, i.e. above 1.e13
#Identify subhalos for every host halo
#Match all halos to a tree file via location.dat
#Select first tree file and read in
#Loop through all halos in this tree file
##select halo
##select main branch using mmp? and Last_mainleaf_depthfirst_ID
##trim DataFrame of unneccesary columns
##output DataFrame in host directory
#
#select halo
#Grab Tree_root_ID - map to tree_X_Y_Z.dat using location.dat
#select main branch using mmp? and Last_mainleaf_depthfirst_ID
#
