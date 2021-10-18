#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 09:53:13 2021
create new_initial conditions
@author: nma
"""

import os
import xarray as xr
import numpy as np
from scipy.interpolate import griddata

os.chdir("/home/nma/momdev/exps/global/INPUT/")

gold = xr.open_dataset("GOLD_IC.2010.11.15.nc")

n_gold = gold.sel(longitude=slice(60,120),latitude=slice(5,28))

grid = xr.open_dataset("../../regional/INPUT/ocean_hgrid.nc")

lons,lats = grid.x.values.flatten(),grid.y.values.flatten()
n_lons,n_lats = np.array(np.unique(lons)[::2],dtype=np.float32),np.array(np.unique(lats)[::2],dtype=np.float32)
n_lonss,n_latss = np.delete(n_lons,4),np.delete(n_lats,4)



n_gold_temp = n_gold.ptemp.interp(longitude=n_lonss,latitude=n_latss)


#%%create_salt and ptemp
"""63 layers (both ptemp and salinity)"""

hycom_new = xr.open_dataset("../../regional/INPUT/data_2015.nc4")




hyc_sal = hycom_new.salinity

hy_n_sal = hyc_sal.interp(lon=n_lonss,lat=n_latss)
hy_n_temp = hyc_temp.interp(lon=n_lonss,lat=n_latss)


salt_40 = hy_n_sal.values
temp_40 = hy_n_temp.values

llsal = 23*[np.expand_dims(salt_40[0,-1,:,:],axis=0)]

n_sal_22 = np.expand_dims(np.concatenate(llsal),axis=0)

salt_63 = np.append(arr=salt_40,values=n_sal_22,axis=1)


lltemp = 23*[np.expand_dims(temp_40[0,-1,:,:],axis=0)]

n_temp_22 = np.expand_dims(np.concatenate(llsal),axis=0)

temp_63 = np.append(arr=temp_40,values=n_temp_22,axis=1)

#%% ndsets

lons,lats = n_lonss,n_latss
interfaces = gold.Interface.values
layers = gold.Layer.values 
eta = gold.eta.values
ftemp_63 = temp_63[0,:,:,:]
fsalt_63 = salt_63[0,:,:,:]


dset = xr.Dataset({
    "ptemp" : (["Layer","latitude","longitude"],ftemp_63),
    "salt" : (["Layer","latitude","longitude"],fsalt_63),
    "eta" : (["Interface","latitude","longitude"],eta)},
    coords = {"Interface":(["Interface",],interfaces),
              "longitude":(["longitude",],lons),
              "latitude":(["latitude",],lats)})
