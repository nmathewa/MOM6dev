# Closed Boundaries

- A natural candidate for a closed boundary would be a coastline or possibly the shelf break. Physically, the condition is that no water flows across the boundary. Closed boundary conditions can further be classified as 
    1. **No Slip** - Where there is no flow along the boundary or through it 
    2. **Free Slip** - where there is flow along the boundary but not normal or perpendicular to boundary


# Open boundaries

- In most models other than global models, we need to set conditions for the sides of the domain not bounded by land

- goal for open boundaries is to allow waves and disturbances originating within the model domain to leave the domain without affecting the interior solution in a way that is not physically realistic

- The open boundaries can defined in certain ways, some of them are,
    1. **Nested Grid** - in a nested grid, values at the grid points from the larger model are used as boundary conditions at the appropriate locations in the smaller nested model
    2. **Specified boundary conditions** - Boundary conditions on open boundaries can be specified or prescribed in a number of ways. The boundaries can be set to climatological values, which could be held constant or interpolated from say monthly values to the time step of the model. Observations obtained on a continuing basis can also be used
    3. **Sponge Boundaries** - usually an additional set of gridpoints is used outside the actual physical area of the model to help implement open boundary conditions. In a sponge boundary, the idea is to absorb outward propagating waves and energy rather than having it reflect back into the model domain


# Code Overview

## Code Overview

1. create input datasets (U,V,SSH,S,T)

```python
ds = xr.merge([uu,vv,salt,ssh,temp])
```

2. boundary regional grid object

```python


xgrid = grid.x[::2,::2]
ygrid = grid.y[::2,::2]

south = xr.Dataset()

south['lon'] = xgrid.isel(nyp=0)
south['lat'] = ygrid.isel(nyp=0)

```

---

3. Regrid functions to regrid input data to regional grid

```python
v_south = regrid_south(ds_cut['v'])
u_south = regrid_south(ds_cut['u'])
temp_south = regrid_south(ds_cut['temp'])
ssh_south = regrid_south(ds_cut['eta_t'])
salt_south = regrid_south(ds_cut['salt'])

```

4. Fill values in z levels

```python
drowned_v_south = v_south.ffill(dim='nxp').ffill(dim='st_ocean')
drowned_u_south =u_south.ffill(dim='nxp').ffill(dim='st_ocean')
drowned_temp_south = temp_south.ffill(dim='nxp').ffill(dim='st_ocean')
drowned_salt_south = salt_south.ffill(dim='nxp').ffill(dim='st_ocean')
drowned_ssh_south = ssh_south.ffill(dim='nxp')

```
---
5. creating dz data for each variable

```python

cur_depth = south_obc.zl.values

reg_south_obc = south_obc.interp(zl=hy_depth)


south_dz_new = np.array
(len(reg_south_obc.xh.values)*
[np.array(len(reg_south_obc.yq.values)*
[np.array(len(reg_south_obc.time.values)*
[np.insert(np.diff(hy_depth),
                                                                                      0,1)])])])



```

---

6. time axis correction

```ferret
use nsouth.nc
define axis/t=1-jan-2012:31-dec-2013:1/units=days/calendar
=noleap/t0=31-dec-2011 time

let v11_segment_001 = v[gt=time@asn]
let u11_segment_001 = u[gt=time@asn]
let pt_segment_001 = temp[gt=time@asn]
let s_segment_001 = salt[gt=time@asn]
let ssh_segment_001 = ssh[gt=time@asn]
let dz_v11_segment_001 = dz_v[gt=time@asn]
let dz_u11_segment_001 = dz_u[gt=time@asn]
let dz_s_segment_001 = dz_salt[gt=time@asn]
let dz_pt_segment_001 = dz_temp[gt=time@asn]
set mem/size=2000
sp rm -f nsouth_only.nc
save/file=nsouth_only.nc/append 
v11_segment_001,u11_segment_001,pt_segment_001
,s_segment_001,ssh_segment

```
