# Model setup 

## Domain setup 

1. Closed boundaries. Fake rigid wall is set in the Southern face
2. All the mosaic files are made using FRE-NC tools

## Initial conditions 

1. HYCOM 41 level initial conditions are used 
2. 2013-01-01-00:00:00

## Boundary conditions 

1. Since all 4 walls are closed ,  simulation will run in closed boundary condition

## Forcing datasets

1. Datasets from ERA5-reanalysis
   1. wind ,U10 and V10
   2. temp , T at 2 meters
   3. specific humidity 
   4. sea level pressure

All the units, and attributes in match with the MOM6 (MOM5, since MOM6 does not have any official guidline for creating forcing datasets) requirements


# Simulation outputs



# Setting up open boundary conditions 

![](Untitled%20Diagram.drawio.png)


- 3 ( or 4 open boundary segments )
- OBC_NUMBER_OF_SEGMENTS = 3
  
### segments setup

```
OBC_SEGMENT_001 = "I=99,J=5:7,SIMPLE
OBC_SEGMENT_002 = "J=5,I=98:99,SIMPLE
OBC_SEGMENT_003 = "J=4,I=76:90,SIMPLE
OBC_SEGMENT_004 = "I=76,J=4:7,SIMPLE

```
### Data setup


### Avaialable oboundary conditions

- SIMPLE - the boundary values of normal velocities are specified. User-specified fields for open boundaries can be set via OBC_USER_CONFIG in MOM_input, DOME, for instance. This user code is currently the only way to provide the cross-boundary transport required for SIMPLE boundaries. Supercritical is another example.

- SIMPLE_TAN - the boundary values of tangential velocities are specified. Does not need any user code for transports.

- SIMPLE_GRAD - the boundary value of the normal gradient of tangential flow is specified.

- GRADIENT - zero gradient of all fields near the boundary.

- FLATHER - a radiation boundary condition on the barotropic flow which attempts to comply with exterior values, tidal or otherwise.

- ORLANSKI - a radiation boundary condition on the baroclinic flow.

- OBLIQUE - a radiation boundary condition for baroclinic flows using oblique phase speeds (Raymond and Kuo, 1984).

- NUDGED - a modifier on the radiation conditions (ORLANSKI and OBLIQUE) to nudge to exterior velocity values.


- ORLANSKI_TAN - a radiation boundary condition for the baroclinic flow tangential to the boundary.

- NUDGED_TAN - a modifier on the radiation condition to nudge tangential flow to exterior velocity values.

- ORLANSKI_GRAD - a radiation boundary condition for dvdx or dudy, contributing to the vorticity and strain computations.

- NUDGED_GRAD - a modifier on the radiation condition to nudge dvdx or dudy to external values.

