"""
Created on Thu Jun 10 14:29:13 2021

@author: mathew

"""

import os
import xarray as xr
import numpy as np

os.chdir(os.getenv("IISC")+"/exps/regional/INPUT/")

#%% 360 and 210 so 2 degree resolution

dset = xr.open_dataset("ocean_hgrid.nc")


ny = dset.ny.values
nx = dset.y.values


#%%
x1lon = 88
x2lon = 92
y1lat = 16
y2lat = 19

nx = np.arange(721)
ny = np.arange(421)

lonq = np.linspace(x1lon,x2lon,721)
latq = np.linspace(y1lat,y2lat,421)

nxx,nyy = np.meshgrid(lonq,latq)

lonh = []
for ii in range(len(lonq)-1):
    lonh += [(lonq[ii+1] + lonq[ii])/2]

lonh = np.array(lonh)

lath = []
for jj in range(len(latq)-1):
    lath += [(latq[jj+1] + latq[jj])/2]

lath = np.array(lath)


dx = []
for xxx in range(len(lonq)-1):
    dx += [lonq[xxx+1] - lonq[xxx]]

dx = np.array(dx)*111*1000

dxf = np.meshgrid(dx,latq)[0]


dy = []
for xxx in range(len(latq)-1):
    dy += [latq[xxx+1] - latq[xxx]]
    
dy = np.array(dy)*111*1000

dyf = np.meshgrid(lonq,dy)[1]


angle_dx = np.zeros((np.shape(nxx)))

#%%
dxh,dyh = np.meshgrid(dx,dy)

area = dxh*dyh



dset.x[:] = nxx
dset.y[:] = nyy
dset.area[:] = area
dset.dx[:] = dxf
dset.dy[:] = dyf

dset.to_netcdf("regionalmom6.nc")


#%% Topo config

dset = xr.open_dataset("topog.nc")


vals = dset.depth.values

n_vals = np.round(np.random.uniform(6000, 7000,np.shape(vals)),2)

dset.depth[:] = n_vals


dset.to_netcdf("topog.nc")

#%%

dset = xr.open_dataset("GOLD_IC.2010.11.15.nc")


eta = dset.eta.values


