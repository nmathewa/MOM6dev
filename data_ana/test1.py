#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:26:33 2021

@author: nMathewa

@Indian Institute of Science

"""

import os
import xarray as xr
import numpy as np
import glob
import matplotlib.pyplot as plt


os.chdir("/home/vinay/nma/MOM6dev/data_ana/")


sam_dir = "../../exps/regional2/INPUT/"
sam_files = glob.glob(sam_dir+"*.nc")

out_dir = "../../exps/regional2/INPUT/test_ins/"

#%%
    
dt_names = []
for ii in range(len(sam_files)):
    print (sam_files[ii])
    dt_names += [xr.open_dataset(sam_files[ii])]

#dt_names = ["sponge","depth","sponge_mask","tsuv_filled","regional","vgrid"]
    
sponge,depth,sponge_m,tsuv_filled,regional,vgrid = dt_names[0],dt_names[1],dt_names[2],dt_names[3],dt_names[4],dt_names[5]


#%%region and regional.mom

lon_min,lon_max = 88.6,92.5

lat_min,lat_max = 19.4,22.7
    #nx = np.arange(resx)
    #ny = np.arange(resy)
    
def create_lat_lon_regular(lonx1,lonx2,laty1,laty2,resx,resy):
    #nx = np.arange(resx)
    #ny = np.arange(resy)
    
    #lonq = np.linspace(lonx1,lonx2,resx)
    #latq = np.linspace(laty1,laty2,resy)
    
    lonq = np.arange(lonx1,lonx2,resx)
    latq = np.arange(laty1,laty2,resy)
    
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
    
    dxh,dyh = np.meshgrid(dx,dy)
    
    area = dxh*dyh
    
    return nxx,nyy,area,dxf,dyf,angle_dx

res = np.unique(regional.x.values)
nn = []

for ii in range(len(res)-1):
    nn += [res[ii+1] - res[ii]]

kk = []
for jj in range(len(res)-1):
    kk += [res[ii+1] - res[ii]]
    
resx = np.round(np.mean(nn),3)
resy = np.round(np.mean(nn),3)

x,y,area,dx,dy,angle = create_lat_lon_regular(lon_min, lon_max, lat_min, lat_max, resx, resy)


#%% sponge preparation


plt.contourf(sponge.rmu.values)


#%%depth preparation
from scipy.interpolate import griddata

dep_vals = depth.depth.values

gtopo = xr.open_dataset(out_dir+"bath/gebco_2020_n24.290771484375_s9.195556640625_w78.46435546875001_e100.63476562500001.nc")


n_dset = gtopo.sel(lat = slice(lat_min-1,lat_max+1),lon = slice(lon_min-1,lon_max+1)) #subsetting the netcdf using xarrray.sel
xlat = n_dset.lat.values
ylon = n_dset.lon.values
vals = n_dset.elevation.values


xm,ym = np.meshgrid(ylon,xlat) 
xf = xm.flatten()
yf = ym.flatten()
valsf = vals.flatten()


xx = np.arange(lon_min,lon_max,resx)
yy = np.arange(lat_min,lat_max,resy)


n_bath = griddata((xf,yf),valsf,(xx[None,:],yy[:,None]),method="linear")




#%%

# wet is 1 dry is 0

abs_bath = abs(np.where(n_bath > 0,0,n_bath))

n_wet = np.where(abs_bath > 0,1,0)

wets = depth.wet.values

plt.contourf(n_wet,levels=1)
plt.colorbar()



#plt.contourf(gtopo.lon.values,gtopo.lat.values,gtopo.elevation.values)
#plt.title("GEBCO global bathymetry 2020")
#plt.xlabel("Longitude")
#plt.ylabel("Latitude")
#plt.savefig("Bath.png")












    