#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 17:09:22 2021

@author: nma
"""

import xarray as xr
import numpy as np
import os
os.chdir("/home/nma/HDD/archives/outs/")
import matplotlib.pyplot as plt
import cartopy 
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature
reader = shpreader.Reader("/home/nma/HDD/archives/outs/gadm36_IND_shp/gadm36_IND_2.shp")

 
dirs = "/home/nma/HDD/archives/outs/ocnm*"

shape_feature = ShapelyFeature(reader.geometries(), ccrs.PlateCarree(), facecolor="lime", edgecolor='black', lw=1)


ocns = xr.open_mfdataset(dirs,concat_dim="Time")
#%%

u = ocns.u.values[30,0,:,:-1]
v = ocns.v.values[30,0,1:,:]

speed = np.sqrt(u*u + v*v)
#plt.contourf(speed)



ax = plt.axes(projection=ccrs.PlateCarree())
#ax.add_feature(cartopy.feature.OCEAN, zorder=0)
#ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')


xq,yh = ocns.xq.values,ocns.yh.values

scale = 1e7
x2d,y2d = np.meshgrid(xq,yh)


u = u*np.cos(2 * x2d[:,:-1] / scale + 3 * y2d[:,:-1]/scale)
v = v*np.cos(6*x2d[:,:-1]/scale)


ax.contourf(xq[:-1],yh,speed)
ax.quiver(x2d[:,:-1],y2d[:,:-1],u,v)
#ax.coastlines('110m', linewidth=0.8)
ax.add_feature(shape_feature)

plt.savefig("test.png",dpi=500)
