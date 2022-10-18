# Open Boundary file generation

We use the OBC for southern and western boundary of the domain. We shall use CDO and python for making the OBC files.

## Download the data
We will use the Copernicus Marine Ensemble reanalyses product which has daily frequency. Take a spread of 0.5 degree around the boundary like if -4 N is the southern boundary take -4.5N to -3.5N as the data files(and spanning the longitude).

## Make a grid description file
Use CDO command griddes to get the grid description of the staggered grid from ocean_geometry.nc file(output to a file). Then, edit the griddes file in way that the western and eastern boundaries will have a single longitude(constant xh or xq) and northern and southern boundaries will have a single latitude(constant yh or yq).

Eg: following is the grid for tracer fields(temp, salt, ssh):
```
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
```
we change it to(for southern boundary) as :
```
gridtype  = lonlat
#gridsize  = 118800
xsize     = 300
ysize     = 1 # change here
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
```
Then remap the raw files by the above grid description file. Similarly do for u points and v points and other boundaries.

## Vertical remapping
Now, do the vertical remapping to the target grid of the model using Python.(Below for southern boundary)
```
import xarray as xr

obc_file = xr.open_dataset("south.nc")
target_grid = xr.open_dataset("~/HDD_data/vinay/testing/run/new/ic_file/ic_tracer.nc")

depth_levels = target_grid["zl"]

west_obc = obc_file.interp(depth=depth_levels)
west_obc.to_netcdf("SOUTH.nc")
```
