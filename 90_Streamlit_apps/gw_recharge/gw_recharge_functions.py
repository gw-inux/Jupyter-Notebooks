import numpy as np

def evaporation_from_radiation(lat, doy):
    '''
    input params:
        lat...int: latitute of the weather station [°]
        doy...array: day of the year 
    output params:
        E_r...array: Evaporation dur to extraterrestrial radiation for every day of the year [mm/d]
        R_e...array: Extraterrestrial radiation [MJ/m²/d]
    '''
    ### calculate the extraterrestrial radiation to plot along ETP
    lat_rad = lat*np.pi/180  # in rad

    ### variables dependent on the doy
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365)  # inverse relative change in distance between Earth and Sun
    delta = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39) # declination of the sun
    omega_s = np.arccos(-np.tan(lat_rad) * np.tan(delta)) # sunset hour angle

    ### Therefrom we calculate the extraterrestrial radiation in [MJ/m2/d]: Re
    R_e = 24 * 60 / np.pi * 0.082 * dr * (omega_s * np.sin(lat_rad) * np.sin(delta) + np.cos(lat_rad) * np.cos(delta) * np.sin(omega_s))

    ## And finally the evaporation due to the extraterrestrial radiation in [mm/d]
    E_r = R_e / 2.45

    return E_r, R_e


def linear_reduction_function(S_B_A, TAW, p=0.5):
    """
    This function calculates the water stress coefficient K_s based on the volumetric soil moisture.
    input params:
        S_B_A...float: The volumetric soil moisture [%]
        TAW...float: The volumetric soil moisture at the field capacity in [%]
        p...float: The fraction of the field capacity at which the plant starts to experience water stress []
    output params:
        K_s...float: The water stress coefficient
    """ 
    # calculate the "tipping point"
    theta_0 = TAW * (1-p)

    if S_B_A >= theta_0:
        K_s = 1 

    elif S_B_A <= 0:
        K_s = 0 

    elif S_B_A > 0 and S_B_A < theta_0:
        K_s = (S_B_A ) / (theta_0 )

    return K_s


def update_moisture_content(S_B_A, precip, ETA, TAW):
    '''
    input params:
        S_B_A...float: Soilwater storage [mm/d]
        precip...float: Precipitation [mm/d]
        ETA...float: Actual Evapotranspiration [mm/d]
        TAW...float: The volumetric soil moisture at the field capacity in [%]
    output params:
        updated_S_B_A...float: Updated Soilwater storage [mm/d]
        excess_water...float: Excess water [mm/d]
    '''
    # check if water holding capacity is exceeded, and if it is: update the TAW and calculate the excess water...
    if S_B_A + precip - ETA > TAW:
        updated_S_B_A = TAW
        excess_water = S_B_A + precip - ETA - TAW
        
    #...else set the excess water = 0
    else: 
        updated_S_B_A = S_B_A + precip - ETA
        excess_water = 0 

    return updated_S_B_A, excess_water


def run_recharge_simulation(TAW, p, ETP, precip):
    '''
    input params:
        TAW...array: The volumetric soil moisture at the field capacity in [%]
        p...array: The fraction of the field capacity at which the plant starts to experience water stress []
        ETP...array: Potential evapotranspiration [mm/d]
        precip...array: Precipitation [mm/d]
    output params:
        ETA...array: Actual evapotranspiration [mm/d]
        S_B_A...array: Soilwater storage [mm/d]
        gw_recharge...array: Groundwater recharge [mm/d]
    '''

    # setting initial values, initiating arrays/variables
    gw_recharge = np.zeros(len(ETP))
    S_B_A = np.zeros(len(ETP))
    
    initial_soil_moisture = TAW # assuming that the soil is saturated at the beginning 
    S_B_A[0] = initial_soil_moisture

    initial_fraction_of_ETP = 1 # ETA/ETP
    ETA = np.zeros(len(ETP))
    
    # then update the values
    for i in np.arange(1, len(ETP)):   # for every value within the arrays
        
        ETA[0] = initial_fraction_of_ETP * ETP[i]
        
        K_s = linear_reduction_function(S_B_A[i-1], TAW, p)
        ETA[i] = K_s * ETP[i]  

        S_B_A[i], excess_water = update_moisture_content(S_B_A[i-1], precip.iloc[i], ETA[i], TAW)

        gw_recharge[i] = excess_water
    
    return gw_recharge, ETA, S_B_A

