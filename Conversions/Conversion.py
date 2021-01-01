"""
-----------------------------------------
Created on 2020-04-15
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

New in version 0.3:
    Implemented command line functionality with conversion(), works better than expected.
    Added better unit handling for hz_to_wl and wl_to_hz
    Cleaned up some formatting
    

To do list:
    
    Import new air2vac, vac2air parameters from PySME's util.py. Not sure where they get them, Piskunov wrote it though.
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

"______________________________________________Frequency to wl______________________________________________"

def hz_to_wl(hz,prefix=None,angstrom=False,c=c):
    '''Default takes Hz and gives meters. Remember that differences need to be
    calculated from a set value.'''
    if isinstance(hz,(list,tuple)):
        hz = np.array(hz)
    if prefix != None:
        prefix = prefix.capitalize()
        if prefix == 'K':
            hz = hz*10**3
        elif prefix == 'M':
            hz = hz*10**6
        elif prefix == 'G':
            hz = hz*10**9
        elif prefix == 'T':
            hz = hz*10**12
    if angstrom != False:
        c = c*10**10            
    return(c/hz)

def wl_to_hz(wl,angstrom=False,c=c):
    '''Default takes Hz and gives meters. Remember that differences need to be
    calculated from a set value.'''
    if isinstance(wl,(list,tuple)):
        wl = np.array(wl)
    if angstrom != False:
        c = c*10**10           
    return(c/wl)

"____________________________________________CONVERSION FUNCTION____________________________________________"
air, vac, nr, wl, inv, ev, erg, hz, q, k, m, g, t = 'air', 'vac', 'nr', 'wl', 'inv', 'ev', 'erg', 'hz', 'quit', 'K', 'M', 'G', 'T'
Air, Vac, Nr, Wl, Inv, eV, Erg, Hz, Q, K, M, G, T = 'air', 'vac', 'nr', 'wl', 'inv', 'ev', 'erg', 'hz', 'quit', 'K', 'M', 'G', 'T'

def conversion(From, To, dec=3, vta_constants=ciddor96):
    print('\n')
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
    elif (From == 'hz') & (To == 'wl'):
        print('Give input as: frequency,prefix')
        def converter(number):
            wl = float(hz_to_wl(number[0],number[1]))
            if np.all(wl >= 10**3):
                pre, div  = 'km', 10**3
            elif np.all(wl >= 10**0) & np.all(wl < 10**3):
                pre, div = 'm', 10**0
            elif np.all(wl >= 10**-2) & np.all(wl < 10**0):
                pre, div = 'cm', 10**-2
            elif np.all(wl >= 10**-4) & np.all(wl < 10**-2):
                pre, div  = 'mm', 10**-3
            elif np.all(wl >= 10**-6) & np.all(wl < 10**-4):
                pre, div  = 'um', 10**-6
            elif np.all(hz <= 10**-6):
                pre, div = 'Å', 10**-10
            else:
                pre, div = '',1
            return(print(f'{round(wl/div,dec)} {pre}'))            
    elif (From == 'wl') & (To == 'hz'):
        def converter(number):
            hz = float(wl_to_hz(number,angstrom=False))
            if np.all(hz >= 10**3) & np.all(hz < 10**6):
                pre, div = 'K', 10**3
            elif np.all(hz >= 10**6) & np.all(hz < 10**9):
                pre, div = 'M', 10**6
            elif np.all(hz >= 10**9) & np.all(hz < 10**12):
                pre, div  = 'G', 10**9
            elif np.all(hz >= 10**12):
                pre, div = 'T', 10**12
            else:
                pre, div = '',1
            return(print(f'{round(hz/div,dec)} {pre}Hz'))
    else:
        print('\nConversion from {} to {} not yet implemented'.format(From,To))
        raise SystemExit('Please try again\n')
    global number
    print("Input 'q' to quit\n")
    while True:
        try:
            number = eval(input('{} to {}: '.format(From,To)))
        except NameError:
            print('Input not recogniced\n')
            continue
        except SyntaxError:
            print('Input not recogniced\n')
            continue
        if number == 'quit':
            # This could be done with raise
            print('Conversion stopped\n')
            break  
        else:
            converter(number)
            print('\n')
        continue

if __name__ == "__main__":
    import argparse
    import sys
    
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='''Convert between different units, actual python file contains functions,\nrunning in command line is easier for quick conversions.\n\n------------------------------------------------------------\n                    IMPLEMENTED COMMANDS                    \n------------------------------------------------------------\nair: wavelength in air\nvac: wavelength in vacuum\nwl:  vacuum below 2000 Å and above 20000 Å, air otherwise\nnr:  wavenumber\ninv: energy in inverse centimeters\nev:  energy in electronvolts\nhz:  frequency in Hertz, with support for different prefixes\n''')
        parser.add_argument("From", type=str, help="convert from, choose from implemented commands")
        parser.add_argument("To", type=str, help="convert to, choose from implemented commands")
        parser.add_argument("Dec", nargs='?', type=int, help="number of decimal places shown", default=3)
    
        args = parser.parse_args()
        answer = conversion(args.From,args.To,args.Dec)
