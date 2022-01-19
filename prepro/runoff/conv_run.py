#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 06:52:39 2022

@author: nma
"""
import xarray as xr
import numpy as np
import os
os.chdir("/home/nma/GIT/MOM6dev/prepro/runoff/")
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
#%%

run_area = xr.open_dataset("area.nc").cell_area.values
run = xr.open_dataset("runoff_parag.nc")


""" 
1 . volume to m
2. to mm (multiply by 0.001)

"""
ax = plt.axes(projection=ccrs.PlateCarree())

n_runoff = 1000*((run.runoff)/run_area)

n_runoff.attrs = {"long_name" : "Runoff flux in to ocean",
                  "units":"(kg/m^2)/s",
                  "history":"CDO"}
n_runoff[7,:,:].plot(cmap='jet')

n_runoff.to_netcdf("new_runoff.nc")
