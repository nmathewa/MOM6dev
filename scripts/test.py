#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 18:53:33 2021

@author: nma
"""
import os
os.chdir("/home/nma/momdev/exps/caops/INPUT")
import xarray as xr
import numpy as np

stress = xr.open_dataset("erdQAstressmday_375a_1584_3428.nc").isel(altitude=0)

ori_siz = xr.open_dataset("chl_mom6.nc")
nlats,nlons = ori_siz.Latitude.values,ori_siz.Longitude.values

ori_lon = stress.longitude.values - 180
ori_lat = stress.latitude.values

taux_raw,tauy_raw = stress.taux.values,stress.tauy.values

times_new = np.arange('0001-01', '0001-02',dtype='datetime64[D]')[:12]


n_taux = xr.DataArray(data=taux_raw,
                      dims=['time','latitude',"longitude"],
                      coords=dict(
                          time = (["time"],np.array(times_new,dtype=np.float64)),
                          latitude = (['latitude',],ori_lat),
                          longitude = (['longitude',],ori_lon)))

n_tauy = xr.DataArray(data=tauy_raw,
                      dims=['time','latitude',"longitude"],
                      coords=dict(
                          time = (["time"],np.array(times_new,dtype=np.float64)),
                          latitude = (['latitude',],ori_lat),
                          longitude = (['longitude',],ori_lon)))

taux_x = n_taux.interp(latitude=nlats,longitude=nlons)
tauy_y = n_tauy.interp(latitude=nlats,longitude=nlons)


dset = taux_x.to_dataset(name = "taux")

dset["tauy"] = tauy_y

dset_nnn = dset.isel(time=0)
dset_nnn.to_netcdf("wind_force_new_1.nc")
