#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 22:41:12 2021

@author: nma
"""

import os
os.chdir("/home/nma/momdev/exps/regional/INPUT/")
from osgeo import gdal
src_tiff = "/home/nma/Downloads/ETOPO1_Bed_g_geotiff.tif"


ds = gdal.Translate("topog.nc", src_tiff, format='NetCDF')

#%%

import xarray as xr

dd = xr.open_dataset("topog.nc")

dd_s = dd.sel(lon=slice(76,100),lat=slice(9,26))

dd_s.z.plot()

#%%
depth = dd_s.z*-1

n_dep = depth.where(depth > 0 ,0)

n_dset =  n_dep.to_dataset(name="depth")

n_dset.to_netcdf("topog_final.nc")
