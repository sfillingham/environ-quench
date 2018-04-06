"""This module will contain the general quenching model class and all 
specific quenching model classes.

More description to follow once this module has been fully developed.
Needs more work...
"""

import numpy as np
import pandas as pd
from astropy.table import Table
from astropy.cosmology import LambdaCDM
cosmo = LambdaCDM(H0=70, Om0=0.3, Ode0=0.7)

class quenching_models:
    """General quenching model class.

    """

    def __init__(self):

        return self
