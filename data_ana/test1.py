#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:26:33 2021

@author: nMathewa

@Indian Institute of Science

"""

import os
import xarray as xr
import numpy as np
import glob
import matplotlib.pyplot as plt


os.chdir("/home/vinay/nma/MOM6dev/data_ana/")
#os.chdir("/home/mathew/hdd/UBU20/hdd/GIT/MOM6dev/data_ana/")

sam_dir = "../../exps/regional2/INPUT/"
#sam_dir = "/home/mathew/hdd/UBU20/hdd/IISC_PA/exps/regional2/INPUT/"

sam_files = glob.glob(sam_dir+"*.nc")

out_dir = "/home/vinay/nma/exps/regional2/INPUT/test_ins/"

#out_dir = "/home/mathew/hdd/UBU20/hdd/IISC_PA/exps/regional2/INPUT/test_ins/"

#%%

""" Sponge rmu files are not used"""
    
dt_names = []
for ii in range(len(sam_files)):
    print (sam_files[ii])
    dt_names += [xr.open_dataset(sam_files[ii])]

#dt_names = ["sponge","depth","sponge_mask","tsuv_filled","regional","vgrid"]
    
sponge,depth,sponge_m,tsuv_filled,regional,vgrid = dt_names[0],dt_names[1],dt_names[2],dt_names[3],dt_names[4],dt_names[5]

#tsuv_filled,sponge_m,depth,vgrid,regional,sponge,sponge_rmu,test = dt_names[0],dt_names[1],dt_names[2],dt_names[3],dt_names[4],dt_names[5],dt_names[6],dt_names[7]

#%%region and regional.mom

lon_min,lon_max = 75.6,90.5

lat_min,lat_max = 10.4,20.7
    #nx = np.arange(resx)
    #ny = np.arange(resy)

def create_lat_lon_regular(lonx1,lonx2,laty1,laty2,resx,resy):
    #nx = np.arange(resx)
    #ny = np.arange(resy)
    
    lonq = np.linspace(lonx1,lonx2,resx)
    latq = np.linspace(laty1,laty2,resy)
    
    #lonq = np.arange(lonx1,lonx2,resx)
    resy #latq = np.arange(laty1,laty2,resy)
    
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

res = np.unique(regional.x.values)
nn = []

for ii in range(len(res)-1):
    nn += [res[ii+1] - res[ii]]

kk = []
for jj in range(len(res)-1):
    kk += [res[ii+1] - res[ii]]
    
#resx = np.round(np.mean(nn),3)
#resy = np.round(np.mean(nn),3)

resx = 525 #nx
resy = 385 #ny

x,y,area,dx,dy,angle = create_lat_lon_regular(lon_min, lon_max, lat_min, lat_max, resx, resy)


region_bob = xr.Dataset({
    "x" : (["nyp","nxp"],x),
    "y" : (["nyp","nxp"],y),
    "angle_dx" : (["nyp","nxp"],angle),
    "dx" : (["nyp","nx"],dx),
    "dy" : (["ny","nxp"],dy),
    "area" : (["ny","nx"],area),})

region_bob.to_netcdf(out_dir+"regional_bob.nc")

#%% sponge preparation


plt.contourf(sponge.rmu.values)


#%%depth preparation
from scipy.interpolate import griddata

nresx = 262
nresy = 192

"""custom lons and lats for depth"""
#n_lons = np.linspace(lons[0],lons[-1],nresx)
#n_lats = np.linspace(lats[0],lats[-1],nresy)


dep_vals = depth.depth.values

gtopo = xr.open_dataset(out_dir+"bath/gebco_2020_n24.290771484375_s9.195556640625_w78.46435546875001_e100.63476562500001.nc")

#gtopo = xr.open_dataset("/home/mathew/hdd/UBU20/hdd/IISC_PA/exps/regional2/INPUT/n_folder/gebco_2020_tid_netcdf/GEBCO_2020_TID.nc")

n_dset = gtopo.sel(lat = slice(lat_min-1,lat_max+1),lon = slice(lon_min-1,lon_max+1)) #subsetting the netcdf using xarrray.sel
xlat = n_dset.lat.values
ylon = n_dset.lon.values
vals = n_dset.elevation.values


xm,ym = np.meshgrid(ylon,xlat) 
xf = xm.flatten()
yf = ym.flatten()
valsf = vals.flatten()

#xx = np.arange(lon_min,lon_max,resx)
#yy = np.arange(lat_min,lat_max,resy)

xx = np.linspace(lon_min,lon_max,nresx)
yy = np.linspace(lat_min,lat_max,nresy)

n_bath = griddata((xf,yf),valsf,(xx[None,:],yy[:,None]),method="linear")




#%%

# wet is 1 dry is 0

abs_bath = abs(np.where(n_bath > 0,0,n_bath))
abs_bath = np.nan_to_num(abs_bath)

n_wet = np.array(np.where(abs_bath > 0,1,0),dtype=float)

wets = depth.wet.values

plt.contourf(abs_bath)
#plt.colorbar()



#plt.contourf(gtopo.lon.values,gtopo.lat.values,gtopo.elevation.values)
#plt.title("GEBCO global bathymetry 2020")
#plt.xlabel("Longitude")
#plt.ylabel("Latitude")
#plt.savefig("Bath.png")

dset = xr.Dataset({
    "depth" : (["nx","ny"],abs_bath),
    "wet" : (["nx","ny"],n_wet)})

dset.to_netcdf(out_dir+"depth_bob.nc")
#%%


figure,axis = plt.subplots(2,2)


axis[1,0].contourf(xx,yy,n_bath)
axis[1,0].set_title("BOB_depth")



axis[1,1].contourf(xx,yy,n_wet)
axis[1,1].set_title("wetness BOB")


axis[0,0].contourf(depth.depth.values)
axis[0,0].set_title("COAPS")
    


axis[0,1].contourf(depth.wet.values)
axis[0,1].set_title("COAPS wetness")


plt.suptitle("Depth data creation")


plt.savefig("depth_create.png")

#%% Sponge_m or initial conditions sponge files

""" Ptemp , salinity , water_u, water_v 11 layer """


#lons = np.arange(lon_min,lon_max,resx)
#lats = np.arange(lat_min,lat_max,resy)

lons = np.linspace(lon_min,lon_max,resx)
lats = np.linspace(lat_min,lat_max,resy)


saline_glo = xr.open_dataset("/home/vinay/Downloads/vosaline_ORAS5_1m_201812_r1x1.nc")

saline_bob = saline_glo.sel(lat = slice(lat_min-1,lat_max+1),lon = slice(lon_min-1,lon_max+1))

#plt.contourf(saline_bob.vosaline[0,0,:,:])



xlat = saline_bob.lat.values
ylon = saline_bob.lon.values

depth = saline_bob.deptht.values

dep_merge = []
for ii in range(11):
    vals = saline_bob.vosaline.values[0,ii,:,:]
    xm,ym = np.meshgrid(ylon,xlat)
    xf = xm.flatten()
    yf = ym.flatten()
    valsf = vals.flatten()
    saline_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")
    dep_merge += [saline_n]
    
saline_new = np.array(dep_merge)
saline_new = np.nan_to_num(saline_new)

#vals = saline_bob.vosaline.values[0,0,:,:]
#time = xr.Dataset({"time": dt.datetime(2114, 1, 2)})


#xm,ym = np.meshgrid(ylon,xlat) 
#xf = xm.flatten()
#yf = ym.flatten()
#valsf = vals.flatten()



#saline_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")


"""Ptemp"""


potemp_glo = xr.open_dataset("/home/vinay/Downloads/votemper_ORAS5_1m_201812_r1x1.nc")

potemp_bob = potemp_glo.sel(lat = slice(lat_min-1,lat_max+1),lon = slice(lon_min-1,lon_max+1))

#xlat = potemp_bob.lat.values
#ylon = potemp_bob.lon.values
#vals = potemp_bob.votemper.values[0,0,:,:]


#xm,ym = np.meshgrid(ylon,xlat) 
#xf = xm.flatten()
#yf = ym.flatten()
#valsf = vals.flatten()


#pot_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")n_dep

dept_merge = []
for jj in range(11):
    vals = potemp_bob.votemper.values[0,ii,:,:]
    xm,ym = np.meshgrid(ylon,xlat)
    xf = xm.flatten()
    yf = ym.flatten()
    valsf = vals.flatten()
    potemp_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")
    dept_merge += [potemp_n]
    
pot_new_fin = np.array(dept_merge)

pot_new_fin = np.nan_to_num(pot_new_fin)


#%%"""water u and water_v"""

cur_data = xr.open_dataset("/home/vinay/Downloads/oscar_vel10004.nc")

cur_bob = cur_data.sel(latitude = slice(lat_max + 1,lat_min - 1),longitude = slice(lon_min - 1,lon_max + 1))


xlat = cur_bob.latitude.values
ylon = cur_bob.longitude.values
valsu = cur_bob.u.values[0,0,:,:]
valsv = cur_bob.v.values[0,0,:,:]

xm,ym = np.meshgrid(ylon,xlat) 
xf = xm.flatten()
yf = ym.flatten()
valsfu = valsu.flatten()
valsfv = valsv.flatten()

u_val = griddata((xf,yf),valsfu,(lons[None,:],lats[:,None]),method="linear")

v_val = griddata((xf,yf),valsfv,(lons[None,:],lats[:,None]),method="linear")

u_nvals = []
v_nvals = []

for ii in range(11):
    u_nvals += [u_val]
    v_nvals += [v_val]

uvals_n = np.array(u_nvals)
vvals_n = np.array(v_nvals)

uvals_n = np.nan_to_num(uvals_n)
vvals_n = np.nan_to_num(vvals_n)


#plt.contourf(u_val)


#plt.contourf(ylon,xlat,valsu)

dd = sponge_m.water_u.values[0,0,:,:]

depth = sponge_m.depth.values

n_dep = np.linspace(depth[0],depth[-1],11)


time = np.datetime64('2005-02-25')

#%%
saline_new = np.expand_dims(saline_new,0)

#%%
pot_new_fin = np.expand_dims(pot_new_fin,0)


#%%
uvals_n = np.expand_dims(uvals_n,0)
vvals_n = np.expand_dims(vvals_n,0)

#%%

sponge_new = xr.Dataset({
    "ptemp" : (["time","depth","lat","lon"],pot_new_fin),
    "salinity" : (["time","depth","lat","lon"],saline_new),
    "water_u" : (["time","depth","lat","lon"],uvals_n),
    "water_v" : (["time","depth","lat","lon"],vvals_n)},
    coords = {"lon":(["lon",],lons),
              "lat":(["lat",],lats),
              "depth":(["depth",],n_dep),
              "time":(["time",],[np.datetime64("2005-02-25")])})

sponge_new.to_netcdf(out_dir+"final_sponge.nc")


#%% vgrid


dz = vgrid.dz.values

sigma = vgrid.sigma2.values
layer = vgrid.Layer.values


n_layer = np.linspace(layer[0],layer[-1],11)
n_dz = np.linspace(dz[0],dz[-1],11)
n_sigma = np.linspace(sigma[0],sigma[-1],12)

layer_n = xr.Dataset({
    "dz" : (["Layer"],n_dz),
    "sigma2": (["interfaces"],n_sigma)},
    coords = {"Layer":(["Layer",],n_layer)})

layer_n.to_netcdf(out_dir+"vgridbob.nc")


#%% tsuv filled

resx = 601
resy = 413



#lons = np.arange(lon_min,lon_max,resx)
#lats = np.arange(lat_min,lat_max,resy)

lons = np.linspace(lon_min-5,lon_max+5,resx)
lats = np.linspace(lat_min-5,lat_max+5,resy)


saline_glo = xr.open_dataset("/home/vinay/Downloads/vosaline_ORAS5_1m_201812_r1x1.nc")

saline_bob = saline_glo.sel(lat = slice(lat_min-10,lat_max+10),lon = slice(lon_min-10,lon_max+10))

#plt.contourf(saline_bob.vosaline[0,0,:,:])



xlat = saline_bob.lat.values
ylon = saline_bob.lon.values

depth = saline_bob.deptht.values



dep_merge = []
for ii in range(11):
    vals = saline_bob.vosaline.values[0,ii,:,:]
    xm,ym = np.meshgrid(ylon,xlat)
    xf = xm.flatten()
    yf = ym.flatten()
    valsf = vals.flatten()
    saline_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")
    dep_merge += [saline_n]

saline_new = np.array(dep_merge)
saline_new = np.nan_to_num(saline_new)

#vals = saline_bob.vosaline.values[0,0,:,:]
#time = xr.Dataset({"time": dt.datetime(2114, 1, 2)})


#xm,ym = np.meshgrid(ylon,xlat) 
#xf = xm.flatten()
#yf = ym.flatten()
#valsf = vals.flatten()



#saline_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")


"""Ptemp"""


potemp_glo = xr.open_dataset("/home/vinay/Downloads/votemper_ORAS5_1m_201812_r1x1.nc")

potemp_bob = potemp_glo.sel(lat = slice(lat = slice(lat_min-10,lat_max+10),lon = slice(lon_min-10,lon_max+10)))

#xlat = potemp_bob.lat.values
#ylon = potemp_bob.lon.values
#vals = potemp_bob.votemper.values[0,0,:,:]


#xm,ym = np.meshgrid(ylon,xlat) 
#xf = xm.flatten()
#yf = ym.flatten()
#valsf = vals.flatten()


#pot_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")

dept_merge = []


for jj in range(11):
    vals = potemp_bob.votemper.values[0,ii,:,:]
    xm,ym = np.meshgrid(ylon,xlat)
    xf = xm.flatten()
    yf = ym.flatten()
    valsf = vals.flatten()
    potemp_n = griddata((xf,yf),valsf,(lons[None,:],lats[:,None]),method="linear")
    dept_merge += [potemp_n]
    


pot_new_fin = np.array(dept_merge)


pot_new_fin = np.nan_to_num(pot_new_fin)


#%%"""water u and water_v"""

cur_data = xr.open_dataset("/home/vinay/Downloads/oscar_vel10004.nc")

cur_bob = cur_data.sel(latitude = slice(lat = slice(lat_min-10,lat_max+10),lon = slice(lon_min-10,lon_max+10))



xlat = cur_bob.latitude.values
ylon = cur_bob.longitude.values
valsu = cur_bob.u.values[0,0,:,:]
valsv = cur_bob.v.values[0,0,:,:]


xm,ym = np.meshgrid(ylon,xlat) 
xf = xm.flatten()
yf = ym.flatten()
valsfu = valsu.flatten()
valsfv = valsv.flatten()



u_val = griddata((xf,yf),valsfu,(lons[None,:],lats[:,None]),method="linear")

v_val = griddata((xf,yf),valsfv,(lons[None,:],lats[:,None]),method="linear")

u_nvals = []
v_nvals = []


for ii in range(11):
    u_nvals += [u_val]
    v_nvals += [v_val]

uvals_n = np.array(u_nvals)
vvals_n = np.array(v_nvals)

uvals_n = np.nan_to_num(uvals_n)
vvals_n = np.nan_to_num(vvals_n)


#plt.contourf(u_val)


#plt.contourf(ylon,xlat,valsu)

dd = sponge_m.water_u.values[0,0,:,:]

depth = sponge_m.depth.values

n_dep = np.linspace(depth[0],depth[-1],11)


time = np.datetime64('2005-02-25')

#%%
saline_new = np.expand_dims(saline_new,0)

#%%
pot_new_fin = np.expand_dims(pot_new_fin,0)


#%%
uvals_n = np.expand_dims(uvals_n,0)
vvals_n = np.expand_dims(vvals_n,0)

#%%

tsuv_filled = xr.Dataset({
    "ptemp" : (["time","depth","lat","lon"],pot_new_fin),
    "salinity" : (["time","depth","lat","lon"],saline_new),
    "water_u" : (["time","depth","lat","lon"],uvals_n),
    "water_v" : (["time","depth","lat","lon"],vvals_n)},
    coords = {"lon":(["lon",],lons),
              "lat":(["lat",],lats),
              "depth":(["depth",],n_dep),
              "time":(["time",],[np.datetime64("2005-02-25")])})

sponge_new.to_netcdf(out_dir+"tsuv_init.nc")

