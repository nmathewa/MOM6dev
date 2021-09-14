#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:13:11 2021

@author: nma
"""

import xarray as xr
import numpy as np

gebco = xr.open_dataset("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebo_grid.nc")


lat = gebco.lat.values
lon = gebco.lon.values


ele = gebco.elevation.values
ele_d = np.single(ele)
attributes = {}
#attributes["missing_value"] = 9999



ttr = xr.Variable(dims=("lat","lon"),data=ele_d,attrs={"missing_value":"12.2","dtype":"NC_DOUBLE"})
#dset.to_netcdf("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebco_test.nc",format="NETCDF4")
dset = xr.Dataset({
    "depth" : ttr},
    coords = {"lon":(["lon",],lon),
              "lat":(["lat",],lat)},
    attrs=(attributes))
dset.to_netcdf("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebco_test.nc")

print(dset.attrs)

#%%

gebco_new = xr.open_dataset("/home/nma/mom/MOM6dev/exps/regional2/INPUT/gebco_test.nc")

print(gebco_new.attrs)


#%%


