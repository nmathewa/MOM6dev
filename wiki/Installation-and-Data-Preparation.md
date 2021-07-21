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

```BASH
mkdir -p build/intel/shared/repro/
cd build/intel/shared/repro/
../../../../src/mkmf/bin/list_paths -l ../../../../src/FMS
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



# References

1. [Model source, parameters and scripts used in first publications of OM4/CM4](https://zenodo.org/record/2601872#.YJOizCbhW00)
2. [MOM6 Input dataset for SmartSim ML EKE Experiment](https://zenodo.org/record/4682270#.YJOjdCbhW00)