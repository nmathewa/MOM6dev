# Initial conditions files preparation

We shall use CDO and python to generate the initial conditions files.

## Download the ic file
We use the NEMO renalyses ensemble for Copernicus Marine.

## Remap the ic file.
Use the ocean_geometry.nc file by running MOM6 case using WRITE_GEOMETRY. This file contains the staggered grid.
### Tracer remap
```
cdo select,name=so_mean,thetao_mean ic.nc tracer.nc
```
for grid description
```
cdo griddes ocean_geometry.nc
```
use the lath, lonh for the tracer grid

grid_t.txt
```
#
# gridID 2
#
gridtype  = lonlat
gridsize  = 118800
xsize     = 300
ysize     = 396
xname     = lonh
xlongname = "Longitude"
xunits    = "degrees_east"
yname     = lath
ylongname = "Latitude"
yunits    = "degrees_north"
xfirst    = 77.0366666666667
xinc      = 0.0733333333333334
yfirst    = -3.96338383838384
yinc      = 0.0732323232323232
scanningMode = 64
```
remap it now using the grid description
```
cdo remapcon,grid_t.txt tracer.nc o.nc
```
### U and V velocity remap
use xq, yh grid for u and yh,xq for v
```
cdo remapbic,grid_v.txt v.nc o.nc
```

### Flooding and interpolating the NaN values
use python file make_ic.py which has input files as vertical grid file, the three remapped ic files to finally get the input files for the case(one for tracers and two for u and v)
