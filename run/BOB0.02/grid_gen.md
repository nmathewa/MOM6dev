# Grid generation for BOB for ~1/48 degree horizontal model 

ni = 1200 ;
nj = 1000

## Horizontal grid
```
make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd 77,99 --ybnd 4,25 --nlon 2400 --nlat 2000 --verbose
```

## Mosaic grid creation
```
make_solo_mosaic --num_tiles 1 --dir . --mosaic_name bob_mosaic --tile_file horizontal_grid.nc --periodx 0 --periody 0
```

## Topography creation
```
make_topog --mosaic bob_mosaic.nc --topog_type realistic --topog_file gebco_bob.nc --topog_field elevation --scale_factor 1
```

