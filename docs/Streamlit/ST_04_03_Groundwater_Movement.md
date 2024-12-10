---
title: Groundwater Movement
layout: home
nav_order: 3
parent: Basic Hydrogeology
grand_parent: Streamlit Apps
has_children: false
---

<script type="text/javascript" async
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js">
</script>

### Streamlit Apps for the topic

# 04 Basic Hydrogeology



## Groundwater Movement



### Analytical solution for 1D unconfined flow with two defined head boundaries

### Conceptual model

The conceptual model considers the aquifer as a homogeneous and isotropic structure with a horizontal bottom. The aquifer is bounded by two defined-head boundary conditions on the in- and outflow part. From the top, the aquifer receives uniform groundwater recharge.

### Mathematical model

The equation for 1D groundwater flow in a homogeneous aquifer is


$$
\frac{d}{dx} \left(-hK \frac{dh}{dx} \right) = R
$$
with

- *x* is spatial coordinate along the flow,

- *h* is hydraulic head,

- *K* is hydraulic conductivity,

- *R* is recharge.

A solution for the equation can be obtained with two boundary conditions at *x* = 0 and *x* = *L*:


$$
h(0) = h_0
$$

$$
h(L)=h_L
$$



The solution for hydraulic head *h* along *x* is

$$
h(x) = \sqrt{h_0^2 - \frac{h_0^2 - h_L^2}{L} x + \frac{R}{K} x (L - x)}
$$


### Computation and visualization

Subsequently, the solution is computed and results are visualized. You can modify the parameters to investigate the functional behavior. You can modify the groundwater recharge *R* (in mm/a) and the hydraulic conductivity *K* (in m/s).



<img src="..\assets\images\st\04\GWF 1D unconf analytic ST.png" alt="screenshot of the app" width="400"/>

You can **access the app** here: [ https://gwf-1d-unconf-analytic.streamlit.app/](https://gwf-1d-unconf-analytic.streamlit.app/)



