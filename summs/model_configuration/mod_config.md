

The model setup has a uniform horizontal resolution 0.036 degrees and its domain bounded by latitude 4N to 25N and longitudes 77E to 99E. The bottom topography is based on new version of ETOPO (ETOPO version 1).

![Domain](grid_system.png)



The model has 41 vertical levels (HYCOM) and spacing gradually increases up to 5000m


![](topo.png)

All 4 sides are treated as solid rigid walls among them southern wall is fake rigid boundary. 


Equation of state used in the model is based on *Wright (1997)*. Vertical mising uses the KPP scheme with nonlocal mixing. Chlorophyll schemes are not used for estimating shortwave penetration.


| Field | Data Source | References | Frequency |
| ---   | --- | --- | --- | 
| Air Temperature (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Short wave Downward flux (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Longwave downward flux  (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Specific Humidity (K) | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m U wind | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| 10m V wind | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Precipitation | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Runoff rate | ERA 5 Interim reanalysis | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
| Sea Level Pressure | hPa | The ERA5 Global Reanalysis  Hersbach, H. et al. May 2020. QJRMS | daily |
