#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:49:14 2021

@author: nma
"""

import xarray as xr
import numpy as np
import os 

os.chdir("/home/nma/HDD/hdd/IISC_PA/COAPS_config/datasets/CFSv2/")



def str_com(vel):
    if vel >4 and vel <= 11 :
        cd = 1.2e-3
    elif vel > 11 and vel < 25:
        cd = 1e-3*(0.49 + (0.065*vel))
    
    else:
        cd = 0.0013
    rho = 1.22
    tau = cd*rho*(vel*vel)
    return tau

tau_vec = np.vectorize(str_com)

uv10 = xr.open_dataset("cfsv2_gom-sec2_2015_01hr_uv-10m.nc")

u,v = uv10.wndewd,uv10.wndnwd

print(np.nanmax(u))
#%%
import matplotlib.pyplot as plt
taux = tau_vec(u[0,:,:])

plt.contourf(taux)
plt.colorbar()
