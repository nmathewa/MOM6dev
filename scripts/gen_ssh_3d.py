#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:51:05 2021

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
    time = ii
    fig = plt.figure(figsize =(14, 9))
    ax = plt.axes(projection ='3d')
    z = ocns.ssh.values[time,:,:]
    ax.set_zlim(-4,4)
    ocns.ssh[time,:,:].plot.surface(cmap=cm.ocean_r,vmin=-0.4,vmax=0.4)
    plt.savefig("docs/SSH/ssh_"+str(ii)+".png")


