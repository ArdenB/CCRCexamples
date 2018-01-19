#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some example's of good and bad plotting practices
	
Resources:
	For all the great color paletes for python, got to
	https://jiffyclub.github.io/palettable/

	For more infomation about which colormaps are safe, see
	http://colorbrewer2.org/
	Note: all colorbrewer colormaps are in the palettable package

	For general infomation about map making see:
	http://gisgeography.com/map-elements-how-to-guide-map-making/
	http://www.esri.com/news/arcuser/0911/making-a-map-meaningful.html

	For a detailed guide to mapmaking see the Mapbox guide pdf in the repo
"""
__title__ = "Plotting and map making"
__author__ = "Arden Burrell"
__version__ = "1.0 (19.01.2018)"
__email__ = "arden.burrell@unsw.edu.au"


#==============================================================================

# general modules
import os, sys # check for files and so on
import numpy as np # array manipulations

# plotting modules 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mpc
from matplotlib import ticker
# import matplotlib as mpl
import pdb
# for mapping 
from mpl_toolkits.basemap import Basemap

# for all the awesome color palets!!!!!!!!!!
import palettable 

#==============================================================================
# =========== Main function ==========

def main():
	"""

	Call the demonstration functions in order

	"""
	# Show the mapping of years 
	yearmapper()

	# Map a variable that diverges
	divergingmap()
	
	# Map a variable that is in groups
	groupmap()

	# Map a variable that is sequental 
	sequentialmap()


#==============================================================================
# =========== plotting functions ==========
def mapper(
	image, cmap, vmin, vmax, region="global", title=None, 
	tks=False, tckstr=None, norm=False, nancolour='dimgrey'
	):
	"""
	A general mapping function that can be used to generate many different
	map types  
	"""

	# ===== set the spatial cordinates of the grid, mask the ocean and draw coastlines =====
	# Note: 
	# 	because all of the imput datastes are numpy arrays, the lon and lat bounds 
	# 	and the spatial projection (epsg) are hard coded. This infomation can be 
	# 	can be pulled automitically from nectdf, geoTif's and other raster data
	if region == "global":
		# Set the map frame
		map = Basemap(llcrnrlon=-180.0,llcrnrlat=-90.0,urcrnrlon=180,urcrnrlat=90.0, resolution = 'h', epsg=4326)
		#adds national borders 
		map.drawcountries() 
	elif region == "australia":
		# Set the map frame
		map = Basemap(llcrnrlon=112.0,llcrnrlat=-44.5,urcrnrlon=156.25,urcrnrlat=-10, resolution = 'h', epsg=4326)
		map.drawlsmask(land_color='none', )
	elif region == "mongolia":
		# Set the map frame
		map = Basemap(llcrnrlon=85.0,llcrnrlat=40,urcrnrlon=120,urcrnrlat=52, resolution = 'h', epsg=4326)
		map.drawlsmask(land_color='none', )
		# Draw national borders with a thicker line
		map.drawcountries(linewidth = 1.25) 
	else:
		sys.exit("Unknown Grid region")
	# Set the color or NaN's in the data
	map.drawmapboundary(fill_color=nancolour) #used to be grey
	# For land data, it is usefull to mask lakes etc
	map.fillcontinents(color= 'none', lake_color='white')
	# Add all of the coastlines to the map
	map.drawcoastlines()
	# Add the US and Australian state lines (Doesn't yet support other counteries)
	map.drawstates()

	# ====== Add mpc.BoundaryNorm made custom cmaps =====
	if norm == False:
		map.imshow(np.flipud(image), cmap=cmap, vmin=vmin, vmax=vmax)
	else:
		map.imshow(np.flipud(image), cmap=cmap, vmin=vmin, vmax=vmax, norm=norm)
	
	cb = map.colorbar()
	
	# ===== Move and adjust the number and location of colorbar ticks =====
	if tks == False:
		tick_locator = ticker.MaxNLocator(nbins=20)
	elif type(tks)==int:
		tick_locator = ticker.MaxNLocator(nbins=tks)
	else:
		tick_locator = ticker.MaxNLocator(nbins=vmax-vmin)
	# Add the changes to the colorbar
	cb.locator = tick_locator
	cb.update_ticks()

	# ===== Overwrite the tick labels and replace them with user defined =====
	if tckstr is not None:
		cb.ax.set_yticklabels(tckstr) 

	# ===== add in the Graticules (lon lat grid lines) ======
	if region == "global":
		map.drawparallels(np.arange(-90, 90, 10),labels=[1,0,0,0], dashes=[1,2])
		map.drawmeridians(np.arange(-180, 180, 20),labels=[0,0,0,1], dashes=[1,2])
	elif region == "australia":
		map.drawparallels(np.arange(-50, -10, 10),labels=[1,0,0,0], dashes=[1,2])
		map.drawmeridians(np.arange(110, 156.25, 10),labels=[0,0,0,1], dashes=[1,2])
	elif region == "mongolia":
		map.drawparallels(np.arange(40, 60, 5),labels=[1,0,0,0], dashes=[1,2])
		map.drawmeridians(np.arange(80, 120, 5),labels=[0,0,0,1], dashes=[1,2])
	
	# ===== Show the plot =====
	plt.show()


def yearmapper():
	"""
	Demonstrate how to map a variable where there a many subdevisions,
	in this case the years of a breakpoint detected by the TSS.RESTREND method
	applied to GIMMSv3.1g NDVI data over mongolia. 

	In this data:
		- Nan values mean the method failed
		- 0 value means that the method detected no breakpoints
		- else: the year in which a ecosystem breakpoint occured 
	"""

	# Load the data from a numpy array 
	mong_bp = np.load("./Data/Mongolia_breakpoint_years.npy")

	# ===== Make a naive plot =====
	# Comments: this plot is meant to be terrible, 
	# 	All the values that are relevant are hidden
	# 	There is no colorbar
	
	# Set the figure number
	#	This isnt strictly nessary, but usefull if you 
	# 	want to generate multiple plots then show them together 
	plt.figure(1) 
	# Make the plot
	plt.imshow(mong_bp)
	plt.show()

	pdb.set_trace()
	
	# ===== Make a slightly less terrible one =====
	# Comments: this plot easier to read but not a map 
	# 	Added bounds, and a much better colormap
	# 	The colormap is still continuous (hard to read)
	
	#Hard code the start and end years, (these can be determined automatically) 
	vmin = 1987
	vmax = 2011
	# Get a colormap thats a bit better and tweak it
	cmap = plt.cm.jet 
	cmap.set_under('w') #sets values <vmin to white in the plot
	cmap.set_bad('dimgrey') 

	# Create the image

	plt.imshow(mong_bp, vmin = vmin, vmax = vmax, cmap=cmap)
	plt.colorbar()
	plt.show()
	pdb.set_trace()

	# ===== Turn this into a proper map with a segmented colorbar =====
	plt.figure(2) 
	# Comments: Now its an actual map
	# 	Segmented colorbars are easier to read
	# 	The colormap is still continuous (hard to read)

	# +++++ turn a continuous colormap into a segmented one ++++
	# The continuous color map 
	cmap = plt.cm.jet
	# extract all colors from the cmap
	cmaplist = [cmap(i) for i in range(cmap.N)]
	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
	# Define the coverage and segments (max values, min values, number of segments)
	bounds = np.linspace(vmin, vmax, vmax-(vmin-1))
	# Select the colors for each bound using BoundaryNorm function
	norm = mpc.BoundaryNorm(bounds, cmap.N)
	# set pixels below the vmin to color to be white
	cmap.set_under('w')
	# cmap.set_above('w') # set colors above the vmax value to a color
	tks = (vmax-vmin)/2+1
	
	# +++++ Pass the data and infomation the mapper function +++++
	mapper(mong_bp, cmap, vmin, vmax, region="mongolia", tks=tks, norm=norm)

	# Note: There is almost no reason to use Jet in science, 
	# this is one of very few exceptions. Use palettable ones instead!!!!! 

def divergingmap():
	"""
	Demonstrate how to map a variable where the values diverge,
	in this case,  the total change in NDVI between 1982-2015 as 
	detected by the TSS.RESTREND method	applied to GIMMSv3.1g NDVI
	data. 

	In this data:
		- Nan values mean the method failed
		- -1 values have no statistically significant change in vegetation
		- else: total change in NDVI (note:NDVI is normalised between 0 and 1) 
	"""

	# ===== Load the data from a numpy array =====
	TC = np.load("./Data/Global_total_change.npy")

	# ===== setup the mapping variables =====
	# set the min and max
	vmax = 0.3
	vmin = -0.3
	# Grab a diverging colormap from palettable
	cmap = mpc.ListedColormap(palettable.colorbrewer.diverging.PiYG_10.mpl_colors)
	# set the color of values of pixels with no significant change (have been set to -1)
	cmap.set_under('w')
	# This number needs to be adjusted to get the ticks tp line up
	tks=11

	# Generate the map 
	mapper(TC, cmap, vmin, vmax, region="global", tks=tks)
	pdb.set_trace()

def sequentialmap():
	"""
	Demonstrate how to map a variable where the values are sequential.
	in this case,  the p between NDVI and rainfall detected by the 
	TSS.RESTREND method	applied to GIMMSv3.1g NDVI data. 

	In this data:
		- NaN values mean the method failed
		- else: and Rsquared value between 0 and 1 
	"""

	# ===== Load the data from a numpy array =====
	pval = np.load("./Data/Global_pval.npy")
	
	# ===== setup the mapping variables =====
	# set the min and max
	vmax = 1
	vmin = 0
	# Grab a sequential colormap from palettable
	cmap=mpc.ListedColormap(palettable.cmocean.sequential.Thermal_20_r.mpl_colors)
	# set the color of values of pixels with no significant change (have been set to -1)
	# cmap.set_under('w')
	# set the number of ticks
	tks=21
	
	# ===== Generate the map =====
	mapper(pval, cmap, vmin, vmax, region="global", tks=tks)

	# Note: 
	# 	This is a terrible plot. Hopefully MS will
	# 	update the script with a function that allows 
	#	colormas to be scalled. 

	pdb.set_trace()

def groupmap():
	"""
	Demonstrate how to map a variable where the values are in 
	classified groups. in this case,  the comparison of TSS.RESTREND 
	direction between GIMMSv3.1g NDVI and VOD data. 

	In this data:
		- The numbers refer to groups (0 - 8)
	"""

	# ===== Load the data from a numpy array =====
	groups = np.load("./Data/Global_classes.npy")
	# show what the data looks like
	plt.imshow(groups)
	plt.colorbar()
	plt.show()
	
	# ===== setup the mapping variables =====
	# set the min and max
	vmin = -0.5
	vmax = 8.5
	# Create the labels
	label2=['No Change', 'Both Dec', 'Both Inc','NDVI Inc, VOD Dec','NDVI Inc, VOD stable', 'NDVI stable, VOD Dec','VOD Inc, NDVI Dec', 'VOD Inc, NDVI stable', 'VOD stable, NDVI Dec']
	# Create a custom discrete colourmap from hex values 
	cmaphex = ['#d1cdca','#AF0627', '#ffffff','#1a9850', '#91cf60','#d9ef8b','#6a51a3','#9e9ac8', '#cbc9e2'] 
	cmap = mpc.ListedColormap(cmaphex)
	# Set the color under
	cmap.set_under('w')
	
	# ===== Generate the map =====
	mapper(groups, cmap, vmin, vmax, region="global", tks=True, tckstr = label2)
	
	pdb.set_trace()



if __name__ == '__main__':
	main()