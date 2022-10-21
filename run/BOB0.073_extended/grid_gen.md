# Grid generation for extended BOB(4S to 25N in this case) for ~1/14 degree horizontal model 

ni = 300
nj = 396

## Horizontal grid
```
make_hgrid --grid_type regular_lonlat_grid --nxbnd 2 --nybnd 2 --xbnd 77,99 --ybnd -4,25 --nlon 600 --nlat 792 --verbose
```

## Mosaic grid creation
```
make_solo_mosaic --num_tiles 1 --dir . --mosaic_name bob_mosaic --tile_file horizontal_grid.nc --periodx 0 --periody 0
```

## Topography creation
```
make_topog --mosaic bob_mosaic.nc --topog_type realistic --topog_file gebco_bob.nc --topog_field elevation --scale_factor 1
```

## Coupled mosaic file
```
make_quick_mosaic --input_mosaic bob_mosaic.nc grid_spec --ocean_topog topog.nc
```
generated files due to this are:
* atmos_mosaic_tile1Xland_mosaic_tile1.nc 
* land_mosaic_tile1Xocean_mosaic_tile1.nc
* atmos_mosaic_tile1Xocean_mosaic_tile1.nc  
* mosaic.nc
* land_mask.nc        
* ocean_mask.nc
