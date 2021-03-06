
# Input data processing (Pre-processing)

## Example datasets 

```BASH 
lftp ftp://ftp.gfdl.noaa.gov/perm/Alistair.Adcroft/MOM6-testing

```
using "mget" we can download the data

- some missing datasets are downloaded from [this link](https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/ocn/mom/tx0.25v1/)

## Grid creation

### 1. GRID creation

```BASH
make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd 77,99 --ybnd 4,23 --nlon 524 --nlat 384 --verbose'
```
### 2.mosaic creation

```BASH
make_solo_mosaic --num_tiles 1 --dir . --mosaic_name bob_mos --tile_file mom_grid.nc --periodx 0 --periody 0
```

### 3. Topog creation

- Bathymetry is from ETOPO v2 


```BASH
make_topog --mosaic ocean_mosaic.nc --topog_type realistic --topog_file gebco_test.nc --topog_field depth --scale_factor 1
```

For running the atmospheric, land and ice modulues (for forcing not coupled), the atmospheric and land coupled grids should be generated 

- for creating all domain files 

```BASH
make_quick_mosaic --input_mosaic ocean_mosaic.nc --mosaic_name grid_spec --ocean_topog topog.nc

```
- Then the below files will be generated



## Initial conditions

- [ECMWRF ERA5 reanlysis](https://www.ecmwf.int/en/research/climate-reanalysis/ocean-reanalysis)

- [HYCOM]()

# Forcing Conditions 

- [ERA5 reanalysis](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview)

For the forcing should work atmospheric and land components should be compiled (recommended option is build with Sea Ice (SIS2))

## prerequesties

- Date calendar must be set ("NOLEAP" is used so far)

- There must be no null/nan values, must be interpolated (interpolate nan) for all time steps (rioxarray is used, refer to momtools)
- Units of variables should match with MOM6 requirement (refer next section tree "Variables_info")
- Data Table variable names,file names must be match with file names
- variable nc domains must be larger than the grid extends

## Pre processing a raw ERA5 file

- The ERA5 forcing data file needs to be processed before they can be input to MOM6
- Suppose we have a temperature file of given domain of given time resolution(suppose temp.nc of BOB of 1 hour resolution). We use "cdo" and "nco".

1.) Convert to double/float the variables:
```
cdo -b 64 copy temp.nc o.nc
```

2.) If the time variable is not converted to float/double:
```
ncap2 -s 'time = float(time)' temp.nc o.nc 
```

3.) Creating the time axis
```
cdo -r -f nc settaxis,2012-01-01,00:00:00,1hour temp.nc o.nc
```
format is : 'cdo -r -f nc settaxis,start-date,start-time,frequency infile.nc outfile.nc'
frequency can be 1hour,1day,1month

4.) Delete the leap day if required
```
cdo delete,month=2,day=29 temp.nc o.nc 
```

5.) Change the attribute of time variable
```
ncatted -O -a calendar,time,o,c,NOLEAP temp.nc o.nc 
```

6.) Remap to a particular grid 
```
cdo remapycon,other_grid.nc infile.nc outfile.nc
```
other_grid.nc is the grid which we want for infile.nc 

## Variable Table

| Variable name | data_table id | units | type | forcing type |
| --------------|---------------|-------|------|--------------|
Salinity (S) |  -- | PSU | IC | 
| water Temperature | | Degree C |
| hori and meri components | | |
Sea level pressure | p_surf,p_bot | Pa | forcing |"ATM"
| Air Temperature | t_bot | Kelvin | forcing| "ATM"  
| 
### Data Table

![](Screenshot%20from%202021-11-15%2014-17-47.png)

data table should set up accordingly (with forcing datasets)

# Open boundary conditions

## Simple 




### OLR flux 

- 2015 daily dataset 
- watt/m^2
- [data download](https://www.ncei.noaa.gov/products/climate-data-records/outgoing-longwave-radiation-daily)
- [NCAR air-sea flux data](https://rda.ucar.edu/datasets/ds260.2/)


# References

1. [Boundary condition pynotes](https://github.com/ESMG/regionalMOM6_notebooks/blob/master/creating_obc_input_files/panArctic_OBC_from_global_MOM6.ipynb)
2. [ocean model grid genreator tool](https://github.com/nikizadehgfdl/ocean_model_grid_generator)
3. [COSIMA pan antarctic MOM6 model configs](https://github.com/COSIMA/mom6-panan)

4. [regrid runoff](https://github.com/adcroft/regrid_runoff)
5. [make regional mom6](https://github.com/favorliao/Reginal-MOM6)