def water_budget(TAW, p, alpha, V_GW_0, Irr_eff, Q_env, A_irr_tot, GWL_0, Sy, gw_recharge, precip, ETA, irrigated=True):
    '''
    input parameters:
        TAW...int: total available water [mm]
        p...float: readily available water/ totally available water []
        alpha...float: [1/d]
        V_GW_0...int: initial groundwater volume [mm]
        Irr_eff: float: []
        Q_env...float: environmentally friendly amound of runoff [mm/d]
        A_irr_tot...float: Part of the total Area that is beeing irrigated []
        GWL_0...float: groundwater level [mü.NN]
        gw_recharge...np.array: groundwater recharge for the non irrigated area [mm/d]
        precip...np.array: precipitation [mm]
        ETA...actual evapotranspiration [mm/d]
    output parameters:
        Si
        gw_recharge_irr
        V_GW_tot
        Q_GW_tot
        ID
        Ia
        GWL
    '''
    if irrigated==False:
        Out=np.zeros_like(gw_recharge, dtype=float)
        V_GW=np.zeros_like(gw_recharge, dtype=float)
        V_GW[0]=V_GW_0
        for i in range(1, len(In)):
            Out[i-1] = V[i-1] * k
            V_GW[i] = V[i-1] - Out[i-1] + In[i]

    if irrigated==True:
        Si, gw_recharge_irr, V_GW_tot, Q_GW_tot, ID, Ia, GWL =[np.zeros_like(gw_recharge) for i in range(7)]
        Si[0]=1
        V_GW_tot[0]=V_GW_0
        GWL[0]=GWL_0

        for i in np.arange(1,len(gw_recharge)-1):
            #Si...initial storage [mm]
            if Si[i-1]+ precip[i] - ETA[i] > TAW:
                Si[i]= TAW
            else:
                Si[i]=Si[i-1]+precip[i]-ETA[i]
            #gw_recharge_irr...rechargenoff [mm/d]
            if Si[i-2]+precip[i-1]-ETA[i-1]>TAW:
                gw_recharge_irr[i-1]=Si[i-2]+precip[i-1]-ETA[i-1]-TAW
            else:
                gw_recharge_irr[i-1]=0
            #V_GW_tot...total groundwater volume [mm]
            V_GW_tot[i]=V_GW_tot[i-1]+gw_recharge_irr[i]*A_irr_tot+gw_recharge[i]*(1-A_irr_tot)-Q_GW_tot[i-1]-Ia[i-1]
            #Q_GW_tot...total groundwater runoff [mm/d]
            Q_GW_tot[i-1]=V_GW_tot[i-1]*alpha
            #ID...d??? irrigation[mm]
            if Si[i-1]>(1-p)*TAW:
                ID[i-1]=0
            else:
                ID[i-1]=((1-p)*TAW-Si[-1])*A_irr_tot
            #Ia...actual irrigation [mm]
            if ID[i-1] > 0:
                if ((Q_GW_tot[i-1]-ID[i-1])/Irr_eff)>Q_env:
                    Ia[i-1]=ID[i-1]/Irr_eff
                else:
                    Ia[i-1]=Q_GW_tot[i-1]-Q_env
            else:
                Ia[i-1]=0
            #GWL...groundwater level above normal null [mü.NN]
            GWL[i]= GWL[i-1]-(((V_GW_tot[i]-V_GW_tot[i-1])/Sy)/1000)

        if Si[-2]+precip[-1]-ETA[-1]>TAW:
            gw_recharge_irr[-1]=Si[-2]+precip[-1]-ETA[-1]-TAW
        else:
            gw_recharge_irr[-1]=0
        Q_GW_tot[-1]=V_GW_tot[-1]*alpha
        if Si[-1]>(1-p)*TAW:
            ID[-1]=0
        else:
            ID[-1]=((1-p)*TAW-Si[-1])*A_irr_tot

    return Si, gw_recharge_irr, V_GW_tot, Q_GW_tot, ID, Ia, GWL



            

        

            


