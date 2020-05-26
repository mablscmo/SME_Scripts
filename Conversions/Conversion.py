"""
-----------------------------------------
Created on 2020-04-158
author: Martin Montelius
Version: 0.2.1
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

New in version 0.2:
    New function conversion(), takes From and To as arguments and lets you write in numbers to your hearts content, converting them to whatever you
    want (as long as it is implemented). Can also take number of decimals as input, default is 3, and the vac to air variables just like the 
    regular functions. Give it q to quit. 
    Also implemented electronvolt to inverse centimeters function.

    0.2.1:
    Implemented eV/inv cm to vac/air/nr. The conversion() implementation works but is sort of wonky, giving input as a tuple, list or just a comma
    between two numbers works fine. 
    

"""
import numpy as np

edlen66 = [8.34213*10**-5,2.406030*10**-2,1.5997*10**-4,130,130]
ciddor96 = [0, 5.792105*10**-2,1.67917*10**-3,238.0185,57.362]


"_____________________________________________Wavelengths and wavenumbers_____________________________________________"
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

def air_to_nr(air):
    if isinstance(air,(list,tuple)):
        air = np.array(air) 
    return(vac_to_nr(air_to_vac(air)))


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



"_________________________________________________Energies_________________________________________________"
def inv_to_ev(inv,upper=None):
    if isinstance(inv,(list,tuple,float,int)):
        inv = np.array(inv)        
    if upper != None:
       upper = np.array(upper)
       inv = np.stack((inv,upper))
    return(inv/8065.544)

def ev_to_inv(ev,upper=None):
    if isinstance(ev,(list,tuple,float,int)):
        ev = np.array(ev)        
    if upper != None:
       upper = np.array(upper)
       ev = np.stack((ev,upper))
    return(ev*8065.544)

def ev_to_erg(ev,upper=None):
    if isinstance(ev,(list,tuple,float,int)):
        ev = np.array(ev)        
    if upper != None:
       upper = np.array(upper)
       ev = np.stack((ev,upper))
    return(ev*1.60217733e-12)

def erg_to_ev(erg,upper=None):
    if isinstance(ev,(list,tuple,float,int)):
        erg = np.array(erg)        
    if upper != None:
       upper = np.array(upper)
       erg = np.stack((erg,upper))
    return(erg/1.60217733e-12)

def inv_to_erg(inv,upper=None):
    if isinstance(ev,(list,tuple,float,int)):
        inv = np.array(inv)        
    if upper != None:
       upper = np.array(upper)
       inv = np.stack((inv,upper))
    return(inv_to_ev(ev_to_erg(inv)))

def erg_to_inv(erg,upper=None):
    if isinstance(ev,(list,tuple,float,int)):
        erg = np.array(erg)        
    if upper != None:
       upper = np.array(upper)
       erg = np.stack((erg,upper))
    return(erg_to_ev(ev_to_inv(erg)))


"________________________________________________Energy to wl_______________________________________________"
c = 2.99792458e8    # ms-1 Speed of light
h = 4.135667696e-15  #eVs Planck constant 

def ev_to_vac(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(h*c*10**10/(upper-lower))

def ev_to_air(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(vac_to_air(h*c*10**10/(upper-lower)))

def ev_to_nr(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(vac_to_nr(h*c*10**10/(upper-lower)))

def inv_to_vac(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(h*c*10**10/(inv_to_ev(upper)-inv_to_ev(lower)))

def inv_to_air(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(vac_to_air(h*c*10**10/(inv_to_ev(upper)-inv_to_ev(lower))))

def inv_to_nr(lower,upper,c=c,h=h):
    if isinstance(lower,(list,tuple)) or isinstance(upper,(list,tuple)):
        lower = np.array(lower)
        upper = np.array(upper)
    return(vac_to_nr(h*c*10**10/(inv_to_ev(upper)-inv_to_ev(lower))))



"____________________________________________CONVERSION FUNCTION____________________________________________"
air, vac, nr, wl, inv, ev, erg, q = 'air', 'vac', 'nr', 'wl', 'inv', 'ev', 'erg', 'quit'
Air, Vac, Nr, Wl, Inv, eV, Erg, Q = 'air', 'vac', 'nr', 'wl', 'inv', 'ev', 'erg', 'quit'

def conversion(From, To, dec=3, vta_constants=ciddor96):
    if (From == 'air') & (To == 'vac'):
        def converter(number):
            return(print(round(float(air_to_vac(number)),dec)))
    elif (From == 'vac') & (To == 'air'):
        def converter(number):
            return(print(round(float(vac_to_air(number,vta_constants)),dec)))
    elif (From == 'inv') & (To == 'ev'):
        def converter(number):
            return(print(round(float(inv_to_ev(number)),dec)))
    elif (From == 'ev') & (To == 'inv'):
        def converter(number):
            return(print(round(float(ev_to_inv(number)),dec)))
    elif (From == 'nr') & (To == 'wl'):
        def converter(number):
            return(print(round(float(nr_to_wl(number,vta_constants)),dec)))
    elif (From == 'nr') & (To == 'air'):
        def converter(number):
            return(print(round(float(nr_to_air(number)),dec)))
    elif (From == 'nr') & (To == 'vac'):
        def converter(number):
            return(print(round(float(nr_to_vac(number)),dec)))
    elif (From == 'vac') & (To == 'nr'):
        def converter(number):
            return(print(round(float(vac_to_nr(number)),dec)))
    elif (From == 'air') & (To == 'nr'):
        def converter(number):
            return(print(round(float(air_to_nr(number)),dec)))
    elif (From == 'ev') & (To == 'erg'):
        def converter(number):
            return(print(round(float(ev_to_erg(number)),dec)))
    elif (From == 'erg') & (To == 'ev'):
        def converter(number):
            return(print(round(float(erg_to_ev(number)),dec)))
    elif (From == 'inv') & (To == 'erg'):
        def converter(number):
            return(print(round(float(inv_to_erg(number)),dec)))
    elif (From == 'erg') & (To == 'inv'):
        def converter(number):
            return(print(round(float(erg_to_inv(number)),dec)))
    elif (From == 'ev') & (To == 'vac'):
        print('Give input as: lower,upper')
        def converter(number):
            return(print(round(float(ev_to_vac(number[0],number[1])),dec)))        
    elif (From == 'ev') & (To == 'air'):
        print('Give input as: lower,upper')
        def converter(number):
            return(print(round(float(ev_to_air(number[0],number[1])),dec)))
    elif (From == 'ev') & (To == 'nr'):
        print('Give input as: lower,upper')
        def converter(number):
            return(print(round(float(ev_to_nr(number[0],number[1])),dec)))
    elif (From == 'inv') & (To == 'vac'):
        print('Give input as: upper,lower')
        def converter(number):
            return(print(round(float(inv_to_vac(number[0],number[1])),dec)))        
    elif (From == 'inv') & (To == 'air'):
        print('Give input as: upper,lower')
        def converter(number):
            return(print(round(float(inv_to_air(number[0],number[1])),dec)))
    elif (From == 'inv') & (To == 'nr'):
        print('Give input as: upper,lower')
        def converter(number):
            return(print(round(float(inv_to_nr(number[0],number[1])),dec)))
    else:
        print('Conversion from {} to {} not yet implemented'.format(From,To))
        raise SystemExit('Please try again')
    global number
    print("Input 'q' to quit")
    while True:
        try:
            number = eval(input('{} to {}: '.format(From,To)))
        except NameError:
            print('Input not recogniced')
            continue
        if number == 'quit':
            print('Conversion stopped')
            break  
        else:
            converter(number)
        continue
