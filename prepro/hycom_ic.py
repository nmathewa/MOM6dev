# This file is used to merge the bottom and interior variables
# field of the HYCOM reanalysis. Also, regridding is carried
# out from input regrid to model grid

import xarray as xr
import numpy as np
import xesmf as xe

# files 
ic = xr.open_dataset("~/Desktop/bob_ic.nc")
tf= xr.open_dataset("~/Desktop/ocean_geometry.nc")

# empty variables
salt = np.zeros([1,41,283,301])
temp = np.zeros([1,41,283,301])
uo = np.zeros([1,41,283,301])
vo = np.zeros([1,41,283,301])

# assign variables
eta = ic["surf_el"].values 

s = ic["salinity"].values 
sb = ic["salinity_bottom"].values

t = ic["water_temp"].values
tb = ic["water_temp_bottom"].values

u = ic["u"].values 
ub = ic["water_u_bottom"].values

v = ic["v"].values 
vb = ic["water_v_bottom"].values

# loop
for time in range(len(temp)):
    for depth in range(len(temp[0])-1):
        for lat in range(len(temp[0][0])):
            for lon in range(len(temp[0][0][0])):
                salt[time,depth,lat,lon] = s[time,depth,lat,lon]
                temp[time,depth,lat,lon] = t[time,depth,lat,lon]
                uo[time,depth,lat,lon] = u[time,depth,lat,lon]
                vo[time,depth,lat,lon] = v[time,depth,lat,lon]
                                


# bottom values
salt[0,-1,:,:] = sb[:,:,:]
temp[0,-1,:,:] = tb[:,:,:]
uo[0,-1,:,:] = ub[:,:,:]
vo[0,-1,:,:] = vb[:,:,:]

depth = np.zeros(41)
depth[:-1] = ic.depth.values
depth[-1] = 5500.0


ds = xr.Dataset(
    data_vars=dict(
        salt=(["Time", "depth", "lat", "lon"], salt),
        temp=(["Time", "depth", "lat", "lon"], temp),
        u=(["Time", "depth", "lat", "lon"], uo),
        v=(["Time", "depth", "lat", "lon"], vo),
        eta=(["Time", "lat", "lon"], eta), 
    ),
    coords=dict(
        lon=ic.lon.values,
        lat=ic.lat.values,
        Time=ic.time.values,
        depth=depth,
    ),
)

# Fix output metadata, including removing all _FillValues.
all_vars = list(ds.data_vars.keys()) + list(ds.coords.keys())
encodings = {v: {'_FillValue': 1.0e20, "missing_value": 1.0e20} for v in all_vars}
encodings['Time'].update({'dtype':'float64', 'calendar': 'gregorian'})


# Regridding to model target grid
target_tracer = (tf[["lath", "lonh"]])
target_u = (tf[["lath", "lonq"]])
target_v = (tf[["latq", "lonh"]])

ds_tracer = ds[["salt", "temp", "eta"]]
ds_u = ds[["u"]]
ds_v = ds[["v"]]

regrid_tracer = xe.Regridder(ds_tracer, target_tracer, method="bilinear", extrap_method="nearest_s2d")
regrid_u = xe.Regridder(ds_u, target_u, method="bilinear", extrap_method="nearest_s2d")
regrid_v = xe.Regridder(ds_v, target_v, method="bilinear", extrap_method="nearest_s2d")

# do the regridding
rg_s = regrid_tracer(ds["salt"])
rg_t = regrid_tracer(ds["temp"])
rg_h = regrid_tracer(ds["eta"])

rg_u = regrid_u(ds["u"])
rg_v = regrid_v(ds["v"])

# to xarray data array
da_s = xr.DataArray(rg_s, name="salt")
da_t = xr.DataArray(rg_t, name="temp")
da_h = xr.DataArray(rg_h, name="ssh")

da_u = xr.DataArray(rg_u, name="u")
da_v = xr.DataArray(rg_v, name="v")

ds = xr.merge((da_s, da_t, da_h, da_u, da_v))


# Fix output metadata, including removing all _FillValues.
all_vars = list(ds.data_vars.keys()) + list(ds.coords.keys())
encodings = {v: {'_FillValue': 1.0e20, "missing_value": 1.0e20} for v in all_vars}
encodings['Time'].update({'dtype':'float64', 'calendar': 'gregorian'})
# make a file
ds.to_netcdf("~/Desktop/ic_final.nc", encoding=encodings)
