## Directory architecure


### setting up custom directory 

## Namelist description (Required ones)

|namelist_id | name | notes | 
| ----- | -----| -----|
| NIGLOBAL | Total number of grid points in x direction|
| NJGLOBAL | Total number of grid points in the y direction | |
DT | baroclinic dynamic timestep | integer fraction of forcing timestep |
DT_THERM | thermodynamic and tracer advection timestep | int multiple of DT and less than forcing or coupling time-step|
FRAZIL | if True water freezes if it gets too cold | accumulated heat deficit returned to surface state |
DO_GEOTHERMAL | If True apply geothermal heating | |
BOUND_SALINITY | If True limit salinity to be +ve | |
C_P = 3925.0 | heat capacity of sea water | |
SAVE_INITIAL_CONDS = True | | |
IC_OUTPUT_FILE = ' ' | | |
INPUTDIR = ' ' | 
GRID_CONFIG = ' ' | mosaic , cartesian , spherical | method for defining horizonta grid. Mosaic needs the mosaic geometry files |
|GRID_CONFIG = ' '| Name of the file that read horizontal grid data |
|TOPO_CONFIG = ''| This specifies how bathymetry is specified | 'file' reads the TOPO_FILE |
MAXIMUM_DEPTH = 6000 | maximum depth of ocean | |
MINIMUM_DEPTH = 0.5 |  | based on maskin depth anython shallower than minimum depth assumed to be land |
CHANNEL_CONFIG = "global_1deg" | | |
NK = 63 | Number of model layers | 
USE_IDEAL_AGE_TRACER = True |If true, use the ideal_age_example tracer package | 
**COORD_CONFIG** = "file" | This specifies how layers are to be defined |
THICKNESS_CONFIG = "file" | A string that determines how the initial layer thicknesses are specifie for a new run | "file" reads the thickness file THICKNESS_FILE
THICKNESS_FILE = " " | Name of the thickness file | 
ADJUST_THICKNESS = True |If true, all mass below the bottom removed if the topography is shallower than the thickness input file would indicate | 
TS_CONFIG = "file" | A string that determines how the initial tempertures and salinities are specified for a new run | file read velocities from TS_FILE
TS_FILE = "GOLD_IC.2010.11.15.nc" | The initial condition file for temperature | 
