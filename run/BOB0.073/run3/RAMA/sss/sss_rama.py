import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 

# 8 N 90 E
sss_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss8n90e_dy.cdf")
sss_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss_model_8n90e.nc")
sss_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sss/sss_model_8n90e.nc")

plt.figure(1)
sss_obs["S_41"].plot(label="Obs", linewidth=3)
sss_m1["SSS"].plot(label="ERA", linestyle="dashed")
sss_m3["SSS"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sss_8n90e.png")

# 12 N 90 E
sss_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss12n90e_dy.cdf")
sss_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss_model_12n90e.nc")
sss_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sss/sss_model_12n90e.nc")

plt.figure(2)
sss_obs["S_41"].plot(label="Obs", linewidth=3)
sss_m1["SSS"].plot(label="ERA", linestyle="dashed")
sss_m3["SSS"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sss_12n90e.png")


# 15 N 90 E
sss_obs = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss15n90e_dy.cdf")
sss_m1 = xr.open_dataset("~/HDD2/runs/run1/RAMA/sss/sss_model_15n90e.nc")
sss_m3 = xr.open_dataset("~/HDD2/runs/run3/RAMA/sss/sss_model_15n90e.nc")

plt.figure(3)
sss_obs["S_41"].plot(label="Obs", linewidth=3)
sss_m1["SSS"].plot(label="ERA", linestyle="dashed")
sss_m3["SSS"].plot(label="TRMM_ASCAT", linestyle="dashed")
plt.legend()
plt.savefig("sss_15n90e.png")
