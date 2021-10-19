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
hyc_temp = hycom_new.water_temp


hy_n_sal = hyc_sal.interp(lon=n_lonss,lat=n_latss)
hy_n_temp = hyc_temp.interp(lon=n_lonss,lat=n_latss)


salt_40 = hy_n_sal.values
temp_40 = hy_n_temp.values

llsal = 23*[np.expand_dims(salt_40[0,-1,:,:],axis=0)]

n_sal_22 = np.expand_dims(np.concatenate(llsal),axis=0)

#salt_63 = np.append(arr=salt_40,values=n_sal_22,axis=1)

salt_38 = hy_n_sal.values[:,:37,:,:]


lltemp = 23*[np.expand_dims(temp_40[0,-1,:,:],axis=0)]

n_temp_22 = np.expand_dims(np.concatenate(llsal),axis=0)

#temp_63 = np.append(arr=temp_40,values=n_temp_22,axis=1)

temp_38 = hy_n_temp.values[:,:37,:,:]

import matplotlib.pyplot as plt

plt.contourf(temp_38[0,-1,:,:])
#%%create eta
"""64 level eta"""
import matplotlib.pyplot as plt

eta_init = gold.eta.values

topog = xr.open_dataset("../../regional/INPUT/topog.nc")


dep = topog.depth.values
#topog.depth.plot()

eta0 = eta_init[0,:,:]

eat_0 = np.expand_dims(np.ones(np.shape(dep))*eta0[0,0],axis=0)

eat_1 = np.expand_dims(np.where(dep > 0,eta0[0,0],-5),axis=0)

eat_2 = np.expand_dims(np.where(dep > 0,eta0[0,0],-10),axis=0)

eat_3 = np.expand_dims(np.where(dep > 0,eta0[0,0],-10),axis=0)


eat_4 = np.expand_dims(np.where(dep > 0,eta0[0,0],-10),axis=0)

#eat_5 = 59*[np.expand_dims(np.where(dep >= 10,-1*dep,eta0[0,0]),axis=0)]

eat_5 = 33*[np.expand_dims(np.where(dep >= 10,-1*dep,eta0[0,0]),axis=0)]

#eat_58 = np.concatenate(eat_5)
eat_34 = np.concatenate(eat_5)

eat_full = np.concatenate([eat_0,eat_1,eat_2,eat_3,eat_4,eat_34],axis=0)
#plt.contourf(eat_1)
#for ii in range(eta_init.shape[0]):
    


#%% ndsets

lons,lats = n_lonss,n_latss
interfaces = gold.Interface.values[:38]
layers = gold.Layer.values 
eta = gold.eta.values
#ftemp_63 = temp_63[0,:,:,:]
#fsalt_63 = salt_63[0,:,:,:]
ftemp_38 = temp_38[0,:,:,:]
fsalt_38 = salt_38[0,:,:,:]



dset = xr.Dataset({
    "ptemp" : (["Layer","latitude","longitude"],ftemp_38),
    "salt" : (["Layer","latitude","longitude"],fsalt_38),
    "eta" : (["Interface","latitude","longitude"],eat_full)},
    coords = {"Interface":(["Interface",],interfaces),
              "longitude":(["longitude",],lons),
              "latitude":(["latitude",],lats)})


dset.to_netcdf("../../regional/INPUT/test_wo2eta.nc")

#%%
"""ptemp only up to 38, salt up to 37"""
import xarray as xr

readdset = xr.open_dataset("../../regional/INPUT/test_wo2eta.nc")

#readdset.ptemp[38,:,:].plot()
readdset.salt[38,:,:].plot()