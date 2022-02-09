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