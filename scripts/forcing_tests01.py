#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 15:07:21 2021

@author: nma
"""
import xarray as xr
import glob

safordir = "/media/nma/misc/UBU20/hdd/IISC_PA/datasets/global/siena_201204/INPUT/" 
bobdatas = "/media/nma/misc/UBU20/hdd/IISC_PA/datasets/myins/"

romsdata = "/home/nma/Downloads/lab_nma/"

outdir = "/home/nma/momdev/exps/regional2/INPUT/"

maskfiles = "/home/nma/Downloads/gshhg-gmt-2.3.7/"

shpfiles = "/home/nma/Downloads/gshhg-shp-2.3.7/GSHHS_shp/f/"

sdset = xr.open_dataset(safordir+"ocean_forcing_daily.nc")

sdset.SW[0,:,:].plot()

dlon,dlat = (77,99),(4,23)

#%% long wave radiation

tflux = xr.open_dataset(romsdata+"Daily_INCOIS_BoB2013TROPFLUX.nc")



tflux.LWR[0,:,:].plot()


lwr13 = tflux.LWR.values
swr13 = tflux.SWR.values


#%% shortwave flux

import numpy as np
import matplotlib.pyplot as plt
import cartopy as cart
#from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

f = Dataset(safordir+"ocean_forcing_daily.nc")
sst = f.variables['LW'][0,:,:]
lats = f.variables['yh'][:]
lons = f.variables['xh'][:]

ax = plt.axes(projection=cart.crs.PlateCarree())
ax.coastlines()
ax.add_feature(cart.feature.LAND, zorder=100, edgecolor='k')
ax.set_global()
plot = ax.contourf(lons, lats, sst, 60, transform=cart.crs.PlateCarree())
cb = plt.colorbar(plot)
plt.show()

