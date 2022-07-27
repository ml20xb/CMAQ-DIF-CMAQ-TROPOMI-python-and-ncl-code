# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 14:01:18 2022

@author: baoxinbin
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
    

main_dir = "D:/TROPOMIchina/YRD/"

ff = xr.open_dataset(main_dir+'GRIDCRO2D_2018365.nc')

lat = ff['LAT'][0,0,:,:]
lon = ff['LON'][0,0,:,:]
print(lat.shape)
print(len(lat))
names = ['2019031.NO2.ncf','2019031.NO2.ncf','2019033.NO2.ncf','2019034.NO2.ncf',
         '2019035.NO2.ncf','2019036.NO2.ncf','2019037.NO2.ncf','2019038.NO2.ncf','2019039.NO2.ncf','2019040.NO2.ncf'
         ,'2019041.NO2.ncf','2019042.NO2.ncf','2019043.NO2.ncf','2019044.NO2.ncf','2019045.NO2.ncf','2019046.NO2.ncf'
         ,'2019047.NO2.ncf','2019048.NO2.ncf','2019049.NO2.ncf','2019050.NO2.ncf','2019051.NO2.ncf','2019052.NO2.ncf'
         ,'2019053.NO2.ncf','2019054.NO2.ncf','2019055.NO2.ncf','2019056.NO2.ncf','2019057.NO2.ncf','2019058.NO2.ncf'
         ,'2019059.NO2.ncf']
for n in range(len(names)):
    name = names[n]
    f = xr.open_dataset(main_dir + name)
    NO2 = f['NO2_COLUMN'][5,0,:,:]
    if n==0:
        NO2_sum = NO2
    else:
        NO2_sum = NO2_sum + NO2

NO2_sum = NO2_sum / len(names)
latS = 27
latN = 35
lonW = 115
lonE = 123

plt.figure(figsize=(8,6))
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
contour_map(ax,[lonW,lonE,latS,latN])
ax.set_ylim(lat[:,0].values.min(),lat[:,0].values.max())
ax.set_xlim(lon[0,:].values.min(),lon[0,:].values.max())
c=ax.pcolormesh(lon[0,:],lat[:,0],NO2_sum,vmin=0,vmax=12,cmap=cmaps.WhiteBlueGreenYellowRed,transform=ccrs.PlateCarree())
#BlAqGrYeOrReVi200
cb=plt.colorbar(c)
plt.savefig("D:/桌面/yrd_ei_2017/WRF-CMAQ/"+"out1.png")