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
import numpy as np

#%% sample obc files

caops_dir = "/home/nma/HDD/archives/IOMOM5Op/caops/"

sam_obc = xr.open_dataset(caops_dir+"obc_east.nc")


dz = sam_obc.dz_u_segment_002
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


#%%

u_west_dz_new = np.array(len(reg_west_obc.xq.values)*[np.array(len(reg_west_obc.yh.values)*[np.array(len(reg_west_obc.time.values)*[np.insert(np.diff(hy_depth),
                                                                                      0,1)])])])
final_dzuw = u_west_dz_new.transpose(2,3,1,0)

fin_reg_west = reg_west_obc.assign({"dz_U11":(["time","zl","yh","xq"],final_dzuw)})


v_south_dz_new = np.array(len(reg_south_obc.xq.values)*[np.array(len(reg_south_obc.yh.values)*[np.array(len(reg_south_obc.time.values)*[np.insert(np.diff(hy_depth),
                                                                                      0,1)])])])
final_dzvs = v_south_dz_new.transpose(2,3,1,0)

fin_reg_south = reg_south_obc.assign({"dz_V11":(["time","zl","yh","xq"],final_dzvs)})



#%%

reg_south_obc.to_netcdf(obc_dir+"section_south40.nc")
reg_west_obc.to_netcdf(obc_dir+"section_west40.nc")

#%%

tfil_reg_south_obc = fin_reg_south.rename({'values':'v'}).sel(time=slice("2013-01-01", "2013-12-31"))

tfil_reg_west_obc = fin_reg_west.rename({'values':'u'}).sel(time=slice("2013-01-01", "2013-12-31"))




#%%


tfil_reg_south_obc.to_netcdf(obc_dir+"section_south40tt.nc")
tfil_reg_west_obc.to_netcdf(obc_dir+"section_west40tt.nc")

#%%



