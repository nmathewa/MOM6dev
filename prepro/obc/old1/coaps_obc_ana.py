#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:36:04 2021

@author: nma
"""
import xarray as xr
import os
import xesmf
import matplotlib.pyplot as plt
import bottleneck
import numpy as np
import subprocess as sp
import os
import glob
import cartopy.crs as ccrs


os.chdir("/home/nma/mom/general/datasets/OBC_DAILY/")

#%%

obc_east = xr.open_dataset("obc_GOMb0.08_east_2015a_53X_daily.nc")

u_segment = obc_east.u_segment_002[:,:,:,0].values


