import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
import numpy as np
import xarray as xr
import cmaps

import geocat.datafiles as gdf
import geocat.viz as gv
import cmocean



def plotting(ti):
    # Open a netCDF data file using xarray default engine and load the data into xarrays
    ds = xr.open_dataset("~/HDD2/runs/run1/speed/speed_obs.nc")
    r1 = xr.open_dataset("~/HDD2/runs/run1/speed/speed_model.nc")
    r2 = xr.open_dataset("~/HDD2/runs/run2/speed/speed_model.nc")
    r3 = xr.open_dataset("~/HDD2/runs/run3/speed/speed_model.nc")


    # Extract data from timestep
    ds = ds.isel(time=ti)
    r1 = r1.isel(time=ti)
    r2 = r2.isel(time=ti)
    r3 = r3.isel(time=ti)

    # Ensure longitudes range from 0 to 360 degrees
    U = ds.u
    V = ds.v

    u1 = r1.SSU
    v1 = r1.SSV

    u2 = r2.SSU
    v2 = r2.SSV

    u3 = r3.SSU
    v3 = r3.SSV

    # Splice data to only include every nth value
    U = U[::8, ::8]
    V = V[::8, ::8]

    u1 = u1[::8, ::8]
    v1 = v1[::8, ::8]

    u2 = u2[::8, ::8]
    v2 = v2[::8, ::8]

    u3 = u3[::8, ::8]
    v3 = v3[::8, ::8]

    # Calculate the magnitude of the winds
    magnitude = np.sqrt(U*U + V*V)
    m1 = np.sqrt(u1*u1 + v1*v1)
    m2 = np.sqrt(u2*u2 + v2*v2)
    m3 = np.sqrt(u3*u3 + v3*v3)

    # Create subplots and specify their projections
    projection = ccrs.PlateCarree()
    fig, axs = plt.subplots(3, 2, figsize=(13, 19), subplot_kw={"projection": projection})
    #plt.tight_layout()

    # Add coastlines, the zorder keyword specifies the order in which the elements
    # are drawn where elements with lower zorder values are drawn first
    axs[0, 0].coastlines(linewidth=0.5, zorder=1)
    axs[0, 1].coastlines(linewidth=0.5, zorder=1)
    axs[1, 0].coastlines(linewidth=0.5, zorder=1)
    axs[1, 1].coastlines(linewidth=0.5, zorder=1)
    axs[2, 0].coastlines(linewidth=0.5, zorder=1)
    axs[2, 1].coastlines(linewidth=0.5, zorder=1)

    axs[0, 0].set_facecolor("0.75")
    axs[0, 1].set_facecolor("0.75")
    axs[1, 0].set_facecolor("0.75")
    axs[1, 1].set_facecolor("0.75")
    axs[2, 0].set_facecolor("0.75")
    axs[2, 1].set_facecolor("0.75")

    # Use geocat.viz.util convenience function to set axes tick values
    gv.set_axes_limits_and_ticks(axs[0, 0],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))
    gv.set_axes_limits_and_ticks(axs[0 ,1],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))
    gv.set_axes_limits_and_ticks(axs[1, 0],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))
    gv.set_axes_limits_and_ticks(axs[1 ,1],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))
    gv.set_axes_limits_and_ticks(axs[2, 0],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))
    gv.set_axes_limits_and_ticks(axs[2 ,1],
                                xlim=[77, 99],
                                ylim=[4, 25],
                                xticks=np.linspace(77, 99, 5),
                                yticks=np.linspace(4, 25, 5))

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gv.add_major_minor_ticks(axs[0, 0])
    gv.add_major_minor_ticks(axs[0, 1])
    gv.add_major_minor_ticks(axs[1, 0])
    gv.add_major_minor_ticks(axs[1, 1])
    gv.add_major_minor_ticks(axs[2, 0])
    gv.add_major_minor_ticks(axs[2, 1])

    # Use geocat.viz.util convenience function to make plots look like NCL plots by
    # using latitude, longitude tick labels
    gv.add_lat_lon_ticklabels(axs[0, 0])
    gv.add_lat_lon_ticklabels(axs[0, 1])
    gv.add_lat_lon_ticklabels(axs[1, 0])
    gv.add_lat_lon_ticklabels(axs[1, 1])
    gv.add_lat_lon_ticklabels(axs[2, 0])
    gv.add_lat_lon_ticklabels(axs[2, 1])

    # Remove the degree symbol from tick labels
    axs[0, 0].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[0, 0].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    axs[0, 1].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[0, 1].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    axs[1, 0].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[1, 0].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    axs[1, 1].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[1, 1].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    axs[2, 0].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[2, 0].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    axs[2, 1].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    axs[2, 1].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

    # Use geocat.viz.util convenience function to set titles and labels
    gv.set_titles_and_labels(axs[0, 0],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)
    gv.set_titles_and_labels(axs[0, 1],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)
    gv.set_titles_and_labels(axs[1, 0],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)
    gv.set_titles_and_labels(axs[1, 1],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)
    gv.set_titles_and_labels(axs[2, 0],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)
    gv.set_titles_and_labels(axs[2, 1],
                            lefttitle='Speed',
                            lefttitlefontsize=10,
                            righttitle=U.units,
                            righttitlefontsize=10)

    axs[0, 0].set_title(u1.time.values, loc='center', y=1.04, fontsize=10)
    axs[0, 1].set_title("Model_ERA", loc='center', y=1.04, fontsize=10)
    axs[1, 0].set_title(u1.time.values, loc='center', y=1.04, fontsize=10)
    axs[1, 1].set_title("Model_TRMM", loc='center', y=1.04, fontsize=10)
    axs[2, 0].set_title(u1.time.values, loc='center', y=1.04, fontsize=10)
    axs[2, 1].set_title("Model_TRMM_ASCAT", loc='center', y=1.04, fontsize=10)

    # Load in colormap
    newcmap = cmocean.cm.tempo

    # Specify contour levels and contour ticks
    smin = min(magnitude.min(), m1.min(), m2.min(), m3.min())
    smax = max(magnitude.max(), m1.max(), m2.max(), m3.max())

    speed_levels = np.linspace(smin, smax, 60)
    speed_ticks = np.linspace(smin, smax, 8)

    # Plot filled contours
    speed = axs[0, 0].contourf(U['xq'],
                            U['yh'],
                            magnitude,
                            levels=speed_levels,
                            cmap=newcmap,
                            zorder=0)
    axs[0, 1].contourf(u1['xq'],
                        u1['yh'],
                        m1,
                        levels=speed_levels,
                        cmap=newcmap,
                        zorder=0)
    axs[1, 0].contourf(U['xq'],
                            U['yh'],
                            magnitude,
                            levels=speed_levels,
                            cmap=newcmap,
                            zorder=0)
    axs[1, 1].contourf(u2['xq'],
                        u2['yh'],
                        m2,
                        levels=speed_levels,
                        cmap=newcmap,
                        zorder=0)
    axs[2, 0].contourf(U['xq'],
                            U['yh'],
                            magnitude,
                            levels=speed_levels,
                            cmap=newcmap,
                            zorder=0)
    axs[2, 1].contourf(u3['xq'],
                        u3['yh'],
                        m3,
                        levels=speed_levels,
                        cmap=newcmap,
                        zorder=0)

    # Create color bars
    speed_cbar = plt.colorbar(speed,
                            ax=[axs[0, 0],axs[0, 1], axs[1, 0], axs[1, 1], axs[2, 0], axs[2, 1]], 
                            orientation='horizontal',
                            ticks=speed_ticks,
                            shrink=0.7,
                            drawedges=True,
                            pad=0.1)

    # Remove trailing zeros from speed color bar tick labels
    speed_cbar.ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))

    # Plotting vector field
    quiver_speed = axs[0, 0].quiver(U['xq'],
                                U['yh'],
                                U.data,
                                V.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    axs[0, 1].quiver(u1['xq'],
                                u1['yh'],
                                u1.data,
                                v1.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    axs[1, 0].quiver(U['xq'],
                                U['yh'],
                                U.data,
                                V.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    axs[1, 1].quiver(u2['xq'],
                                u2['yh'],
                                u2.data,
                                v2.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    axs[2, 0].quiver(U['xq'],
                                U['yh'],
                                U.data,
                                V.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    axs[2, 1].quiver(u3['xq'],
                                u3['yh'],
                                u3.data,
                                v3.data,
                                scale=7.5,
                                width=0.002,
                                headwidth=6,
                                headlength=7,
                                zorder=2)
    # Add reference vector and label
    axs[0, 0].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)
    axs[0, 1].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)
    axs[1, 0].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)
    axs[1, 1].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)
    axs[2, 0].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)
    axs[2, 1].quiverkey(quiver_speed, 0.8875, 0.8875, 0.25, 0.5, zorder=2)

    plt.savefig("speed_%d.png"%ti)

for i in range(24):
    plotting(i)
