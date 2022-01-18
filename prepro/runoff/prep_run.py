#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:47:09 2022

@author: nma
"""

import numpy as np
import xarray as xr
import os
os.chdir("/home/nma/GIT/MOM6dev/prepro/runoff/")
import geopandas as gpd
from shapely.geometry import Polygon

import cartopy.crs as ccrs
import rioxarray as rio
import matplotlib.pyplot as plt
import rasterio
from shapely.geometry import mapping
#%%


run_sam = xr.open_dataset("runoff_sample_NIO.nc",decode_times=False)
run_pre = xr.open_dataset("bob_runoff_complete.nc")

n_run_pre = run_pre.rio.write_crs("EPSG:4326")


n_val = n_run_pre.rio.interpolate_na()
#boun_box = Polygon([(0, 0), (0, 90), (180, 90), (180, 0), (0, 0)])

ax = plt.axes(projection=ccrs.PlateCarree())
n_val.sro[1,:,:].plot()
ax.coastlines()

#%%

roi_src = "/home/nma/misc/Downloads_UBU/zip (1)/ne_110m_ocean.shp"


n_val.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
n_val.rio.write_crs("EPSG:4326", inplace=True)
geodf = gpd.read_file(roi_src)
run_clip = n_val.sro.rio.clip(geodf.geometry.apply(mapping))

#%%

run_clip[0,:,:].plot()

plt.savefig("masked_clip.png")