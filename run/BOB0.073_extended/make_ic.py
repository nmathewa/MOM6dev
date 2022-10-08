# This will make a IC file for MOM6
# Do regridding prior to this using cdo and with
# ocean_geometry.nc file.
# BOB0.073 extended

import xarray as xr
import numpy as np
from HCtFlood import kara as flood

# functions
def vgrid_to_interfaces(vgrid, max_depth=6500.0):
	if isinstance(vgrid, xr.DataArray):
		vgrid = vgrid.data
	zi = np.zeros(len(vgrid)+1)
	for i in range(1,len(zi)-1):
		zi[i] = vgrid[i]+zi[i-1]
	zi[-1] = max_depth
	return zi 

def vgrid_to_layers(vgrid, max_depth=6500.0):
	if isinstance(vgrid, xr.DataArray):
		vgrid = vgrid.data 
	ints = vgrid_to_interfaces(vgrid, max_depth=max_depth)
	z = (ints + np.roll(ints, shift=1))/2
	layers = z[1:]
	return layers

# open files
tracer_ic_file = xr.open_dataset("tracer.nc")
u_ic_file = xr.open_dataset("u.nc")
v_ic_file = xr.open_dataset("v.nc")
vgrid_file = xr.open_dataset("bob_vgrid.nc")

vgrid = vgrid_file["dz"]
z = vgrid_to_layers(vgrid)

# Target z levels for the IC file
ztarget = xr.DataArray(
		z,
		name='zl',
		dims=['zl'],
		coords={'zl':z},
)

# IC files
ic_t = (
		tracer_ic_file
		[["thetao_mean", "so_mean"]]
        .rename({"lonh":"lon", "lath":"lat"})
)

ic_u = (
		u_ic_file
		[["uo_mean"]]
        .rename({"lonq":"lon", "lath":"lat"})
)

ic_v = (
		v_ic_file
		[["vo_mean"]]
        .rename({"lonh":"lon", "latq":"lat"})
)

# Interpolate GLORYS vertically onto target grid.
# Depths below bottom of GLORYS are filled by extrapolating the deepest available value.
revert_tracer = ic_t.interp(depth=ztarget, kwargs={"fill_value": "extrapolate"}).ffill("zl", limit=None)

revert_u = ic_u.interp(depth=ztarget, kwargs={"fill_value": "extrapolate"}).ffill("zl", limit=None)

revert_v = ic_v.interp(depth=ztarget, kwargs={"fill_value": "extrapolate"}).ffill("zl", limit=None)


# flood temperature and salinity over land
#flooded_tracer = xr.merge((
#		flood.flood_kara(revert_tracer[v], zdim="zl") for v in ["thetao_mean", "so_mean"]
#))

#flooded_tracer = revert_tracer

flooded_tracer = xr.merge((
		flood.flood_kara(revert_tracer[v], zdim="zl") for v in ["thetao_mean", "so_mean"]
))

flooded_u = xr.merge((
		flood.flood_kara(revert_u[v], zdim="zl") for v in ["uo_mean"]
))

flooded_v = xr.merge((
		flood.flood_kara(revert_v[v], zdim="zl") for v in ["vo_mean"]
))


# fixing output metadata
# for tracer files
all_vars = list(flooded_tracer.data_vars.keys()) + list(flooded_tracer.coords.keys())
encodings = {v:{"_FillValue":1.0e20} for v in all_vars}
encodings["time"].update({"dtype":"float64", "calendar":"noleap"})

flooded_tracer["zl"].attrs = {
	"long_name" : "Layer pseudo-depth, -z*",
	"units":"meter",
	"cartesian_axis":"Z",}

flooded_tracer.to_netcdf(
	"ic_tracer.nc",
	format="NETCDF3_64BIT",
	engine="netcdf4",
	encoding=encodings,
	unlimited_dims="time")

# for u files
all_vars = list(flooded_u.data_vars.keys()) + list(flooded_u.coords.keys())
encodings = {v:{"_FillValue":1.0e20} for v in all_vars}
encodings["time"].update({"dtype":"float64", "calendar":"noleap"})

flooded_u["zl"].attrs = {
	"long_name" : "Layer pseudo-depth, -z*",
	"units":"meter",
	"cartesian_axis":"Z",}

flooded_u.to_netcdf(
	"ic_u.nc",
	format="NETCDF3_64BIT",
	engine="netcdf4",
	encoding=encodings,
	unlimited_dims="time")

# for v files
all_vars = list(flooded_v.data_vars.keys()) + list(flooded_v.coords.keys())
encodings = {v:{"_FillValue":1.0e20} for v in all_vars}
encodings["time"].update({"dtype":"float64", "calendar":"noleap"})

flooded_v["zl"].attrs = {
	"long_name" : "Layer pseudo-depth, -z*",
	"units":"meter",
	"cartesian_axis":"Z",}

flooded_v.to_netcdf(
	"ic_v.nc",
	format="NETCDF3_64BIT",
	engine="netcdf4",
	encoding=encodings,
	unlimited_dims="time")
