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

### 2. Cloning and updating repo


``` BASH
git clone https://github.com/NOAA-GFDL/MOM6-examples
cd MOM6-examples
git submodule init
git submodule update --recursive

```

### 3. FMS shared code

```BASH
mkdir -p build/gnu/shared/repro/
cd  build/gnu/shared/repro/ 
../../../../src/mkmf/bin/list_paths -l ../../../../src/FMS
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/linux-gnu.mk -p libfms.a -c "-Duse_libMPI -Duse_netCDF" path_names)

make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 libfms.a -j



```

### 4. Compiling MOM6 in MOM6-SIS2 coupled mode

```BASH

cd MOM6-examples
mkdir -p build/intel/ice_ocean_SIS2/repro/
cd build/gnu/ice_ocean_SIS2/repro/
git submodule update --init --recursive

../../../../src/mkmf/bin/list_paths -l ./ ../../../../src/MOM6/config_src/{infra/FMS1,memory/dynamic_symmetric,drivers/FMS_cap,external} ../../../../src/MOM6/src/{*,*/*}/ ../../../../src/{atmos_null,coupler,land_null,ice_param,icebergs,SIS2,FMS/coupler,FMS/include}/
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/linux-gnu.mk -o '-I../../shared/repro' -p MOM6 -l '-L../../shared/repro -lfms' -c '-Duse_AM3_physics -D_USE_LEGACY_LAND_' path_names

make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 MOM6 -j


```



# General Linux based installation (CentOS, Arch)

## GNU installation

1. GMP
   ```bash
   tar -vxf gmp-6.1.0.tar.bz2
   cd gmp-6.1.0/
   mkdir build
   ./configure --prefix=/path/to/GMP
   make 
   sudo make install
   
   export LD_LIBRARY_PATH=/path/to/GMP/gmp-6.1.0/lib:$LD_LIBRARY_PATH
   ```

2. MPFR
   ```bash
   tar -xvf mpfr-3.1.4.tar.bz2   
   cd mpfr-3.1.4/
   mkdir build
   ./configure --prefix=/path/to/MPFR --with-gmp=/path/to/GMP/gmp-6.1.0
   make 
   sudo make install
   
   export LD_LIBRARY_PATH=/path/to/MPFR/mpfr-3.1.4/lib:$LD_LIBRARY_PATH
   ```
3. MPC
   ```bash
   tar -zvxf mpc-1.0.3.tar.gz   
   cd mpc-1.0.3/
   mkdir build
   ./configure --prefix=/path/to/MPC/mpc-1.0.3 --with-gmp=/path/to/GMP/gmp-6.1.0 --with-mpfr=/path/to/MPFR/mpfr-3.1.4
   make 
   sudo make install
   
   export LD_LIBRARY_PATH=/path/to/MPC/mpc-1.0.3/lib:$LD_LIBRARY_PATH
   ```
4. GNU
   ```bash
   tar -vxf gcc-9.1.0.tar.xz   
   cd gcc-9.1.0/
   mkdir obj build
   cd obj
   .../configure --disable-multilib --enable-languages="c,c++,fortran" --prefix=/path/to/GNU --disable-static --enable-shared --with-gmp=/path/to/GMP/gmp-6.1.0 --with-mpfr=/path/to/MPFR/mpfr-3.1.4 --with-mpc=/path/to/MPC/mpc-1.0.3

   make 
   make install
   
   export PATH=/path/to/GNU/bin:$PATH
   export LD_LIBRARY_PATH=/path/to/GNU/lib64:$LD_LIBRARY_PATH
   ```
## OpenMPI installation





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






