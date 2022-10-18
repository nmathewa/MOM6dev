# Python file to calculate dz and append it to various fields

import xarray as xr
import numpy as np

da = xr.open_dataset("final_south.nc")
zl = da.coords["ZL"]

dz = np.zeros_like(zl)
#dz[0] = zl[0] - 0.0
dz[0] = 1.0

da["PT_SEGMENT_001"] = da["PT_SEGMENT_001"] + 273.15
for i in range(1,len(zl)):
	dz[i] = zl[i] - zl[i-1]
	print(dz[i])

pre_var_u = da["U11_SEGMENT_001"]
pre_var_v = da["V11_SEGMENT_001"]
pre_var_trace = da["PT_SEGMENT_001"]

DZ_U11_SEGMENT_001 = np.zeros_like(pre_var_u)
DZ_V11_SEGMENT_001 = np.zeros_like(pre_var_v)
DZ_PT_SEGMENT_001 = np.zeros_like(pre_var_trace)
DZ_S_SEGMENT_001 = np.zeros_like(pre_var_trace)

# u velocity
for time in range(len(pre_var_u)):
	for z in range(len(pre_var_u[0])):
		for lat in range(len(pre_var_u[0][0])):
			for lon in range(len(pre_var_u[0][0][0])):
				DZ_U11_SEGMENT_001[time][z][lat][lon] = dz[z]

# v velocity
for time in range(len(pre_var_v)):
        for z in range(len(pre_var_v[0])):
                for lat in range(len(pre_var_v[0][0])):
                        for lon in range(len(pre_var_v[0][0][0])):
                                DZ_V11_SEGMENT_001[time][z][lat][lon] = dz[z]

# temp, salt/tracers
for time in range(len(pre_var_trace)):
        for z in range(len(pre_var_trace[0])):
                for lat in range(len(pre_var_trace[0][0])):
                        for lon in range(len(pre_var_trace[0][0][0])):
                                DZ_PT_SEGMENT_001[time][z][lat][lon] = dz[z]
                                DZ_S_SEGMENT_001[time][z][lat][lon] = dz[z]

new_dataset = xr.Dataset({})

new_dataset = da

new_dataset["DZ_U11_SEGMENT_001"] = (('time', 'ZL', 'lath', 'lonq'), DZ_U11_SEGMENT_001)
new_dataset["DZ_V11_SEGMENT_001"] = (('time', 'ZL', 'latq', 'lonh'), DZ_V11_SEGMENT_001)
new_dataset["DZ_PT_SEGMENT_001"] = (('time', 'ZL', 'lath', 'lonh'), DZ_PT_SEGMENT_001)
new_dataset["DZ_S_SEGMENT_001"] = (('time', 'ZL', 'lath', 'lonh'), DZ_S_SEGMENT_001)

print(new_dataset)

new_dataset.to_netcdf("SOUTH.nc")
