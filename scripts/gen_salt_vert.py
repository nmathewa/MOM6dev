#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 16:55:54 2021

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

from matplotlib import cm
import matplotlib

time = -1
level = 0

for ii in range(len(ocns.Time.values)):
    fig = plt.figure(figsize =(14, 9))
    s_profile = ocns.salt.isel(xh =40,yh=40,Time=ii)
    plt.plot(s_profile, s_profile['zl'])
    plt.ylim(1500,0)
    plt.grid()
    plt.ylabel("Depth(m)")
    plt.xlabel("Salinity")
    plt.title("salt_profile "+str(ocns.Time.values[ii]))
    plt.savefig("docs/salin_"+str(ii)+".png",dpi=150)



