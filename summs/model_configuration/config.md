---
title: "Model Configuration"
date: "2022-02-01"
titlepage: False
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-rule-height: 0
titlepage-background: "background.pdf"
table-use-row-colors : true
...

The model used is recent version of Geophysical Fluid Dynamics Laboratory (GFDL), an actively evolving unreleased version of code is publicaly available in the NOAA-GFDL public domain. Modular ocean model version 6 (MOM6) is a hydrostatic, primitive equation, free surface,Boussinesq ocean model with ALE vertical grid remapping to use any kind of vertical coordinates and generalized orthogonal horizontal coordinates. Equations governing ocean dynamics and thermodynamics are discretized on a fixed eulerian grid, with Arkawa C grid defining the horizonatal arrangement of model variables.

## Model Grid and Domain

The model setup has a uniform horizontal resolution 0.036 degrees in longitude and 0.036 degrees in latitude and model domain covers the bay of bengal between latitudes 4N to 25N and longitudes 77E to 99E. For simulating with closed boundaries, the area between latitudes 4N and 4.25 N (0.25 latitude thickness) is closed with fake rigid wall. Model topography is based on 1-min resolution ETOPO1 [*NOAA National Geophysical Data Center. 2009: ETOPO1 1 Arc-Minute Global Relief Model. NOAA National Centers for Environmental Information.*](https://www.ngdc.noaa.gov/mgg/global/)dataset with minimum depth of ocean as 5m and maximum depth of 5000m. 



The model has 41 vertical levels (HYCOM) with upper 12m having 2 meter spacing and up to 50m having an spacing of 5m. The spacing gradually increases up to 1000m when approaching the depth of 5000m.

![Domain](grid_system.png)





![Model Topography](topo.png)

All 4 sides are treated as solid rigid walls among them southern wall is fake rigid boundary. 
The bottom topography is based on new version of ETOPO (ETOPO version 1).




| Field | Data Source | References | Frequency |
| ---   | --- | --- | --- | 
| Air Temperature (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Short wave Downward flux (W/m^-2) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Longwave downward flux  (W/m^-2) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Specific Humidity  | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m U wind (m/s)| ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m V wind (m/s)| ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Precipitation  | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Runoff flux  | Dai, A. 2017 |Dai, A. 2017. Dai and Trenberth Global River Flow and Continental Discharge Dataset. | monthly |
| Sea Level Pressure | ERA5 interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |



## Model Physics options

Among a number of options available in MOM6 the following options are choosed for this model setup, McDougall et al. [2003] nonlinear equation of state has been used, with in situ density as a function of the local potential temperature, salinity and hydrostatic pressure. The tracer advection scheme is the Quicker scheme documented
by Holland et al. [1998]. Neutral tracer physics includes Redi neutral diffusion according to Griffies et al. [1998],and Gent-McWilliams stirring according to the Griffies [1998] skew-flux method. Vertical mixing scheme is the KPP scheme of Large et al. [1994] with nonlocal mixing. The coriolis scheme is, *Sadourny, R. [1975]*. The Tidal momentum forcing turned off.

The turbulent heat fluxes (sensible and latent heat flux) and the upward longwave flux are calculated as a function of model SST. Heat capacity of seawater is assumed to be constant (3992).Temperature and salinity are allowed to evolve freely without any restoration to climatological values.

## Forcing

Forcing datasets derived from The ERA5 Global Reanalysis [Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2018): ERA5 hourly data on single levels from 1979 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS)., 10.24381/cds.adbb2d47](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview) and observational global runoff data (GRUN) [ Dai, A. 2017. Dai and Trenberth Global River Flow and Continental Discharge Dataset. Research Data Archive at the National Center for Atmospheric Research, Computational and Information Systems Laboratory. https://doi.org/10.5065/D6V69H1T.](https://rda.ucar.edu/datasets/ds551.0/) . More about the forcing data is listed in the table 1

The model spin up was started with Initial conditions from HYCOM high resolution model output (HYCOM) with SST,U,V currents and SSS from 1 st January 2012. The model is forced by daily climatology derived from ECMWF reanalysis for the period 2012-2013. The sea-ice ,land and atmospheric components are turned on for all model runs. The first year (2012) is considered as cold run while the second year model is assumed to be stable.

--------------
