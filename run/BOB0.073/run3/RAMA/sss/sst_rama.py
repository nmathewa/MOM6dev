import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 

# 8 N 90 E
sst_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst8n90e_dy.cdf")
sst_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst_model_8n90e.nc")
sst_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sst/sst_model_8n90e.nc")

plt.figure(1)
sst_obs["T_25"].plot(label="Obs", linewidth=3)
sst_m1["SST"].plot(label="ERA", linestyle="dashed")
sst_m3["SST"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sst_8n90e.png")

# 12 N 90 E
sst_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst12n90e_dy.cdf")
sst_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst_model_12n90e.nc")
sst_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sst/sst_model_12n90e.nc")

plt.figure(2)
sst_obs["T_25"].plot(label="Obs", linewidth=3)
sst_m1["SST"].plot(label="ERA", linestyle="dashed")
sst_m3["SST"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sst_12n90e.png")


# 15 N 90 E
sst_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst15n90e_dy.cdf")
sst_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sst/sst_model_15n90e.nc")
sst_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sst/sst_model_15n90e.nc")

plt.figure(3)
sst_obs["T_25"].plot(label="Obs", linewidth=3)
sst_m1["SST"].plot(label="ERA", linestyle="dashed")
sst_m3["SST"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sst_15n90e.png")
