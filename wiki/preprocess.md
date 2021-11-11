
# Input data processing (Pre-processing)

## Example datasets 

```BASH 
lftp ftp://ftp.gfdl.noaa.gov/perm/Alistair.Adcroft/MOM6-testing

```
using "mget" we can download the data

## Grid creation

### 1. GRID creation

```BASH
make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd 77,99 --ybnd 4,23 --nlon 524 --nlat 384 --verbose'
```
### 2.mosaic creation

```BASH
make_solo_mosaic --num_tiles 1 --dir . --mosaic_name ocean_mosaic_india --tile_file mosaic.nc --periodx 0 --periody 0
```


### 3. Topog creation

- Bathymetry is from ETOPO v2 


```BASH
make_topog --mosaic ocean_mosaic_india.nc --topog_type realistic --topog_file gebco_test.nc --topog_field depth --scale_factor 1
```

## Initial conditions

- [ECMWRF ERA5 reanlysis](https://www.ecmwf.int/en/research/climate-reanalysis/ocean-reanalysis)

- [HYCOM]()

## Forcing Conditions 

### OLR flux 

- 2015 daily dataset 
- watt/m^2
- [data download](https://www.ncei.noaa.gov/products/climate-data-records/outgoing-longwave-radiation-daily)
- [NCAR air-sea flux data](https://rda.ucar.edu/datasets/ds260.2/)