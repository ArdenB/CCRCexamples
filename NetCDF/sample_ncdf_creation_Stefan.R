write QualityMask to NCDF
library(raster)

QualityMask <- flip(raster(t(QualityMask), ymn = min(lat), ymx = max(lat), xmn = min(lon), xmx = max(lon), 
                           crs = CRS("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs+ towgs84=0,0,0")), 
                    direction = 'y')

writeRaster(QualityMask, 
            filename = "/srv/ccrc/data11/z3289452/DailyPRCP_netCDFs/CCRCGlobalGriddedDailyPrecip/VERSION1.0/ALL/CCRC_V1.0_1950-2013_1deg_QualityMask.nc",
            format = "CDF",
            varname = "p", varunit = "Boolean", 
            longname = "Mask for REGEN V1.0 Global Gridded Daily Precipitation Dataset 1deg based on Standard Deviation and Kriging Error",
            xname = "lon", yname = "lat", fillValue = -99999, overwrite = T)
# The above is easy and quick but does not allow fine adjustments


# We will use RNetCDF to write to ncdf instead
library(RNetCDF)

nc <- create.nc("/srv/ccrc/data11/z3289452/DailyPRCP_netCDFs/CCRCGlobalGriddedDailyPrecip/VERSION1.0/ALL/CCRC_V1.0_1950-2013_1deg_QualityMask.nc")

# two dimensions
dim.def.nc(nc, "lon", 360)
dim.def.nc(nc, "lat", 180)

# three variables including two coordinate vars
var.def.nc(nc, "lon", "NC_DOUBLE", "lon")
var.def.nc(nc, "lat", "NC_DOUBLE", "lat")
var.def.nc(nc, "p", "NC_INT", c(0, 1))

# attributes
att.put.nc(nc, "lon", "unit", "NC_CHAR", "degrees_east")
att.put.nc(nc, "lat", "unit", "NC_CHAR", "degrees_north")
att.put.nc(nc, "lon", "long_name", "NC_CHAR", "Longitude")
att.put.nc(nc, "lat", "long_name", "NC_CHAR", "Latitude")
att.put.nc(nc, "p", "unit", "NC_CHAR", "boolean")
att.put.nc(nc, "p", "long_name", "NC_CHAR", "boolean mask for REGEN precipitation V1.0")
att.put.nc(nc, "p", "missing_value", "NC_INT", -99999)
att.put.nc(nc, "NC_GLOBAL", "title", "NC_CHAR", "REGEN V1.0 1deg Quality Mask based on Std Dev and Krig Err 1950-2013")
att.put.nc(nc, "NC_GLOBAL", "history", "NC_CHAR", paste("Created on", Sys.Date()))

# put vars
var.put.nc(nc, "lon", lon)
var.put.nc(nc, "lat", lat)
var.put.nc(nc, "p", QualityMask)

close.nc(nc)