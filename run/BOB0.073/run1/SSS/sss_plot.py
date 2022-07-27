import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz as gv

# open files
sss_obs_file = xr.open_dataset("~/HDD2/runs/run1/SSS/sss_obs.nc")
sss_run_file = xr.open_dataset("~/HDD2/runs/run1/SSS/sss_model.nc")



def main_plot(ti):
    # data
    sss_obs = sss_obs_file["SSS"]
    sss_run = sss_run_file["SSS"]

    # select time 
    sss_obs = sss_obs.isel(TIME=ti)
    sss_run = sss_run.isel(time=ti)
    diff = sss_obs - sss_run
    
    # Plotting
    fig = plt.figure(figsize=(10, 10))
    
    grid = gridspec.GridSpec(nrows=1, ncols=3, figure=fig)
    
    # Choose the map projection
    proj = ccrs.PlateCarree()
    
    t1 = sss_run.time.values
    
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
                                 lefttitle="sss",
                                 righttitle="psu",
                                 lefttitlefontsize=10,
                                 righttitlefontsize=10)
        # Add center title
        ax.set_title(title, loc='center', y=1.04, fontsize=10)
    ax2.set_title("Model", loc='center', y=1.04, fontsize=10)
    ax3.set_title("Obs - Model", loc='center', y=1.04, fontsize=10)
    # Select an appropriate colormap
    cmap = 'Spectral_r'
    
    # limits
    tmin = 28 #min(sss_run.min(), sss_obs.min())
    tmax = 37 #max(sss_run.max(), sss_obs.max())
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
                 boundaries=bounds,
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
    
    plt.savefig("salt_%i.png" %ti)


for i in range(24):
    main_plot(i)
