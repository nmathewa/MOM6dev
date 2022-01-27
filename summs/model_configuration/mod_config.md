

The model setup has a uniform horizontal resolution 0.036 degrees and its domain bounded by latitude 4N to 25N and longitudes 77E to 99E. The bottom topography is based on new version of ETOPO (ETOPO version 1).

![Domain](grid_system.png)



The model has 41 vertical levels (HYCOM) and spacing gradually increases up to 5000m


![](topo.png)

All 4 sides are treated as solid rigid walls among them southern wall is fake rigid boundary. 


Equation of state used in the model is based on *Wright (1997)*. Vertical mixing uses the KPP scheme with nonlocal mixing. Chlorophyll schemes are not used for estimating shortwave penetration.


| Field | Data Source | References | Frequency |
| ---   | --- | --- | --- | 
| Air Temperature (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Short wave Downward flux (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Longwave downward flux  (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Specific Humidity  | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m U wind (m/s)| ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m V wind (m/s)| ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Precipitation  | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Runoff flux  | GRUN |GRUN: An observations-based global gridded runoff dataset from 1902 to 2014 | monthly |
| Sea Level Pressure | ERA5 interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |


# Experiment

The model was start with Initial conditions (HYCOM) with SST,currents and SSS from 1 st January 2012. Using daily forcing datasets the model is set to run for 2 years.