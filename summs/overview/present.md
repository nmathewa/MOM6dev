---
marp: true

---

## Aim 

- Configure and setup high-resolution ocean model for bay of bengal region 


## Model overview


- **Geophysical Fluid Dynamics Laboratory (GFDL) MOM6** 
- publicly available in the NOAA-GFDL public domain. (GIT)
-  Modular ocean model version 6 (MOM6) is a hydrostatic, primitive equation, free surface,Boussinesq ocean model with **ALE vertical grid remapping** to use any kind of vertical coordinates and generalized orthogonal horizontal coordinates.
-   Equations governing ocean dynamics and thermodynamics are discretized on a fixed eulerian grid, with **Arkawa C grid** defining the horizontal arrangement of model variables

---

![bg 100%](Model%20Build.png)

---

# Domain

![bg left 100%](../model_configuration/grid_system.png)


- 0.062 degrees resolution
- 4N , 25N and 77E to 99E
- 1-min ETOPO1
- 41 levels vertical resolution (HYCOM)
- max depth of 5000m



---

# Boundary Conditions


![bg left 80%](../2012_2013_forc_cbc/domain.png)

- 3 boundaries were considered
- One closed and two open boundaries
- The input data for boundaries are from Indian ocean model simulation (MOM5)  


---


## Track and progress

![](git_page.png)


---


![bg 40%](MOM6dev%20repo.png)

---

## Overview of simulations

![](Rigid%20boundary%20Simulations.png)


---


![bg 80%](SST.png)



---

![bg 80%](SSS.png)

---

![bg 80%](SSH.png)

---

![bg 70%](4%20SSV.png)


---

# Next steps

## Short term

- A good amount of experimentation's needed with open boundary
- comparison of namelist and physics option with previous runs
- using 1 hourly high resolution forcing (temp,slp,u and v)

## Long term

- Increasing the resolution and tests
