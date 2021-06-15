"""
Created on Tue Jun 15 09:37:54 2021

@author: mathew

gridcreation

"""

import numpy as np


def create_lat_lon_regular(lonx1,lonx2,laty1,laty2,resx,resy):
    nx = np.arange(resx)
    ny = np.arange(resy)
    
    lonq = np.linspace(lonx1,lonx2,resx)
    latq = np.linspace(laty1,laty2,resy)
    
    nxx,nyy = np.meshgrid(lonq,latq)
    
    lonh = []
    for ii in range(len(lonq)-1):
        lonh += [(lonq[ii+1] + lonq[ii])/2]
    lonh = np.array(lonh)
    
    lath = []
    
    for jj in range(len(latq)-1):
        lath += [(latq[jj+1] + latq[jj])/2]
    
    lath = np.array(lath)
    
    dx = []
    
    for xxx in range(len(lonq)-1):
        dx += [lonq[xxx+1] - lonq[xxx]]
    
    dx = np.array(dx)*111*1000
    
    dxf = np.meshgrid(dx,latq)[0]
    
    dy = []
    
    for xxx in range(len(latq)-1):
        dy += [latq[xxx+1] - latq[xxx]]
    
    dy = np.array(dy)*111*1000
    
    dyf = np.meshgrid(lonq,dy)[1]
    
    angle_dx = np.zeros((np.shape(nxx)))
    
    dxh,dyh = np.meshgrid(dx,dy)
    
    area = dxh*dyh
    
    return nxx,nyy,area,dxf,dyf,angle_dx



