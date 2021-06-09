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


latq = geo.latq.values
lonq = geo.lonq.values
geolatb = geo.geolatb.values
geolonb = geo.geolonb.values


#### After finding dx and Dy (latq-1,lonq-1)
lonh = geo.lonh.values
lath = geo.lath.values
geolat = geo.geolat.values
geolon = geo.geolon.values


D = geo.D.values
f = geo.f.values

alls = list(geo.keys())

tx = geo["dxT"].values
ty = geo["dyT"].values

dd = geo["dxBu"].values

#%%


# setting up lat/lon
x1lon = 88.3
x2lon = 92.1
y1lat = 16.8
y2lat = 19.6

lonq = np.arange(x1lon,x2lon,0.25)
latq = np.arange(y1lat,y2lat,0.25)

geolon,geolat = np.meshgrid(lonq,latq)

#%%

# measuring distances zonal spacing at v points (latq,lonh) zv

def create_llgrid(x1,x2,y1,y2,gdx,gdy):
    lats = np.linspace(y1,y2,gdy)
    lons = np.linspace(x1,x2,gdx)
    x,y = np.meshgrid(lons,lats)
    dx1,dy1 = [],[]
    for ii in range(len(lons)-1):
        dx1 += [lons[ii+1]-lons[ii]]
    for jj in range(len(lats)-1):
        dy1 += [lats[jj+1]-lats[jj]]
    dx1 = np.array(dx1)*71.5*1000
    dy1 = np.array(np.abs(dy1))*111.3*1000
    dxx,dyy = np.meshgrid(dx1,dy1)
    area = dxx*dyy
    dx,yy = np.meshgrid(dx1,lats)
    xx,dy = np.meshgrid(lons,dy1)
    return x,y,dx,dy,area

dxv = []
lonh = []
for ii in range(len(lonq)-1):
        dxv += [lonq[ii+1]-lonq[ii]]
        lonh += [lonq[ii]]
dxv = np.array(dxv)*71.5*1000

lonh = np.array(lonh)
dxzv,yy = np.meshgrid(dxv,latq)

# measuring distances meridional grid spacing at u points (lath,lonq) mu

dyu = []
lath = []
for ii in range(len(latq)-1):
        dyu += [latq[ii+1]-latq[ii]]
        lath += [latq[ii]]
dyu = np.array(dyu)*111.3*1000



lath = np.array(lath)
xx,dymu = np.meshgrid(lonq,dyu)


# measuring zonal grid spacing at u points (lath,lonq) zu

xx,dxzu = np.meshgrid(lonq,dyu)


# meridional grid spacing at v points (latq,lonh) mv

yy,dymv = np.meshgrid(latq,dxv)


# zonal grid spacing at h points (lath,lonh)


xx,dxzh = np.meshgrid(lath,dxv)

# meridional grid spacing at h points (lath,lonh)

dymh,yy = np.meshgrid(dyu,lath)

#zonal grid spacing at q points (latq,lonq)

xx,dxzq = np.meshgrid(lonq,latq)

#meridional grid spacing at q points (latq,latq)



# Area oh h cells (lath,lonh)

dx,dy = np.meshgrid(dxv,dyu)

area = dx*dy

# open zonal grid spacing at v points (lath,lonh)
xx,dxzo = np.meshgrid(lath,dxv)

# open meridional grid spacing at u points(lath,lonh)

dymo,yy = np.meshgrid(dyu,lath)

# land or ocean

loc = np.ones(np.shape(dxzo))

#gelon,gelat,geola
#%%

# f- coriolis parameter f = omega*sin(lat)

om = (2*(np.pi))/(24*60*60)
lat = 40

f = 2*om*(np.sin((lat*np.pi)/180))

def cor(latitude):
    om = (2*(np.pi))/(24*60*60)
    f = 2*om*(np.sin((latitude*np.pi)/180))
    return f


geolat = np.meshgrid(lats,lons)[0]
ff = cor(geolat)


#%%
# depth D


dp_dt = "/home/mathew/hdd/UBU20/hdd/IISC_PA/exps/double_gyre/double_gyre/INPUT/GEBCO_2020_08_Jun_2021_60c934f78cd7/gebco_2020_n20.9619140625_s9.052734375_w84.0673828125_e96.240234375.nc"

dp = xr.open_dataset(dp_dt)

ele = dp.elevation
elat,elon = ele.lat.values,ele.lon.values

region_ele = ele.sel(lon=slice(min(lons),max(lons)),lat=slice(min(lats),max(lats)))

from scipy.interpolate import griddata

#ss = griddata((lath,lonh),region_ele.values,(elat,elon))

dp_t = np.random.randint(180,580,(np.shape(dxzo)))

#%%
import scipy.interpolate as inte

interp = inte.RegularGridInterpolator(tuple((lons,lats)), region_ele.values)

#%%create nc

dset = xr.Dataset({
    "geolatb":(["latq","lonq"],geolatb),"geolonb":(["latq","lonq"],geolatb),
    "geolat":(["lath","lonh"],geolat),"geolon":(["lath","lonh"],geolon),
    "D":(["lath","lonh"],d),"f":(["lath","lonh"]),"dxCv":(['latq','lonq'],dxcv),
    "dyCu":(["lath","lonh"],dycu),"dxcu":(["lat"])
    
    })