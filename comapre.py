# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 01:59:15 2022

@author: baoxi
"""

import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker
import cartopy.io.shapereader as shapereader
import matplotlib.pyplot as plt
import cmaps


# 绘图函数
def contour_map(fig,img_extent):
    lon_W,lon_E,lat_S,lat_N = img_extent
    fig.set_extent(img_extent, crs=ccrs.PlateCarree())
    fig.set_xticks(np.arange(lon_W,lon_E+2,2), crs=ccrs.PlateCarree())
    fig.set_yticks(np.arange(lat_S,lat_N+2,2), crs=ccrs.PlateCarree())
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    fig.xaxis.set_major_formatter(lon_formatter)
    fig.yaxis.set_major_formatter(lat_formatter)
    China_map = shapereader.Reader("D:/TROPOMIchina/cnshapefile/china.shp").geometries()
    fig.add_geometries(China_map, ccrs.PlateCarree(),facecolor='none', edgecolor='black',zorder = 1,lw=0.7)
    
main_dir = "D:/TROPOMIchina/compare/"

f = xr.open_dataset(main_dir + '2019-01-NO2.nc')
DIF = f['DIF'][:,:]
lat = f['lat'][:]
lon = f['lon'][:]
latS = 27.5
latN = 35
lonW = 115
lonE = 122


plt.figure(figsize=(8,6))
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
contour_map(ax,[lonW,lonE,latS,latN])
ax.set_ylim(lat[:].values.min(),lat[:].values.max())
ax.set_xlim(lon[:].values.min(),lon[:].values.max())
c=ax.pcolormesh(lon[:],lat[:],DIF,vmin=-15,vmax=15,cmap=cmaps.WhiteBlueGreenYellowRed,transform=ccrs.PlateCarree())
#BlAqGrYeOrReVi200
cb=plt.colorbar(c)
plt.savefig("D:/桌面/yrd_ei_2017/COMPARE/"+"compare1.png")