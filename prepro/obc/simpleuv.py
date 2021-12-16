#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:09:28 2021

@author: nma
"""

import xarray as xr
import xesmf
from HCtFlood.kara import flood_kara
import bottleneck
import os
import numpy as np
#%%

os.chdir("/home/nma/HDD/archives/IOMOM5Op/")

exp_dir = '/home/nma/mom/MOM6dev/prepro/obc/'

uu = xr.open_mfdataset("*.ocean_uvel.nc")
vv = xr.open_mfdataset("*.ocean_vvel.nc")

grd_p = "/home/nma/mom/MOM6dev/exps/regional2/INPUT/bob_grid.nc"

grid = xr.open_dataset(grd_p)

ds = xr.merge([uu,vv])




ds_cut = ds.sel(xu_ocean=slice(65,100), yu_ocean=slice(0,28))

#ds_cut['u'].isel(time=0, st_ocean=0).plot(figsize=[10,6],cmap='jet')


#%%


# southern boundary
south = xr.Dataset()
south['lon'] = grid['x'].isel(nyp=0)
south['lat'] = grid['y'].isel(nyp=0)


# western boundary
west = xr.Dataset()
west['lon'] = grid['x'].isel(nxp=0)
west['lat'] = grid['y'].isel(nxp=0)

#%%

regrid_south = xesmf.Regridder(ds_cut.rename({'xu_ocean': 'lon', 'yu_ocean': 'lat'}), south, 'bilinear', 
                               locstream_out=True, periodic=False, filename='regrid_south.nc')




regrid_west = xesmf.Regridder(ds_cut.rename({'xu_ocean': 'lon', 'yu_ocean': 'lat'}), west, 'bilinear', 
                              locstream_out=True, periodic=False, filename='regrid_west.nc')


u_west = regrid_west(ds_cut['u'])
v_south = regrid_south(ds_cut['v'])

#%%


drowned_u_west = u_west.ffill(dim='nyp').ffill(dim='st_ocean')

drowned_v_south = v_south.ffill(dim='nxp').ffill(dim='st_ocean')




#drowned_v_south.isel(time=0).plot(figsize=[8, 6], yincrease=False, cmap='jet')



#%% adding dim

#dd= drowned_u_west.expand_dims({"nxp":drowned_u_west.lon[0]})

n_west_array = np.expand_dims(drowned_u_west.values,axis=3)

n_south_array = np.expand_dims(drowned_v_south.values,axis=2)

#dz_vals = 

#%%

west_final = xr.Dataset({
    "u" : (["time","zl","yh","xq"],n_west_array),},
    coords = {"time":(["time",],drowned_u_west.time.values),
              "zl":(["zl",],drowned_u_west.st_ocean.values),
              "yh":(["yh",],drowned_u_west.lat.values),
              "xq":(["xq"],[drowned_u_west.lon.values[0]])})


south_final = xr.Dataset({
    "v" : (["time","zl","yq","xh"],n_south_array),},
    coords = {"time":(["time",],drowned_v_south.time.values),
              "zl":(["zl",],drowned_v_south.st_ocean.values),
              "yq":(["yq",],[drowned_v_south.lat.values[0]]),
              "xh":(["xh"],drowned_v_south.lon.values)})



#%%
west_final.to_netcdf(exp_dir+"section_west1.nc")

south_final.to_netcdf(exp_dir+"section_south1.nc")

