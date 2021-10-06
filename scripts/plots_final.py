#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:51:55 2021
data processing
@author: nma
"""

import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import datetime

os.chdir("/home/nma/momdev/exps/caops/")

ocnm = xr.open_mfdataset("ocnm*.nc",concat_dim="Time",use_cftime=True)
ocns = xr.open_mfdataset("ocns*.nc",concat_dim="Time",use_cftime=True)

lons,lats = ocns.xq[:-1],ocns.yq[:-1]


u = ocns.u[:,:,:,:-1]
v = ocns.v[:,:,:-1,:]
uu = u*u
vv = v*v


lon2d, lat2d = np.meshgrid(lons, lats)

#%%
speed = np.sqrt(uu.values[0,0,:,:] + vv.values[0,0,:,:])




#%%
import cartopy as car
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib import cm
import matplotlib

time = -1
level = 0

fig = plt.figure(figsize =(14, 9))
ax = plt.axes(projection ='3d')
#plt.figure(figsize=(8,6))
#ax.coastlines()
#plt.title("Time : " + str(ocns.Time.values[time])+" level : "+str(ocns.zl.values[level]))
#gg = ax.contourf(lon2d,lat2d,ocns.sst.values[time,:,:],cmap="ocean_r",vmin=12,vmax=30,levels=100)


z = ocns.ssh.values[time,:,:]
z = np.ma.masked_invalid(z)
#mask = np.ma.getmaskarray(z)
normC = matplotlib.colors.Normalize(vmax=z.max(), vmin=z.min())
colors = plt.get_cmap("plasma")(normC(z))

#mycmap = plt.get_cmap('gist_earth',cmap=cm.gist_earth)
#ax.plot_surface(lon2d,lat2d,z,cmap=cm.gist_earth)
ax.set_zlim(-4,4)

ocns.ssh[time,:,:].plot.surface(cmap=cm.ocean,vmin=-0.4,vmax=0.4)
#plt.setzlim(-2,2)
#plt.xlabel("Longitude")
#plt.ylabel("Latitude")
#plt.colorbar(gg, orientation="horizontal")
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  #linewidth=1, color='gray', alpha=0.1, linestyle='--')
#plt.savefig("docs/surface_sst2.png",dpi=150)


#%%
for ii in range(len(ocns.Time.values)):
    time = ii
    plt.figure(figsize=(8,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()import glob
    from PIL import Image

    # filepaths
    fp_in = "/home/nma/HDD/archives/outs/*.png"
    fp_out = "/home/nma/HDD/archives/outs/out.gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1000, loop=0)
    plt.title("Time : " + str(ocns.Time.values[time])+" level : "+str(ocns.zl.values[level]))
    gg = ax.contourf(lon2d,lat2d,ocns.sst.values[time,:,:],cmap="ocean_r",vmin=12,vmax=30,levels=100)
    #plt.xlabel("Longitude")
    #plt.ylabel("Latitude")
    plt.colorbar(gg, orientation="horizontal")
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.1, linestyle='--')
    plt.savefig("docs/surface_sst"+str(ii)+".png",dpi=150)    

#%%

import glob
from PIL import Image

# filepaths
fp_in = "/home/nma/momdev/exps/caops/docs/surf*.png"
fp_out = "/home/nma/momdev/exps/caops/docs/out.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=1000, loop=0)