"""
Created on Tue Jun 15 09:37:54 2021

@author: mathew

gridcreation

"""

import numpy as np
import os 
import subprocess as sub
import pandas as pd

class create_grid:
    def __init__(self,latitude,longitude,res_x , res_y,create_method='FRE'):
        
        self.create = create_method
        if self.create == 'FRE':    
            try : 
                sub.check_output('make_hgrid --help')
            except FileNotFoundError:
                print ("FRE_nc_tools not found")
                print("Switching to python engine")
                self.create = 'python'
        else :
            self.fre = True
        
        dom = pd.Series()
        latc,lonc = latitude,longitude
        lat1,lat2 = latc - (res_y/2) , latc + (res_y/2) 
        lon1,lon2 = latc - (res_x/2) , latc + (res_x/2) 
        
        dom['lat1'] = lat1
        dom['lat2'] = lat2
        dom['lon1'] = lon1
        dom['lon2'] = lon2
        
        dom['xres'] = res_x
        dom['yres'] = res_y
        
        self.dom = dom
    
    def get_dom(self):
        return self.dom
    
    def create_ngrid(self):
        lon1 = self.dom['lon1']
        lon2 = self.dom['lon2']
        lat1 = self.dom['lat1']
        lat2 = self.dom['lat2']
        xres = self.dom['xres']
        yres = self.dom['yres']
        
        
        if self.fre :
            sub.run('make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd '+lon1+','+lon2+' --ybnd '+lat1+','+lat2+' --nlon '+xres+' --nlat '+yres+' --verbose')


    
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



