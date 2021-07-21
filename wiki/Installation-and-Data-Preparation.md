## Cloning and compiling

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
