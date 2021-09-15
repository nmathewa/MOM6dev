#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:44:46 2021

@author: nma
"""

from osgeo import gdal
from osgeo import gdal_array
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

#gebco = xr.open_dataset("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebo_grid.nc")
#lat = gebco.lat.values
#lon = gebco.lon.values

etopo = "/home/nma/Downloads/ETOPO1_Bed_g_gdal.grd"


gdd = gdal_array.LoadFile(etopo)
ds = gdal.Open(etopo)
width = ds.RasterXSize
height = ds.RasterYSize
gt = ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5] 
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3] 


gdd_fin = np.flip(gdd)

lons = np.linspace(minx,maxx,np.shape(gdd_fin)[1])
lons_final = lons[::-1]
lats = np.linspace(miny,maxy,np.shape(gdd_fin)[0])



#gdd_fin = np.rot90(gdd,k=4)

#plt.contourf(lons_final,lats,gdd_fin)

attributes ={"author":"IISC-NMA"}

ttr = xr.Variable(dims=("lat","lon"),data=gdd_fin,attrs={"missing_value":"12.2","dtype":"NC_DOUBLE"})
#dset.to_netcdf("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebco_test.nc",format="NETCDF4")
dset = xr.Dataset({
    "depth" : ttr},
    coords = {"lon":(["lon",],lons_final),
              "lat":(["lat",],lats)},
    attrs=(attributes))
dset.to_netcdf("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebco_test.nc")

#%%subset

n_sel = dset.sel(lon = slice(120,60),lat=slice(0,30))

n_sel.to_netcdf("/home/nma/mom/MOM6dev/exps/regional2/INPUT/etopo_test.nc")


plt.contourf(n_sel.depth.values)
plt.colorbar()