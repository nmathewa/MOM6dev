import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz as gv



def main_plot(ti):
    # open files
    wind_file = xr.open_dataset("~/HDD2/runs/run2/phailin/wind_speed.nc")
    rain_file = xr.open_dataset("~/HDD2/runs/run2/phailin/rain.nc")
    mld_file = xr.open_dataset("~/HDD2/runs/run2/phailin/mld_d20.nc")
    d20_file = xr.open_dataset("~/HDD2/runs/run2/phailin/d20.nc")
    
    # data
    wind_u = wind_file["u10"]
    wind_v = wind_file["v10"]
    wind_file["speed"] = np.sqrt(wind_u*wind_u + wind_v*wind_v)
    

    rain = rain_file["precipitation"].isel(time=ti)
    mld = mld_file["MLD_003"].isel(time=ti)
    d20 = d20_file["D"].isel(TIME=ti)
    wind_speed = wind_file["speed"].isel(time=ti)

    # Plotting
    fig = plt.figure(figsize=(16, 16))
    
    grid = gridspec.GridSpec(nrows=2, ncols=2, figure=fig)
    
    # Choose the map projection
    proj = ccrs.PlateCarree()
    
    t1 = mld.time.values
    
    # Add the subplots
    ax1 = fig.add_subplot(grid[0, 0], projection=proj)  # upper cell of grid
    ax2 = fig.add_subplot(grid[0, 1], projection=proj)  # middle cell of grid
    ax3 = fig.add_subplot(grid[1, 0], projection=proj)  # upper cell of grid
    ax4 = fig.add_subplot(grid[1, 1], projection=proj)  # middle cell of grid

    for (ax, title) in [(ax1, t1), (ax2, t1), (ax3, t1), (ax4, t1)]:
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
        gv.set_titles_and_labels(ax1,
                                 lefttitle="wind",
                                 righttitle="m/s",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        gv.set_titles_and_labels(ax2,
                                 lefttitle="rainfall",
                                 righttitle="kgm-2s-1",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        gv.set_titles_and_labels(ax3,
                                 lefttitle="MLD_003",
                                 righttitle="m",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        gv.set_titles_and_labels(ax4,
                                 lefttitle="D20",
                                 righttitle="m",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        # Add center title
        ax.set_title(title, loc='center', y=1.04, fontsize=14)

    # Select an appropriate colormap
    cmap = 'Spectral_r'
    
    # limits
    # Plot data
    C = ax1.contourf(wind_speed["longitude"],
                    wind_speed["latitude"],
                    wind_speed,
                    levels=np.linspace(wind_speed.min(), wind_speed.max(), 100),
                    cmap="jet",
                    extend='both')
    C1 = ax2.contourf(rain['lon'],
                    rain['lat'],
                    rain,
                    levels=np.linspace(rain.min(), rain.max(), 100),
                    cmap=cmap,
                    extend='both')
    C2 = ax3.contourf(mld['xh'],
                    mld['yh'],
                    mld,
                    levels=np.linspace(5, 85, 100),
                    cmap=cmap,
                    extend='both')
    C3 = ax4.contourf(d20['xh'],
                    d20['yh'],
                    d20,
                    levels=np.linspace(15,19,100),
                    cmap=cmap,
                    extend='both')

    # Add colorbars
    # By specifying two axes for `ax` the colorbar will span both of them
    plt.colorbar(C,
                ax=ax1,
                boundaries=np.linspace(wind_speed.min(), wind_speed.max(),5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    plt.colorbar(C1,
                ax=ax2,
                boundaries=np.linspace(rain.min(), rain.max(),5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    plt.colorbar(C2,
                ax=ax3,
                boundaries=np.linspace(5, 85,5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    plt.colorbar(C3,
                ax=ax4,
                boundaries=np.linspace(15,19,5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.7,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    
    plt.suptitle("Different plots", size=28)
    plt.savefig("mld_%i.png" %ti)

for i in range(20):
    main_plot(i)
