"""
NetCDF Builder
This is currently a test script and will eventuall be made into a module

"""
#==============================================================================

__title__ = "netCDF maker"
__author__ = "Arden Burrell (Manon's original code modified)"
__version__ = "v1.0(02.03.2018)"
__email__ = "arden.burrell@gmail.com"

#==============================================================================
# Set to go up two levels to TSSRESTREND folder
import os
os.chdir('../../')
#==============================================================================

# load modules for netcdf
import scipy.io.netcdf as nc
import collections
import datetime

# Load modules for the files
import numpy as np
from collections import OrderedDict

# Load modules for debugging
import pdb
# +++++ Import plotting and colorpackages +++++
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib as mpl
import palettable 

#==============================================================================
def main():
	# Create a blank object to hold my info
	ncinfo = netCDF_info() #call the class

	# =========== load the numpy array ===========
	DEMarray = np.load("./Input_data/DEM/GMTED/data/Global_DEM_at_GIMMS.npy")
	# plot the data
	plt.style.use('classic')
	cmap = mpc.ListedColormap(
		palettable.matplotlib.Viridis_20.mpl_colors
		)
	plt.imshow(DEMarray, vmin=0, vmax=5000, cmap=cmap)
	plt.colorbar()
	plt.show()

	# =========== Expand the DIMS ===========
	DEMarray3d = np.expand_dims(DEMarray, axis=0)

	# =========== Grab lats and lons from an exising netcdf ===========
	# NOTE: this netcdf is the exact shape i want to make
	file_name  = './Input_data/DEM/GMTED/data/10N000E_20101117_gmted_mea075_at_GIMMS.nc'
	lat_arr, lon_array = nc_getLatsandLons(file_name)


	# =========== Add info ===========
	# The data i want to save
	ncinfo.data        = DEMarray3d
	# File name to save into
	ncinfo.fname       = "./Input_data/DEM/GMTED/data/Global_DEM_GMTED_at_GIMMS.nc"
	# The name of the variable to be savesd
	ncinfo.var_name    = "DEM"
	ncinfo.var_lname   = "Height_Above_Mean_Sea_Level"
	# Number of lats
	ncinfo.lat         = 2160
	# number of lons
	ncinfo.lon         = 4320
	# Fill value, really important for CDO 
	ncinfo.fill        = -99999.0
	# Units of my variable (Meters above sea level in this case)
	ncinfo.units       = "m"
	# The dates (This needs work)
	ncinfo.dates       = datetime.datetime.strptime('20100101','%Y%m%d')
	# Array of the latitudes
	ncinfo.latitudes   = lat_arr
	# Array of the longitudes
	ncinfo.longitudes  = lon_array
	# Add Description
	ncinfo.description = "Global DEM regrided from the GMTED2012 2010 250m data using CDO remapcon2"
	# Add the history (This needs work)
	ncinfo.history     = "Created " + datetime.datetime.today().strftime("%y/%m/%d")

	# =========== Create the netcdf file ===========
	write_netcdf(ncinfo)
	

#==============================================================================
def nc_getLatsandLons(fn):
	""" 
	This takes a netcdf fill and pulls out the lat and lons array
	var:
		fn, The name of a file to open
	return:
		lats, np array of the latitude
		lons, np array of the longitude
	"""
	from netCDF4 import Dataset
	# load the netcdf file
	ncf1 = Dataset(fn, mode='r')

	# Pull out the lon and lat data
	lats = ncf1.variables["lat"][:]
	lons = ncf1.variables["lon"][:]

	return lats, lons

class netCDF_info(object):
	"""
	A class to store the netcdf infomation. 
	The goal is to move this calls to its own script in the
	nc module once i have it working.  
	"""
	def __init__(self): #(self, arg)
		# self.arg = arg
		# These are none, later i will add ways to automitaccly fill this data
		self.data        = None
		self.fname       = None
		self.var_name    = None
		self.var_lname   = None
		self.lat         = None
		self.lon         = None
		self.fill        = None
		self.units       = None
		self.dates       = None
		self.latitudes   = None
		self.longitudes  = None
		self.description = None
		self.history     = None
		
def date_range(start_date, end_date):
	# define time vector
	start_date=datetime.datetime.strptime(start_date,'%Y%m%d.%f')
	end_date=datetime.datetime.strptime(end_date,'%Y%m%d.%f')
	current=[start_date+datetime.timedelta(days=x) for x in range((end_date-start_date).days+1)]
	current=[t.strftime('%Y%m%d.%f') for t in current]
	return current

def write_netcdf(ncinfo):
	""" setup and save a netcdf file
	var:
		object of my created class netCDF_info
	"""
	# ========== Create new netcdf ==========
	NAME=nc.netcdf_file(ncinfo.fname,'w')
	
	# ========== Set up the Dimensions ==========
	NAME.createDimension('time', None) #Question: Shouldn't time be unlimited?
	# NAME.createDimension('lev',11)
	NAME.createDimension('lat',ncinfo.lat)
	NAME.createDimension('lon',ncinfo.lon)
	
	# ========== Setup the Variables ==========
	time=NAME.createVariable('time',np.float64,('time',))
	# lev=NAME.createVariable('lev',np.int32,('lev',))
	lat=NAME.createVariable('lat',np.float64,('lat',))
	lon=NAME.createVariable('lon',np.float64,('lon',))
	# VAR=NAME.createVariable(str(VAR),np.float64,('time','lev','lat','lon'),)
	VAR=NAME.createVariable(ncinfo.var_name,np.float64,('time','lat','lon'),)
	# setting the missing value is super important for the file to be cdo readable
	setattr(VAR,'missing_value',ncinfo.fill)
	setattr(VAR, 'standard_name', ncinfo.var_lname) 
	
	# ========== Set the units ==========
	time.units= 'day as %Y%m%d'
	# lev.units = '-'
	lat.units = 'degrees_north'
	lon.units = 'degrees_east'
	VAR.units = ncinfo.units

	# ========== Add data ==========
	
	# creates time vector using the date_range function
	# time[:]=[t for t in date_range('20110101.5','20111231.5')] 
	# lev[:]=PFT_vector
	lat[:] = ncinfo.latitudes
	lon[:] = ncinfo.longitudes
	# THis is a Bodge for singe variable data
	VAR[:] = ncinfo.data

	#Add global attributes
	NAME.description = ncinfo.description
	NAME.history     = ncinfo.history

	# WHATS MISSING
	# metadata a whole bunch of metadata
	# the standard_name and long_name of the variables

	# ========== Close the netcdf ==========
	NAME.close()

#==============================================================================

if __name__ == '__main__':
	main()