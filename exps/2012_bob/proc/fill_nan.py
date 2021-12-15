#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:44:05 2021

@author: nma
"""

import xarray as xr
import os
os.chdir("/home/nma/mom/MOM6dev/exps/2012_bob/proc/")
import rioxarray as rio

#%%

era_1213 = xr.open_dataset("2012-2013_era5daily.nc")

sphum_ = xr.open_mfdataset("q*m.nc").Q2M



sphum_.rio.write_crs("EPSG:4326", inplace=True)


fill_t = sphum_.rio.interpolate_na().to_dataset()


fill_t.to_netcdf("sphum_filled2012-13.nc")

