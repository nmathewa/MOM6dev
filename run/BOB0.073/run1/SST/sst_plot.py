import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz as gv

# open files
sst_obs_file = xr.open_dataset("~/HDD2/runs/run1/SST/sst_obs.nc")
sst_run_file = xr.open_dataset("~/HDD2/runs/run1/SST/sst_model.nc")



def main_plot(ti):
    # data
    sst_obs = sst_obs_file["sst"]
    sst_run = sst_run_file["SST"]

    # select time 
    sst_obs = sst_obs.isel(time=ti)
    sst_run = sst_run.isel(time=ti)
    diff = sst_obs - sst_run
    
    # Plotting
    fig = plt.figure(figsize=(10, 10))
    
    grid = gridspec.GridSpec(nrows=1, ncols=3, figure=fig)
    
    # Choose the map projection
    proj = ccrs.PlateCarree()
    
    t1 = sst_run.time.values
    
    # Add the subplots
    ax1 = fig.add_subplot(grid[0], projection=proj)  # upper cell of grid
    ax2 = fig.add_subplot(grid[1], projection=proj)  # middle cell of grid
    ax3 = fig.add_subplot(grid[2], projection=proj)  # lower cell of grid
    
    for (ax, title) in [(ax1, t1), (ax2, t1), (ax3, t1)]:
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
                                 lefttitle="SST",
                                 righttitle=sst_obs.units,
                                 lefttitlefontsize=10,
                                 righttitlefontsize=10)
        # Add center title
        ax.set_title(title, loc='center', y=1.04, fontsize=10)
    
    ax2.set_title("Model", loc='center', y=1.04, fontsize=10)
    ax3.set_title("Obs - Model", loc='center', y=1.04, fontsize=10)
    
    # Select an appropriate colormap
    cmap = 'Spectral_r'
    
    # limits
    tmin = 24 #min(sst_run.min(), sst_obs.min())
    tmax = 31 #max(sst_run.max(), sst_obs.max())
    
    # Plot data
    C = ax1.contourf(sst_obs['xh'],
                     sst_obs['yh'],
                     sst_obs,
                     levels=np.arange(tmin, tmax, 0.25),
                     cmap=cmap,
                     extend='both')
    ax2.contourf(sst_run['xh'],
                 sst_run['yh'],
                 sst_run,
                 levels=np.arange(tmin, tmax, .25),
                 cmap=cmap,
                 extend='both')
    C_2 = ax3.contourf(diff['xh'],
                       diff['yh'],
                       diff,
                       levels=np.arange(-5, 5, 1),
                       cmap="RdBu_r",
                       extend='both')
    
    # Add colorbars
    # By specifying two axes for `ax` the colorbar will span both of them
    plt.colorbar(C,
                 ax=[ax1, ax2],
                 ticks=np.arange(tmin, tmax, 1.5),
                 extendrect=True,
                 extendfrac='auto',
                 shrink=0.95,
                 aspect=13,
                 orientation='horizontal',
                 drawedges=True)

    er_bounds = np.arange(-5,5,1)
    plt.colorbar(C_2,
                 ax=ax3,
                 boundaries=er_bounds,
                 extendrect=True,
                 extendfrac='auto',
                 shrink=0.95,
                 aspect=5.5,
                 orientation='horizontal',
                 drawedges=True)
    
    plt.savefig("temp_%i.png" %ti)


for i in range(24):
    main_plot(i)
