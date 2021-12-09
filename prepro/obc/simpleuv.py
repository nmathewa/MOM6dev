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

#%%

os.chdir("/home/nma/HDD/archives/IOMOM5Op/")

exp_dir = '/home/nma/mom/MOM6dev/prepro/obc/'

uu = xr.open_mfdataset("*.ocean_uvel.nc")
vv = xr.open_mfdataset("*.ocean_vvel.nc")

grd_p = "/home/nma/mom/MOM6dev/exps/regional2/INPUT/bob_grid.nc"

grid = xr.open_dataset(grd_p)

ds = xr.merge([uu,vv])




ds_cut = ds.sel(xu_ocean=slice(65,100), yu_ocean=slice(0,28))

ds_cut['u'].isel(time=0, st_ocean=0).plot(figsize=[10,6],cmap='jet')


#%%


# southern boundary
south = xr.Dataset()
south['lon'] = grid['x'].isel(nyp=0)
south['lat'] = grid['y'].isel(nyp=0)

# western boundary
west = xr.Dataset()
west['lon'] = grid['x'].isel(nxp=0)
west['lat'] = grid['y'].isel(nxp=0)



regrid_south = xesmf.Regridder(ds_cut.rename({'xu_ocean': 'lon', 'yu_ocean': 'lat'}), south, 'bilinear', 
                               locstream_out=True, periodic=False, filename='regrid_south.nc')




regrid_west = xesmf.Regridder(ds_cut.rename({'xu_ocean': 'lon', 'yu_ocean': 'lat'}), west, 'bilinear', 
                              locstream_out=True, periodic=False, filename='regrid_west.nc')


u_west = regrid_west(ds_cut['u'])
v_south = regrid_south(ds_cut['v'])

#%%


drowned_u_west = u_west.ffill(dim='nyp').ffill(dim='st_ocean')

drowned_v_south = v_south.ffill(dim='nxp').ffill(dim='st_ocean')


drowned_v_south.isel(time=0).plot(figsize=[8, 6], yincrease=False, cmap='jet')

#%%
drowned_u_west.to_netcdf(exp_dir+"section_west.nc")

drowned_v_south.to_netcdf(exp_dir+"section_south.nc")

