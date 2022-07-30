import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz as gv

# open files
sss_obs_file = xr.open_dataset("~/HDD2/runs/run1/SSS/sd_obs.nc")
sss_run_file = xr.open_dataset("~/HDD2/runs/run1/SSS/sd1.nc")

sss_run_2 = xr.open_dataset("~/HDD2/runs/run2/SSS/sd2.nc")
sss_run_3 = xr.open_dataset("~/HDD2/runs/run3/SSS/sd3.nc")


def main_plot(ti):
    # data
    sss_obs = sss_obs_file["sd"]
    sss_run = sss_run_file["sd"]
    sss_run2 = sss_run_2["sd"]
    sss_run3 = sss_run_3["sd"]

    # select time 
    sss_obs = sss_obs.isel(TIME=ti)
    sss_run = sss_run.isel(time=ti)
    sss_run2 = sss_run2.isel(time=ti)
    sss_run3 = sss_run3.isel(time=ti)
    
    # Plotting
    fig = plt.figure(figsize=(14, 14))
    
    grid = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)
    
    # Choose the map projection
    proj = ccrs.PlateCarree()
    
    t1 = sss_run.time.values
    
    # Add the subplots
    ax1 = fig.add_subplot(grid[0, 0], projection=proj)  # upper cell of grid
    ax2 = fig.add_subplot(grid[0, 1], projection=proj)  # middle cell of grid
    ax3 = fig.add_subplot(grid[1, 0], projection=proj)  # upper cell of grid
    ax4 = fig.add_subplot(grid[1, 1], projection=proj)  # middle cell of grid
    ax5 = fig.add_subplot(grid[2, 0], projection=proj)  # upper cell of grid
    ax6 = fig.add_subplot(grid[2, 1], projection=proj)  # middle cell of grid

    for (ax, title) in [(ax1, t1), (ax2, t1), (ax3, t1), (ax4, t1), (ax5, t1), (ax6, t1)]:
        # Use geocat.viz.util convenience function to set axes tick values
        gv.set_axes_limits_and_ticks(ax=ax,
                                     xlim=(77, 99),
                                     ylim=(4, 25),
                                     xticks=np.linspace(77, 99, 5),
                                     yticks=np.linspace(4, 25, 4))
    
        # Use geocat.viz.util convenience function to make plots look like NCL
        # plots by using latitude, longitude tick labels
        gv.add_lat_lon_ticklabels(ax)
    
        # Remove the degree symbol from tick labels
        ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
        ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    
        # Use geocat.viz.util convenience function to add minor and major ticks
        gv.add_major_minor_ticks(ax)
    
        # Draw coastlines
        ax.coastlines(linewidth=0.5)
    
        # Use geocat.viz.util convenience function to set titles
        gv.set_titles_and_labels(ax,
                                 lefttitle="sss",
                                 righttitle="std_dev",
                                 lefttitlefontsize=10,
                                 righttitlefontsize=10)
        # Add center title
    ax1.set_title("Obs", loc='center', y=1.04, fontsize=10)
    ax2.set_title("Model_ERA", loc='center', y=1.04, fontsize=10)
    ax3.set_title("Obs", loc='center', y=1.04, fontsize=10)
    ax4.set_title("Model_TRMM", loc='center', y=1.04, fontsize=10)
    ax5.set_title("Obs", loc='center', y=1.04, fontsize=10)
    ax6.set_title("Model_TRMM_ASCAT", loc='center', y=1.04, fontsize=10)
    
    # Select an appropriate colormap
    cmap = 'Spectral_r'
    
    # limits
    tmin = 0 #min(sss_run.min(), sss_obs.min())
    tmax = 3 #max(sss_run.max(), sss_obs.max())
    bounds = np.arange(tmin,tmax,0.25)
    # Plot data
    C = ax1.contourf(sss_obs['xh'],
                     sss_obs['yh'],
                     sss_obs,
                     levels=np.arange(tmin, tmax, 0.25),
                     cmap=cmap,
                     extend='both')
    ax2.contourf(sss_run['xh'],
                 sss_run['yh'],
                 sss_run,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    ax3.contourf(sss_obs['xh'],
                 sss_obs['yh'],
                 sss_obs,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    ax4.contourf(sss_run2['xh'],
                 sss_run2['yh'],
                 sss_run2,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    ax5.contourf(sss_obs['xh'],
                 sss_obs['yh'],
                 sss_obs,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    ax6.contourf(sss_run3['xh'],
                 sss_run3['yh'],
                 sss_run3,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    
    # Add colorbars
    # By specifying two axes for `ax` the colorbar will span both of them
    plt.colorbar(C,
                 ax=[ax1, ax2],
                 boundaries=bounds,
                 extendrect=True,
                 extendfrac='auto',
                 shrink=0.95,
                 aspect=13,
                 orientation='horizontal',
                 drawedges=True)
    
    plt.savefig("salt_sd_%i.png" %ti)


for i in range(1):
    main_plot(i)
