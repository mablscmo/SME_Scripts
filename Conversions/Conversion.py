"""
-----------------------------------------
Created on 2020-04-158
author: Martin Montelius
Version: 0.1
-----------------------------------------

Conversions between wavenumber in cm**-1 and wavelengths in Å for both vacuum and air.

Formulas and constants taken from:
    https://www.as.utexas.edu/~hebe/apogee/docs/air_vacuum.pdf
    https://www.astro.uu.se/valdwiki/Air-to-vacuum%20conversion

The formulas take most kinds of input, float, int, list, tuple, np.array; but multiple outputs are always given as np.array.

nr_to_wl gives vacuum wavelengths below 2000Å and above 20000Å, with air wavelengths given inbetween, similar to how NIST gives its wavelengths.

Functions involving vacuum to air conversions have a vta_constants parameter, ciddor96 offers slightly better precision,
edlen66 is the one VALD uses.

inv_to_ev converts energylevels between inverse centimeters and electronvolts.
"""
import numpy as np

edlen66 = [8.34213*10**-5,2.406030*10**-2,1.5997*10**-4,130,130]
ciddor96 = [0, 5.792105*10**-2,1.67917*10**-3,238.0185,57.362]

def nr_to_vac(wnr):
    if isinstance(wnr,(list,tuple)):
        wnr = np.array(wnr)
    return(10**8/wnr)

def vac_to_nr(vac):
    if isinstance(vac,(list,tuple)):
        vac = np.array(vac)    
    return(10**8/vac)


def vac_to_air(vac,vta_constants=ciddor96):
    if isinstance(vac,(list,tuple)):
        vac = np.array(vac)        
    s = 10**4/vac
    a, b1, b2, c1, c2 = vta_constants
    
    n = 1 + a + b1/(c1 - s**2) + b2/(c2 - s**2)
    return(vac/n)

def air_to_vac(air):
    if isinstance(air,(list,tuple)):
        air = np.array(air)    
    s = 10**4/air
    n = 1 + 0.00008336624212083 + 0.02408926869968/(130.1065924522 - s**2) + 0.0001599740894897/(38.92568793293 - s**2)
    return(air*n)


def nr_to_air(wnr,vta_constants=ciddor96):
    if isinstance(wnr,(list,tuple)):
        wnr = np.array(wnr)
    return(vac_to_air(nr_to_vac(wnr),vta_constants))


def nr_to_wl(wnr,vta_constants=ciddor96):
    if isinstance(wnr,(list,tuple,float,int)):
        wnr = np.array(wnr)
    if np.all(wnr>50000) | np.all(wnr<5000) == True:
        return(nr_to_vac(wnr))
    elif np.all(wnr<50000) | np.all(wnr>5000) == True:
        return(nr_to_air(wnr,vta_constants))
    else:
        wl = []
        for i in range(len(wnr)):
            if wnr[i] < 5000 | wnr[i] > 50000:
                wl.append(nr_to_vac(wnr[i]))
            else:
                wl.append(nr_to_air(wnr[i],vta_constants))
        return(np.array(wl))


def inv_to_ev(inv):
    if isinstance(inv,(list,tuple)):
        inv = np.array(inv)        
    return(inv/8065.544)
