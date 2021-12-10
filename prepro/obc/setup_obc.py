#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 12:18:01 2021
Regrid vertical
@author: nma
"""

import xarray as xr
import xesmf
import os

#%% sample obc files

caops_dir = "/home/nma/HDD/archives/IOMOM5Op/caops/"

sam_obc = xr.open_dataset(caops_dir+"obc_east.nc")


dz = sam_obc.zl.values
#%% vgrid file

dirv = "/home/nma/mom/MOM6dev/prepro/obc/gen_vgrid/"


IC_grid = xr.open_dataset(dirv+"2013_final.nc")

hy_depth = IC_grid.DEPTH.values

#%% new_obcs 
obc_dir = "/home/nma/mom/MOM6dev/prepro/obc/"

west_obc = xr.open_dataset(obc_dir+"section_west.nc")

south_obc = xr.open_dataset(obc_dir+"section_south.nc")

cur_depth = south_obc.zl.values

reg_south_obc = south_obc.interp(zl=hy_depth)
reg_west_obc = west_obc.interp(zl=hy_depth)


reg_south_obc.to_netcdf(obc_dir+"section_south40.nc")
reg_west_obc.to_netcdf(obc_dir+"section_west40.nc")

#%%

tfil_reg_south_obc = reg_south_obc.rename({'values':'v'}).sel(time=slice("2013-01-01", "2013-12-31"))

tfil_reg_west_obc = reg_west_obc.rename({'values':'u'}).sel(time=slice("2013-01-01", "2013-12-31"))

tfil_reg_south_obc.to_netcdf(obc_dir+"section_south40tt.nc")
tfil_reg_west_obc.to_netcdf(obc_dir+"section_west40tt.nc")

#%%



