#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 18:56:08 2021

@author: nma
"""

import os
os.chdir("/home/nma/mom/MOM6dev/exps/regional2/INPUT/")
import xarray as xr
import matplotlib.pyplot as plt

mos = xr.open_dataset("ocean_mosaic_bob.nc")

grid = xr.open_dataset("bob_grid.nc")

etopo = xr.open_dataset("etopo_test.nc")

topo = xr.open_dataset("topog.nc")


plt.contourf(etopo.depth.values)
plt.title("etopo_ori")
plt.colorbar()
plt.savefig("etopo.png")

#%%
import numpy as np
from scipy.interpolate import griddata

bath = etopo.depth.values

n_bath = -1*(np.where(bath > 0,0,bath))

#plt.contourf(n_bath)
#plt.colorbar()

nlons,nlats = np.unique(grid.x.values)[::2],np.unique(grid.y.values)[::2]



olons,olats = np.meshgrid(etopo.lon.values,etopo.lat.values)
lonf = olons.flatten()
latf = olats.flatten()
valsf = n_bath.flatten()


#%%
n_baths = griddata((lonf,latf),valsf,(nlons[None,:],nlats[:,None]),method="linear")

#%%

depth_topog = topo.depth.values

final_bath = np.float64(n_baths[1:,1:])


plt.contourf(final_bath)
plt.colorbar()

#%%


dset = xr.Dataset({
    "depth" : (['ny','nx'],final_bath)})

dset.to_netcdf("pytopog.nc")

