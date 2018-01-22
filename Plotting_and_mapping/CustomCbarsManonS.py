# -*- coding: utf-8 -*-

""" basic color bar alterations
"""


# modules
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap


# functions

def CropCmap(cmap, Ncrop, Ncrop2 = None, name = 'cropped cmap'):

    """ crop the edges of a cmap (remove extremes) to make it more readable
    """

    # new cmap index list to compute the colors from
    if Ncrop2 is None:
        cmaplist = np.linspace(float(Ncrop)/cmap.N, 1. - float(Ncrop)/cmap.N)

    if Ncrop2 is not None:
        cmaplist = np.linspace(float(Ncrop)/cmap.N, 1. - float(Ncrop2)/cmap.N)

    return LinearSegmentedColormap.from_list(name, cmap(cmaplist))


def ShiftCmap(cmap, start = 0., locpoint = 0.5, stop = 1.0, name = 'centered'):

    """ shift the colours to associate a value standing anywhere in the new cmap
    (relatively to the two extremes start & stop or min & max) with whichever
    value / colour of the input cmap (by default the midpoint).
    If the input cmap is divergent, this will be white by default.
    The locpoint value cannot be the min or max (start or stop).
    """

    # declare a colour + transparency dictionary
    cdict={'red':[], 'green':[], 'blue':[], 'alpha':[]}

    # regular index to compute the colors
    RegInd = np.linspace(start, stop, cmap.N)

    # shifted index to match what the data should be centered on
    ShiftInd = np.hstack([np.linspace(0., locpoint, cmap.N/2, endpoint = False),
                        np.linspace(locpoint, 1., cmap.N/2, endpoint = True)])

    # associate the regular cmap's colours with the newly shifted cmap colour
    for RI, SI in zip(RegInd, ShiftInd):

        # get standard indexation of red, green, blue, alpha
        r, g, b, a = cmap(RI)

        cdict['red'].append((SI, r, r))
        cdict['green'].append((SI, g, g))
        cdict['blue'].append((SI, b, b))
        cdict['alpha'].append((SI, a, a))

    return LinearSegmentedColormap(name, cdict)
