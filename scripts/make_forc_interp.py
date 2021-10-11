#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:50:25 2021
import
@author: nma
"""
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbs
import os

outest = "/home/nma/momdev/exps/caops/docs/"
os.chdir("/home/nma/momdev/exps/caops/INPUT/")

sponge_init = xr.open_dataset("53X_archm.2015010109_tsuv_filled.nc")
n_wind = xr.open_dataset("wind_force.nc")



sbs.heatmap(sponge_init.ptemp[0,0,:,:].values)
plt.savefig(outest+"init_hm.jpg")

#%%

f_lats = n_wind.lat.values
f_lons = n_wind.lon.values
taux = n_wind.taux
tauy = n_wind.tauy


n_lats = sponge_init.lat.values
n_lons = sponge_init.lon.values

n_taux = taux.interp(lat=n_lats,lon=n_lons)
n_tauy = tauy.interp(lat=n_lats,lon=n_lons)


dset = n_taux.to_dataset(name='taux')

dset["tauy"] = n_tauy

dset.to_netcdf("wind_force_new.nc")

#%%



m_forc = xr.open_dataset("wind_force_new.nc")
#sam_forc = xr.open_dataset("")


taux,tauy = m_forc.taux.values,m_forc.tauy.values

n_taux = np.transpose(taux,(1,2,0))
n_tauy = np.transpose(tauy,(1,2,0))

#sbs.heatmap(n_taux[:,:,0])

taux_nan = np.where(n_taux == np.nan,0,n_taux)
tauy_nan = np.where(n_tauy == np.nan,0,n_tauy )

plt.contourf(tauy_nan[:,:,0])
#%%

dset = xr.Dataset({
    "taux" : (["lat","lon","time"],taux_nan),
    "tauy" : (["lat","lon","time"],tauy_nan)},
    coords = {"time":(["time",],m_forc.time.values),
              "lon":(["lon",],n_lons),
              "lat":(["lat",],n_lats)})
dset.to_netcdf("wind_force_new_1.nc")
