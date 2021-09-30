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

outdir = "/home/nma/momdev/exps/regional2/INPUT/"

sdset = xr.open_dataset(safordir+"ocean_forcing_daily.nc")

sdset.SW[0,:,:].plot()

dlon,dlat = (77,99),(4,23)

#%% long wave radiation

lw_global = xr.open_dataset(bobdatas+"olr-daily_v01r02_20150101_20151231.nc")

#lw_global.olr[0,:,:].plot()

bob_lw = lw_global.sel(lon=slice(dlon[0]-1,dlon[1]+1),lat=slice(dlat[0]-1,dlat[1]+1))

bob_lw.olr[0,:,:].plot()

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

