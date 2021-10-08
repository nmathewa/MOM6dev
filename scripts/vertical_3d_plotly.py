#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:44:04 2021
plotly 3d multiple surface
@author: nma
"""
import plotly.graph_objects as go
import numpy as np
import xarray as xr
import os

os.chdir("/home/nma/momdev/exps/caops/")
ocns = xr.open_mfdataset("ocns*.nc",use_cftime=True)


lons,lats,zz = ocns.xq[:-1],ocns.yq[:-1],ocns.zl
lon2d, lat2d = np.meshgrid(lons, lats)

salin1 = ocns.salt.isel(zl=0,Time=0).values

salin2 = ocns.salt.isel(zl=1,Time=0).values

salin3 = ocns.salt.isel(zl=2,Time=0).values

salin4 = ocns.salt.isel(zl=3,Time=0).values

salin5 = ocns.salt.isel(zl=4,Time=0).values

salin6 = ocns.salt.isel(zl=5,Time=0).values


z_new = ocns.zl.values[:6]

zz1 = np.ones(shape=np.shape(salin1))*(-1*(z_new[0]))
zz2 = np.ones(shape=np.shape(salin1))*(-1*(z_new[1]))
zz3 = np.ones(shape=np.shape(salin1))*(-1*(z_new[2]))
zz4 = np.ones(shape=np.shape(salin1))*(-1*(z_new[3]))
zz5 = np.ones(shape=np.shape(salin1))*(-1*(z_new[4]))
zz6 = np.ones(shape=np.shape(salin1))*(-1*(z_new[5]))

#%%
max_v = np.nanmax(salin1)
min_v = np.nanmin(salin1)


contour1 = go.Contour(x= lons,y = lats,z = salin1)

fig = go.Figure(data=[
    go.Surface(x=lons,y=lats,z=zz1,surfacecolor=salin1,hovertext=salin1,name="Level 1",colorscale="Jet"),
    go.Surface(x=lons,y=lats, z=zz2,surfacecolor=salin2,hovertext=salin2,name="Level 2" ,colorscale="Jet"),
    go.Surface(x=lons,y=lats, z=zz3,surfacecolor=salin2,hovertext=salin3 ,name="Level 3",colorscale="Jet"),
    go.Surface(x=lons,y=lats, z=zz4,surfacecolor=salin2,hovertext=salin4 ,name="Level 4",colorscale="Jet"),
    go.Surface(x=lons,y=lats, z=zz5,surfacecolor=salin2,hovertext=salin5 ,name="Level 5",colorscale="Jet"),
    go.Surface(x=lons,y=lats, z=zz6,surfacecolor=salin2,hovertext=salin6 ,name="Level 6",colorscale="Jet"),

],layout=go.Layout(
        title=go.layout.Title(text="Salinity 2D vertical profile (6 levels)")
    ))
    
fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
fig.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="green"
)

fig.write_html("docs/outtest.html")

