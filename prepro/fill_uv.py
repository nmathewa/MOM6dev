# This script fills in the invalid , NaN 
# values in the velocity fields, uand v with 0
# over land and below bathymetry are also filled with 0


import xarray as xr
import numpy as np

ic = xr.open_dataset("~/Desktop/ic_final.nc")
topo_u = xr.open_dataset("~/Desktop/bathy_u.nc")
topo_v = xr.open_dataset("~/Desktop/bathy_v.nc")
mask_file_u = xr.open_dataset("~/Desktop/ocean_mask_u.nc")
mask_file_v = xr.open_dataset("~/Desktop/ocean_mask_v.nc")
hgrid = xr.open_dataset("~/Desktop/bob_hor.nc")

# variable field required
u = ic["u"].values
v = ic["v"].values
bathy_u = topo_u["elevation"].values
bathy_v = topo_v["elevation"].values
mask_u = mask_file_u["mask"].values 
mask_v = mask_file_v["mask"].values


# empty arrays
uo = np.zeros(np.shape(u))
vo = np.zeros(np.shape(v))

# main loop for u
for time in range(len(u)):
    for depth in range(len(u[0])):
        for lat in range(len(u[0][0])):
            for lon in range(len(u[0][0][0])):
                if ((mask_u[lat,lon] > 0.5) and (u[time,depth,lat,lon] == u[time,depth,lat,lon])):
                    uo[time,depth,lat,lon] = u[time,depth,lat,lon]




                '''if ((u[time,depth,lat,lon] != u[time,depth,lat,lon]) and (mask_u[lat,lon] > 0.0)):
                    if(depth < bathy_u[lat, lon]):
                        uo[time,depth,lat,lon] = u[time,depth-1,lat,lon]
                    else:
                        uo[time,depth,lat,lon] = 1.0e20
                
                if ((u[time,depth,lat,lon] != u[time,depth,lat,lon]) and (mask_u[lat,lon] < 1.0)):
                    uo[time,depth,lat,lon] = 1.0e20
                
                if (u[time,depth,lat,lon] > 1.0e20):
                    uo[time,depth,lat,lon] = 1.0e20
                    

for time in range(len(u)):
    for depth in range(1):
        for lat in range(len(u[0][0])):
            for lon in range(len(u[0][0][0])):
                if (mask_u[lat,lon] < 1.0):
                    u[time,depth,lat,lon] = 1.0e20
                if ((u[time,depth,lat,lon] != u[time,depth,lat,lon]) and (mask_u[lat,lon] < 1.0)):
                    u[time,depth,lat,lon] = 1.0e20
                if (u[time,depth,lat,lon] > 1.0e20):
                    uo[time,depth,lat,lon] = 1.0e20'''


# main loop for v 
'''for time in range(len(v)):
    for depth in range(1, len(v[0])):
        for lat in range(len(v[0][0])):
            for lon in range(len(v[0][0][0])):
                vo[time,depth,lat,lon] = v[time,depth,lat,lon]
                if ((v[time,depth,lat,lon] != v[time,depth,lat,lon]) and (mask_v[lat,lon] > 0.0)):
                    if(depth < bathy_v[lat, lon]):
                        vo[time,depth,lat,lon] = v[time,depth-1,lat,lon]
                    else:
                        vo[time,depth,lat,lon] = 1.0e20
                
                if ((v[time,depth,lat,lon] != v[time,depth,lat,lon]) and (mask_v[lat,lon] < 1.0)):
                    vo[time,depth,lat,lon] = 1.0e20
                if (v[time,depth,lat,lon] > 1.0e20):
                    vo[time,depth,lat,lon] = 1.0e20

for time in range(len(v)):
    for depth in range(1):
        for lat in range(len(v[0][0])):
            for lon in range(len(v[0][0][0])):
                if (mask_v[lat,lon] < 1.0):
                    v[time,depth,lat,lon] = 1.0e20
                if ((v[time,depth,lat,lon] != v[time,depth,lat,lon]) and (mask_v[lat,lon] < 1.0)):
                    v[time,depth,lat,lon] = 1.0e20
                if (v[time,depth,lat,lon] > 1.0e20):
                    vo[time,depth,lat,lon] = 1.0e20
'''
for time in range(len(v)):
    for depth in range(len(v[0])):
        for lat in range(len(v[0][0])):
            for lon in range(len(v[0][0][0])):
                if ((mask_v[lat,lon] > 0.5) and (v[time,depth,lat,lon] == v[time,depth,lat,lon])):
                    vo[time,depth,lat,lon] = v[time,depth,lat,lon]

# to dataset
depth = ic.depth.values
ds = xr.Dataset(
    data_vars=dict(
        u=(["Time", "depth", "lath", "lonq"], uo),
        v=(["Time", "depth", "latq", "lonh"], vo),
    ),
    coords=dict(
        lonq=ic.lonq.values,
        lath=ic.lath.values,
        lonh=ic.lonh.values,
        latq=ic.latq.values,
        Time=ic.Time.values,
        depth=depth,
    ),
)

# to file
ds.to_netcdf("~/Desktop/uv_ic.nc")

