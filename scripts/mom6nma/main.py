"""
test package to set up the input datasets for MOM6 ocean model
"""


import os
from grid_create import create_lat_lon_regular

os.chdir("/home/mathew/hdd/UBU20/hdd/IISC_PA/Tools/mom6nma/")

x1lon = 88
x2lon = 92
y1lat = 16
y2lat = 19

xres = 721
yres = 421

x,y,area,dx,dy,angle = create_lat_lon_regular(x1lon, x2lon, y1lat, y2lat, xres, yres)


print("grid elements created")
