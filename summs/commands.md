# Installation


## Cloning MOM6-examples repo

```BASH
git clone https://github.com/NOAA-GFDL/MOM6-examples
cd MOM6-examples
git submodule init
git submodule update --recursive

```

## Compiling FMS shared 

```BASH
mkdir -p build/gnu/shared/repro/
cd  build/gnu/shared/repro/ 
../../../../src/mkmf/bin/list_paths -l ../../../../src/FMS
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/linux-gnu.mk -p libfms.a -c "-Duse_libMPI -Duse_netCDF" path_names)

make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 libfms.a -j

```

## Compiling MOM6-SIS

```BASH
cd MOM6-examples
mkdir -p build/intel/ice_ocean_SIS2/repro/
cd build/gnu/ice_ocean_SIS2/repro/
git submodule update --init --recursive

../../../../src/mkmf/bin/list_paths -l ./ ../../../../src/MOM6/config_src/{infra/FMS1,memory/dynamic_symmetric,drivers/FMS_cap,external} ../../../../src/MOM6/src/{*,*/*}/ ../../../../src/{atmos_null,coupler,land_null,ice_param,icebergs,SIS2,FMS/coupler,FMS/include}/
../../../../src/mkmf/bin/mkmf -t ../../../../src/mkmf/templates/linux-gnu.mk -o '-I../../shared/repro' -p MOM6 -l '-L../../shared/repro -lfms' -c '-Duse_AM3_physics -D_USE_LEGACY_LAND_' path_names

make NETCDF=3 REPRO=1 FC=mpif77 CC=mpicc LD=mpif77 MOM6 -j

```
> Go to .bashrc add line "export momsis=/home/neema/GIT/MOM6-examples/build/gnu/ice_ocean_SIS2/repro/MOM6"






