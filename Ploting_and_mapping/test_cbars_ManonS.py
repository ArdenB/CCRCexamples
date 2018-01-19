#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testing colormap alterations
"""

# load modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import BoundaryNorm

from CustomCbarsManonS import *


# plot random values
def plot(number, cmap, norm = None):

    a = np.random.random([5,5])*number

    plt.pcolormesh(a, cmap = cmap, norm = norm)
    plt.colorbar(spacing = 'proportional')

# I want to make a standard plot with all the colors
cmap = plt.cm.magma_r
plot(12, cmap)
plt.title('normal cbar')
plt.show()


# now crop the edge-colours of the cmap
cmap3 = CropCmap(cmap, 30, Ncrop2 = 70, name = 'unbalanced crop') # remove top more than bottom
plot(12, cmap3)
plt.title('cbar cropped more at the top')
plt.show()


# shift a color map
cmap = plt.cm.BrBG
plot(12, cmap)
plt.title('normal cbar')
plt.show()

cmap4 = ShiftCmap(cmap, locpoint = 0.2) # white close to the lower bound
plot(12, cmap4)
plt.title('white close to the lower bound')
plt.show()

cmap4 = ShiftCmap(cmap, locpoint = 0.8) # white close to the upper bound
plot(12, cmap4)
plt.title('white close to the upper bound')
plt.show()


# force bounds
norm = BoundaryNorm([1.2, 2.4, 5., 7., 9.8], cmap4.N)
plot(12, cmap4, norm)
plt.title('arbitrary bounds')
plt.show()
