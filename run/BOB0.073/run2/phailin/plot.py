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
    sst_file = xr.open_dataset("~/HDD2/runs/run2/phailin/oct13.nc")
    sss_file = xr.open_dataset("~/HDD2/runs/run2/phailin/oct13.nc")
    speed_file = xr.open_dataset("~/HDD2/runs/run2/phailin/speed.nc")
    
    # data
    wind_u = wind_file["u10"]
    wind_v = wind_file["v10"]
    wind_file["speed"] = np.sqrt(wind_u*wind_u + wind_v*wind_v)
    

    rain = rain_file["precipitation"].isel(time=ti)
    sst = sst_file["SST"].isel(time=ti)
    sss = sss_file["SSS"].isel(time=ti)
    ssu = speed_file["SSU"].isel(time=ti)
    ssv = speed_file["SSV"].isel(time=ti)
    speed_file["speed"] = np.sqrt(ssu*ssu + ssv*ssv)

    wind_speed = wind_file["speed"].isel(time=ti)
    speed = speed_file["speed"]

    # Plotting
    fig = plt.figure(figsize=(20, 16))
    
    grid = gridspec.GridSpec(nrows=2, ncols=3, figure=fig, hspace=-0.25)
    
    # Choose the map projection
    proj = ccrs.PlateCarree()
    
    t1 = sst.time.values
    
    # Add the subplots
    ax1 = fig.add_subplot(grid[0, 0], projection=proj)  # upper cell of grid
    ax2 = fig.add_subplot(grid[0, 1], projection=proj)  # middle cell of grid
    ax4 = fig.add_subplot(grid[1, 0], projection=proj)  # upper cell of grid
    ax5 = fig.add_subplot(grid[1, 1], projection=proj)  # middle cell of grid
    ax6 = fig.add_subplot(grid[1, 2], projection=proj)  # lower cell of grid

    for (ax, title) in [(ax1, t1), (ax2, t1), (ax4, t1), (ax5, t1), (ax6, t1)]:
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
        
        gv.set_titles_and_labels(ax4,
                                 lefttitle="SST",
                                 righttitle="deg C",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        gv.set_titles_and_labels(ax5,
                                 lefttitle="SSS",
                                 righttitle="psu",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)
        
        gv.set_titles_and_labels(ax6,
                                 lefttitle="currents",
                                 righttitle="m/s",
                                 lefttitlefontsize=14,
                                 righttitlefontsize=14)

        # Add center title
        ax.set_title(title, loc='center', y=1.04, fontsize=14)
    
    
    """ax2.set_title("Rainfall", loc='center', y=1.04, fontsize=14)
    ax4.set_title("SST", loc='center', y=1.04, fontsize=14)
    ax5.set_title("SSS", loc='center', y=1.04, fontsize=14)
    ax6.set_title("Currents", loc='center', y=1.04, fontsize=14)"""

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
    C2 = ax4.contourf(sst['xh'],
                    sst['yh'],
                    sst,
                    levels=np.linspace(27, 29, 100),
                    cmap=cmap,
                    extend='both')
    C3 = ax5.contourf(sss['xh'],
                    sss['yh'],
                    sss,
                    levels=np.linspace(32, 34, 100),
                    cmap=cmap,
                    extend='both')
    C4 = ax6.contourf(speed['xh'],
                    speed['yh'],
                    speed,
                    levels=np.linspace(speed.min(), speed.max(), 100),
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
                ax=ax4,
                boundaries=np.linspace(27, 29,5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    plt.colorbar(C3,
                ax=ax5,
                boundaries=np.linspace(32, 34,5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    
    plt.colorbar(C4,
                ax=ax6,
                boundaries=np.linspace(speed.min(),speed.max(),5),
                extendrect=True,
                extendfrac='auto',
                shrink=0.525,
                aspect=13,
                orientation='vertical',
                pad=0.0,
                drawedges=True)
    
    plt.suptitle("Different plots", size=28)
    plt.savefig("plot_%i.png" %ti)

for i in range(20):
    main_plot(i)
