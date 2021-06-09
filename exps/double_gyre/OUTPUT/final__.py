
"""
Created on Tue Jun  8 00:38:45 2021

@author: mathew

"""
import os
import xarray as xr
import numpy as np

os.chdir(os.getenv("IISC")+"/exps/double_gyre/double_gyre/OUTPUT/")

rd = xr.open_dataset('prog__0001_006.nc')

geo = xr.open_dataset("../INPUT/ocean_geometry.nc")



alls = list(geo.keys())

tx = geo["dxT"].values
ty = geo["dyT"].values

dd = geo["dxBu"].values

#%%
import numpy as np

x1lon = 88
x2lon = 92
y1lat = 16
y2lat = 19

lonq = np.arange(x1lon,x2lon,0.5)
latq = np.arange(y1lat,y2lat,0.5)

lonh = []
for ii in range(len(lonq)-1):
    lonh += [(lonq[ii+1] + lonq[ii])/2]

lonh = np.array(lonh)

lath = []
for jj in range(len(latq)-1):
    lath += [(latq[jj+1] + latq[jj])/2]

lath = np.array(lath)

geolonb,geolatb = np.meshgrid(lonq,latq)

geolat,geolon = np.meshgrid(lonh,lath)





#%% Depth

dp_t = np.random.randint(180,580,(np.shape(geolat)))

D = dp_t
#%% corioils

def cor(latitude):
    om = (2*(np.pi))/(24*60*60)
    f = 2*om*(np.sin((latitude*np.pi)/180))
    return f

ff = cor(geolat)

f = ff
#%% u,v points

# zonal grid spacing at v points (latq,lonh)

#|--v--.--v--|
#|  x  |  x  |
#|--v--.--v--|

dxv = []
for xxx in range(len(lonq)-1):
    dxv += [lonq[xxx+1] - lonq[xxx]]

dxvz = np.array(dxv)*111*1000

dxvz = np.meshgrid(dxvz,latq)[0]


# Meridional spacing at u points (lath,lonq)

dyu = []
for xxx in range(len(latq)-1):
    dyu += [latq[xxx+1] - latq[xxx]]
    
dyum = np.array(dyu)*111*1000

dyum = np.meshgrid(lonq,dyum)[1]

#zonal grid spacing at u points (lath,lonq)

dxu = np.array(dyu)*111*1000

dxuz = np.meshgrid(lonq,dxu)[1]

#meridional grid spacing at v points (latq,lonh)

dyv = np.array(dxv)*111*1000

dyvm = np.meshgrid(dyv,latq)[0]

dxCv = dxvz
dyCu = dyum
dxCu = dxuz
dyCv = dyvm


#%% h points 

dx = np.array(dxv)*111*1000
dy = np.array(dyu)*111*1000

dxh,dyh = np.meshgrid(dx,dy)

dxT,dyT = dxh,dyh

#%% q points

nn = np.ones(np.shape(geolonb))

dxq,dyq = nn*55500,nn*55500

dxBu,dyBu = dxq,dyq
#%%Area H

Ah = dxh*dyh


#%% Area q

Aq = dxq*dyq

#%% open u points


rr = np.zeros((len(dyvm.T)))
dxzvo = dyvm

for ii in range(len(rr)):
    dxzvo[0,ii] = 0
    dxzvo[-1,ii] = 0

rr = np.zeros((len(dxuz)))
dxzuo = dxuz

for jj in range(len(rr)):
    dxzuo[jj,0] = 0
    dxzuo[jj,0] = 0
    
dxCvo,dyCuo = dxzvo,dxzuo
#%%wetness

w = np.ones(np.shape(geolat))

wet = w
#%%create datarray



dset_n = xr.Dataset({
    "geolatb":(["latq","lonq"],geolatb),"geolonb":(["latq","lonq"],geolatb),
    "geolat":(["lath","lonh"],geolat),"geolon":(["lath","lonh"],geolon),
    "D":(["lath","lonh"],D),"f":(["lath","lonh"],f),"dxCv":(['latq','lonh'],dxCv),
    "dyCu":(["lath","lonq"],dyCu),"dxCu":(["lat","lon"],dxCu),"dxT":(["lath","lonh"],dxT),
    "dyT":(["lath","lonh"],dyT),"dxBu":(["latq","lonq"],dxBu),"dyBu":(["latq","lonq"],dyBu),
    "Ah":(["lath","lonh"],Ah),"Aq":(["latq","lonq"],Aq),"dxCvo":(["latq","lonh"],dxCvo),
    "dyCuo":(["lath","lonq"],dyCuo),"wet":(["lath","lonh"],wet)    
    },
    coords = {"lath":(["lath",],lath),
              "lonh":(["lonh",],lonh),
              "latq":(["latq",],latq),
              "lonq":(["lonq",],lonq)})
