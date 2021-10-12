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

#n_taux = np.transpose(taux,(1,2,0))
#n_tauy = np.transpose(tauy,(1,2,0))

#sbs.heatmap(n_taux[:,:,0])

#taux_nan = np.where(taux == np.nan,0,n_taux)
#tauy_nan = np.where(taux == np.nan,0,n_tauy )

plt.contourf(taux[0,:,:])

#%%

dset = xr.Dataset({
    "taux" : (["lat","lon","time"],taux_nan),
    "tauy" : (["lat","lon","time"],tauy_nan)},
    coords = {"time":(["time",],m_forc.time.values),
              "lon":(["lon",],n_lons),
              "lat":(["lat",],n_lats)})
dset.to_netcdf("wind_force_new_1.nc")

#%%

os.chdir("/home/nma/HDD/hdd/IISC_PA/datasets/global/siena_201204/INPUT/")

forcing_ori = xr.open_dataset("ocean_forcing_daily.nc")

times_ori = forcing_ori.time.values[:31]

taux_tim = np.array(taux[:31,:,:],dtype=np.float32)
tauy_tim = np.array(taux[:31,:,:],dtype=np.float32)


times_new = np.array(['0001-01', '0001-02'], dtype='datetime64[D]')


#%%

os.chdir("/home/nma/momdev/exps/caops/INPUT/")


dset = xr.Dataset({
    "taux" : (["time","yh","xq"],taux_tim),
    "tauy" : (["time","yh","xq"],tauy_tim)},
    coords = {"yh":(["yh",],n_lats),
              "xq":(["xq",],n_lons),
              "time":(["time",],times_ori)})
dset.to_netcdf("wind_force_new_1.nc")

#%%

reg = xr.open_dataset('regional.mom6.nc')

