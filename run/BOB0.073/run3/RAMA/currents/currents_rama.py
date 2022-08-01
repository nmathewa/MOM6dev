import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 

# 8 N 90 E
ssu_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/cur8n90e_dy.cdf")
ssu_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/ssu_model_8n90e.nc")
ssu_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/currents/ssu_model_8n90e.nc")

ssu_m3 = ssu_m3*100
plt.figure(1)
ssu_obs["U_320"].plot(label="Obs", linewidth=3)
ssu_m1["SSU"].plot(label="ERA", linestyle="dashed")
ssu_m3["SSU"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("ssu_8n90e.png")

# 12 N 90 E
ssu_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/cur12n90e_dy.cdf")
ssu_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/ssu_model_12n90e.nc")
ssu_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/currents/ssu_model_12n90e.nc")

ssu_m3 = ssu_m3*100
plt.figure(2)
ssu_obs["U_320"].plot(label="Obs", linewidth=3)
ssu_m1["SSU"].plot(label="ERA", linestyle="dashed")
ssu_m3["SSU"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("ssu_12n90e.png")


# 15 N 90 E
ssu_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/cur15n90e_dy.cdf")
ssu_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/currents/ssu_model_15n90e.nc")
ssu_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/currents/ssu_model_15n90e.nc")

ssu_m3 = ssu_m3*100
plt.figure(3)
ssu_obs["U_320"].plot(label="Obs", linewidth=3)
ssu_m1["SSU"].plot(label="ERA", linestyle="dashed")
ssu_m3["SSU"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("ssu_15n90e.png")
