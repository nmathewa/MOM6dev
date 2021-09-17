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
reader = shpreader.Reader("/home/nma/HDD/archives/outs/gadm36_shp/gadm36.shp")


dirs = "/home/nma/HDD/archives/outs/ocnm*"

#shape_feature = ShapelyFeature(reader.geometries(), ccrs.PlateCarree(), facecolor="lime", edgecolor='black', lw=1)


ocns = xr.open_mfdataset(dirs,concat_dim="Time")
#%%


import cartopy.feature as cfeature



u = ocns.u.values[30,0,:,:-1]
v = ocns.v.values[30,0,1:,:]

speed = np.sqrt(u*u + v*v)
#plt.contourf(speed)


fig = plt.figure(figsize=(6,4))
ax = plt.axes(projection=ccrs.PlateCarree())
#ax.add_feature(cartopy.feature.OCEAN, zorder=0)
#ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')


xq,yh = ocns.xq.values,ocns.yh.values

scale = 1e05
x2d,y2d = np.meshgrid(xq,yh)


u = u*np.cos(2 * x2d[:,:-1] / scale + 3 * y2d[:,:-1]/scale)
v = v*np.cos(6*x2d[:,:-1]/scale)


ax.contourf(xq[:-1],yh,speed)
ax.quiver(x2d[:,:-1][::],y2d[:,:-1][::],u[::],v[::],color='black')
#ax.coastlines('110m', linewidth=0.8)
ax.add_feature(cfeature.GSHHSFeature('full', edgecolor='black'))

#plt.colorbar(ax=ax)
plt.title("Ocean currents")
plt.savefig("test.png",dpi=500)


#%%
import datetime


dt = datetime.datetime(2015, 12, 31,0,0)
n_dt = []

for jj in range(np.shape(ocns.u)[0]):
    dt = dt + datetime.timedelta(hours=12)
    n_dt += [dt]
#%%

for ii in range(np.shape(ocns.u)[0]):
    u = ocns.u.values[ii,0,:,:-1]
    v = ocns.v.values[ii,0,1:,:]
    speed = np.sqrt(u*u + v*v)
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    u = u*np.cos(2 * x2d[:,:-1] / scale + 3 * y2d[:,:-1]/scale)
    v = v*np.cos(6*x2d[:,:-1]/scale)
    ax.contourf(xq[:-1],yh,speed,cmap="twilight")
    ax.quiver(x2d[:,:-1][::3],y2d[:,:-1][::3],u[::3],v[::3],scale=7)
    ax.add_feature(cfeature.GSHHSFeature('full', edgecolor='black'))

    PCM=ax.get_children()[2]
    plt.colorbar(PCM,ax=ax)
    plt.title(str(n_dt[ii]))
    plt.savefig("test"+str(ii)+".png",dpi=500)
#%%


import glob
from PIL import Image

# filepaths
fp_in = "/home/nma/HDD/archives/outs/*.png"
fp_out = "/home/nma/HDD/archives/outs/out.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=1000, loop=0)


#%%





from matplotlib import animation


fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())

# initialization function: plot the background of each frame


# animation function.  This is called sequentially
def animate(i):
    u = ocns.u.values[i,0,:,:-1]
    v = ocns.v.values[i,0,1:,:]
    speed = np.sqrt(u*u + v*v)
    
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()