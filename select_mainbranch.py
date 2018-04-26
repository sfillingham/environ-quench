"""This is a module that contains various functions to select the main
branch of a merger tree. Specifically designed for the outputs of 
Rockstar and ConsistentTrees.

Functions
---------
tree_chunk
tree_evolution

"""

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


def tree_evolution(halocat, locationfile, forestfile, keylist=['x', 'y', 'z']):
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
    keylist : tuple
        A list of the DataFrame.keys() to be part of the ouput

    Returns
    -------
    A pd.DataFrame that contains the temporal evolution for every paramter listed
    in the keylist.

    """
    location = pd.read_table(locationfile)
    forest = pd.read_table(forestfile)
    
    haloid = halocat['Tree_root_ID(29)']
    treename = location.iloc[np.where(location['#TreeRootID'] == haloid)[0]]
    uniquetree = np.unique(treename)
    rows = np.linspace(1, 47, 47)

    for i in range(len(uniquetree)):

        filename = '/Users/tmc/bolshoi/bolshoisims/trees/'+treename
        tree = pd.read_table(filename, delim_whitespace=True, skiprows=rows)
        
    

    

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
