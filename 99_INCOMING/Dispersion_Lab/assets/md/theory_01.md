### Advection, dispersion, and mixing

**Advection** carries dissolved mass with moving water. **Mechanical dispersion** describes spreading caused by differences in velocity and pathway. **Molecular diffusion** redistributes solute through molecular motion. A plume can spread without becoming locally well mixed; plume width alone is not a mixing measure ([Devlin, 2020](https://books.gw-project.org/groundwater-velocity/chapter/subsurface-mixing/); [Dentz, Hidalgo & Lester, 2023](https://doi.org/10.1007/s11242-022-01852-x)).

This module represents a conservative, passive solute by equal-mass markers. They are computational parcels of dissolved mass, not grains or molecules that collide. A left/right choice summarizes unresolved pathway selection. The physical Galton board motivates the analogy, but the code does not calculate gravitational acceleration or disk collisions.

Begin with the fixed experiment below. Open the equations when you want to explain your observations. Full source details and model limits are available under **References and model notes**.
