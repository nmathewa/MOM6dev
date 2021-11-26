# UBUNTU

## Cloning and compiling

### 1. Libraries installtion (Ubuntu)

```BASH

sudo apt-get install csh
sudo apt-get install make
sudo apt-get install gfortran
sudo apt-get install openmpi-bin
sudo apt-get install libopenmpi-dev
sudo apt-get install libnetcdf-dev
sudo apt-get install libnetcdff-dev
sudo apt-get install netcdf-bin

```

### 2. FMS shared library

- Setting up the paths and make file
```BASH
mkdir -p build/intel/shared/repro/
cd build/intel/shared/repro/
../../../../src/mkmf/bin/list_paths -l ../../../../src/FMS
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/linux-gnu.mk -p libfms.a -c "-Duse_libMPI -Duse_netCDF" path_names)
```

- Compiling 
```BASH
make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 libfms.a -j
```



# Data Preparation

## Using Python scripts (aka mom6tools)

## Using FRE-NCtools

### 1. GRID creation

```BASH
make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd 77,99 --ybnd 4,23 --nlon 524 --nlat 384 --verbose'
```
### 2.mosaic creation

```BASH
make_solo_mosaic --num_tiles 1 --dir . --mosaic_name ocean_mosaic_india --tile_file mosaic.nc --periodx 0 --periody 0
```


### 3. Topog creation


```BASH
make_topog --mosaic ocean_mosaic_india.nc --topog_type realistic --topog_file gebco_test.nc --topog_field depth --scale_factor 1
```

## Running Examples

- The examples input datasets are located inside ocean_only/INPUT/

```bash'
ln -sf /lustre/f2/pdata/gfdl/gfdl_O/datasets .datasets
```

- The above data should be downloaded from the FTP use the code below to download the global input dataset

```bash
wget -nv ftp://ftp.gfdl.noaa.gov/perm/Alistair.Adcroft/MOM6-testing/global.tgz -q --show-progress
```


# SIS mod

add this line 

```BASH
make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 MOM6 -j
```

# References

1. [Model source, parameters and scripts used in first publications of OM4/CM4](https://zenodo.org/record/2601872#.YJOizCbhW00)
2. [MOM6 Input dataset for SmartSim ML EKE Experiment](https://zenodo.org/record/4682270#.YJOjdCbhW00)



