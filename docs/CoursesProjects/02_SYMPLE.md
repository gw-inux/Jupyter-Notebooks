---
title: SYMPLE
layout: home
nav_order: 2
parent: Courses and Projects
has_children: false
---

# [SYMPLE - School of Hydrogeological Modeling](https://hydrosymple.com/en/)

A collection of Jupyter Notebooks for the SYMPLE School of Hydrogeological Modeling.

![Symple_Logo](.\assets\images\symple\Symple_logo.png)

You can **access and execute them online** with your browser through the MyBinder service with the provided link or by using the QR code on your mobile device. These links will render all Notebooks as (user-friendly) Voila Dashboards, i.e., the underlying Python Code is invisible.

 _Alternatively,_ you can access the whole repository of notebooks online with [this link to MyBinder](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F) (eventually, the start takes some minutes - please be patient). Then, browse through the collection of notebooks and execute them. _If you are new to Jupyter Notebooks,_ it is suggested to have a look at [00_Getting_started.ipynb](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F00_Getting_started.ipynb).

Alternatively, you can download the Jupyter Notebooks from the GitHub repository (specified in Origin* within the table) and **execute them locally** through a suitable Jupyter Notebook installation (e.g., Anaconda). With a properly installed Anaconda, just

* open the command window with `CMD`.
* Browse to your local folder on your computer that contains the Jupyter Notebooks.
* Start your local Jupyter interpreter (hub) by typing `Jupyter Notebook` in your command window.
* Subsequently, your browser should open, and you will be ready to execute the notebooks.

**_Table legend / Abbreviations:_**

**Origin*: ** (Repository) [_01 - Water cycle_](https://github.com/gw-inux/Jupyter-Notebooks/tree/main/01%20Water%20cycle); _02 - Basic hydrology_; [_03 Soil physics_](https://github.com/gw-inux/Jupyter-Notebooks/tree/main/03%20Soil%20physics); [_04 Basic hydrogeology_](https://github.com/gw-inux/Jupyter-Notebooks/tree/main/04%20Basic%20hydrogeology); [_05 Applied hydrogeology_](https://github.com/gw-inux/Jupyter-Notebooks/tree/main/05%20Applied%20hydrogeology); [_06 Groundwater modeling_](https://github.com/gw-inux/Jupyter-Notebooks/tree/main/06%20Groundwater%20modeling)

**Type\**:** Notebook...  **A)** with explanations; **B)** just figure; **C)** as a workbook 

| Content | Origin*/Type** | Preview | Access | QR access |
| ------------------------------------------------------------ | :-----------: | :-------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------: |
| (01) **Volume_Mass_Budget.ipynb**: Water cycle and mass balances, incl. the example of radioactive decay. | _01_/**C**  | ![](.\assets\images\symple\pre\PRE_SY001.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F01+Water+cycle%2FVolume_Mass_Budget.ipynb) | ![](.\assets\images\symple\qr\QR_SY001.png) |
| (02) **Radioactive_Decay.ipynb**: Mass balances and example of radioactive decay. | _01_/**A**  | ![](.\assets\images\symple\pre\PRE_SY002.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F01+Water+cycle%2FRadioactive_Decay.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F01+Water+cycle%2FRadioactive_Decay.ipynb) | ![](.\assets\images\symple\qr\QR_SY002.png) |
| (03) **1D_Conduction.ipynb**: A comparison of diffusive/conductive movement for groundwater flow and heat transport. | _05_/**A**  | ![](.\assets\images\symple\pre\PRE_SY003.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F05+Applied+hydrogeology%2F1D_Conduction.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F05+Applied+hydrogeology%2F1D_Conduction.ipynb) | ![](.\assets\images\symple\qr\QR_SY003.png) |
| (04) **GWF_1D_unconf_analytic_v00.ipynb**: A solution for 1D unconfined flow, bounded by two defined heads; variation of hydraulic conductivity and recharge. | _04_/**A**  | ![](.\assets\images\symple\pre\PRE_SY004.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_v00.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_v00.ipynb) | ![](.\assets\images\symple\qr\QR_SY004.png) |
| (05) **GWF_1D_unconf_analytic_BC.ipynb**: Differences between physical and hydraulic boundary conditions based on the analytical solution of 1D unconfined groundwater flow. | _04_/**C**  | ![](.\assets\images\symple\pre\PRE_SY005.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_BC.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_BC.ipynb) | ![](.\assets\images\symple\qr\QR_SY005.png) |
| (06) **GWF_1D_unconf_analytic_BC3.ipynb**: Analytical solution for 1D unconfined groundwater flow demonstrating the behavior of a 3rd type (Robin) boundary. | _04_/**A**  | PRE                                           | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_BC3.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FGWF_1D_unconf_analytic_BC3.ipynb) | ![](.\assets\images\symple\qr\QR_SY006.png) |
| (07) Theis_interactive.ipynb                                 | _05_/**A**  | PRE                                           | NB Binder Voila Binder                                       | QR                                         |
| (08) TYPE_CURVE_MATCHING_VARNUM.ipynb               | _05_/**A**  | PRE                                           | NB Binder Voila Binder                                       | QR                                         |
| (09) Well_Catchment.ipynb                                    | _04_/**A**  | PRE                                           | NB Binder Voila Binder                                       | QR                                         |
| (10) **TRANS_1D_AD_analytic.ipynb**: Analytical solution of 1D transport with advection and dispersion. Incl. curve fitting with given data. | _05_/**A**  | ![](.\assets\images\symple\pre\PRE_SY010.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FTRANS_1D_AD_analytic.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FTRANS_1D_AD_analytic.ipynb) | ![](.\assets\images\symple\qr\QR_SY010.png) |
| (11) TRANS_1D_MT3D.ipynb                                     | _06_/**A**  | PRE                                           | Offline use | Offline use |
| (12) **DCC_Equivalent_Hydr_Cond.ipynb**: Computes the equivalent hydraulic conductivity (for Darcys law) of a karst conduit. | _05_/**B**  | ![](.\assets\images\symple\pre\PRE_SY012.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FDCC_Equivalent_Hydr_Cond.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FDCC_Equivalent_Hydr_Cond.ipynb) | ![](.\assets\images\symple\qr\QR_SY012.png) |
| (13) **DCC_Flow_Equations.ipynb**: Interactive plot of discharge vs. hydraulic gradient for the Hagen-Poiseuille and Colebrook-White equation. | _05_/**B**  | ![](.\assets\images\symple\pre\PRE_SY013.png) | [![Binder](.\assets\images\NB_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=notebooks%2F04+Basic+hydrogeology%2FDCC_Flow_Equations.ipynb) [![Binder](.\assets\images\VD_badge_logo.png)](https://mybinder.org/v2/gh/gw-inux/Jupyter-Notebooks/HEAD?urlpath=voila%2Frender%2F04+Basic+hydrogeology%2FDCC_Flow_Equations.ipynb) | ![](.\assets\images\symple\qr\QR_SY013.png) |
