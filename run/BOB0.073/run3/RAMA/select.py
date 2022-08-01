import xarray as xr

ds = xr.open_dataset("~/HDD2/runs/run3/run3.nc")

# temperature
t = ds["SST"].sel(xh=["90."], yq=["8."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sst/sst_model_8n90e.nc")

t = ds["SST"].sel(xh=["90."], yq=["12."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sst/sst_model_12n90e.nc")

t = ds["SST"].sel(xh=["90."], yq=["15."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sst/sst_model_15n90e.nc")

# salt
t = ds["SSS"].sel(xh=["90."], yq=["8."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sss/sss_model_8n90e.nc")

t = ds["SSS"].sel(xh=["90."], yq=["12."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sss/sss_model_12n90e.nc")

t = ds["SSS"].sel(xh=["90."], yq=["15."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/sss/sss_model_15n90e.nc")

# ssu
t = ds["SSU"].sel(xh=["90."], yq=["8."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssu_model_8n90e.nc")

t = ds["SSU"].sel(xh=["90."], yq=["12."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssu_model_12n90e.nc")

t = ds["SSU"].sel(xh=["90."], yq=["15."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssu_model_15n90e.nc")

# ssv
t = ds["SSV"].sel(xh=["90."], yq=["8."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssv_model_8n90e.nc")

t = ds["SSV"].sel(xh=["90."], yq=["12."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssv_model_12n90e.nc")

t = ds["SSV"].sel(xh=["90."], yq=["15."], method="nearest")
t.to_netcdf("~/HDD2/runs/run3/RAMA/currents/ssv_model_15n90e.nc")
