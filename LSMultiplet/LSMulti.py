"""
Created on 2020-04-27
author: Martin Montelius
This code is built to calculate the relative log gf values within a LS multiplet, according to the tables in 
"The theory of Atomic Structure and Spectra" Cowan 1981, ISBN 0-520-03821-5.
The formulas assume pure LS coupling.
The code doesn't actually do any atomic physics calculations, it only reads in the data from the tables and picks
out the correct values for the given transition.
All transitions from the books appendix 1 should be included.

Version 2.0
"""
import numpy as np
import pandas as pd

LS_table = pd.read_excel('LS_table.xlsx',index_col=0)
 
def Newgf(loggf2,gu1,gu2,perc_l,perc_u):
    '''Calculates log(gf) for a secondary line, given statistical weights and 
    the ratio between secondary/primary line Einstein coefficients
    loggf2: primary line log(gf
    gu1: secondary line statistical weight
    gu2: primary line statistical weight
    perc_l: secondary line percent strength
    perc_u: primary line percent strength'''
    return(np.log10((10**loggf2)*(gu1/gu2)*(perc_l/perc_u)))

def statW(j):
    '''Returns statistical weight, give j
    Follows formula g = 2j +1'''
    return(2*j+1)

def LSdecomp(LS):
    '''Returns L and S as numbers given a LS - term, 3D => triplet D => l, S = 2, 1'''
    #Assuming L and S defined as string in "3P" format, under/upper in LS()
    S, L = LS    
    #L values used in LS_table
    ls = np.array(['S','P','D','F','G','H'])
    #Check if given L exists and return numerical representation
    try:
        L = np.where(ls == L.upper())[0][0]
    except IndexError:
        print("Haven't implemented L higher than H, not in tables")
        return(None)
    #decodes the 3 in triplet to a 2S + 1 => S = 1 numerical value
    S = (float(S)-1)/2
    return(L,S)

def LS(loggf,under,over,Jlow,Jhigh,jlow,jhigh,rnd=3,perc_data=LS_table):
    '''Calculates the log(gf) value for a secondary line after a stronger line
    in the same LS-Multiplet has gotten its log(gf) measured astrophysically.
    Likely that if this code is needed that the multiplet lines are close and 
    can't be measured separately, meaning the measurement of the primary line
    is not perfect, and after applying this formula it needs to be readjusted.
    
    loggf:     Measured astyrophysical log(gf) of primary line
    under:     first LS term, given as the first line in VALD
    over:      second LS term, given as second line in VALD
    Jlow:      lower J value for primary line
    Jhigh:     upper J value for primary line
    jlow:      lower J value for secondary line
    jhigh:     upper J value for secondary line
    rnd:       amount of wanted decimal points
    perc_data: table with ratios of multiplet lines
    
    The default perc_data is LS_table, an excl file with ratios in percent that
    I have copyed by hand from "The Theory of Atomic Structure and Spectra" by
    Robert D. Cowan, Appendix 1, p. 694 - 701.'''
    #Proper formatting of inputs
    under = under.upper()
    over = over.upper()
    
    #Find the statistical weights for the levels. Put it in a seperate function if I need it elsewhere.
    J = np.array([Jlow,Jhigh,jlow,jhigh])
    Glow, Ghigh, glow, ghigh = statW(J)
    
    #Check LS coupling rules for the J-levels to check for mistakes with helpful errormessages
    if abs(Jhigh - Jlow) != 1:
        if Jhigh == 0 & Jlow == 0:
            return(f'Main {Jlow} - {Jhigh} breaks LS coupling, Delta J = 0 not allowed for 0 - 0')
        elif abs(Jhigh - Jlow) != 0:
            return(f'Main {Jlow} - {Jhigh} breaks LS coupling, allowed Delta J = 0 +- 1 ')
    if abs(jhigh - jlow) != 1:
        if (jhigh == 0) & (jlow == 0):
            return(f'Secondary {jlow} - {jhigh} breaks LS coupling, Delta J = 0 not allowed for 0 - 0')
        elif abs(jhigh - jlow) != 0:
            return(f'Secondary {jlow} - {jhigh} breaks LS coupling, allowed Delta J = 0, +- 1 ')
    
    #Find the correct set of relative Einstein coefficients
    #Decoding L into numbers to compare them
    lnr, Lnr = LSdecomp(under)[0], LSdecomp(over)[0]
    if (lnr == None) | (Lnr == None):
        return(None)
    #Tables only go one way, find if table needs to be flipped
    if lnr < Lnr:
        #No flip, ex 3P - 3D
        perc_u = perc_data.loc[perc_data.index==f'{under}{str(Jlow)}'][f'{over}{str(Jhigh)}'][0]
        perc_l = perc_data.loc[perc_data.index==f'{under}{str(jlow)}'][f'{over}{str(jhigh)}'][0]
    elif lnr == Lnr:
        #More complex for same L transitions, looking at secondary transition to find if flip is needed
        if (jlow < jhigh) | (jlow == jhigh):
            #No flip, ex 3P1 - 3P2
            perc_u = perc_data.loc[perc_data.index==f'{under}{str(Jlow)}'][f'{over}{str(Jhigh)}'][0]
            perc_l = perc_data.loc[perc_data.index==f'{under}{str(jlow)}'][f'{over}{str(jhigh)}'][0]
        else:
            #Flip needed, ex 3P2 - 3P1
            perc_u = perc_data.loc[perc_data.index==f'{over}{str(Jhigh)}'][f'{under}{str(Jlow)}'][0]
            perc_l = perc_data.loc[perc_data.index==f'{over}{str(jhigh)}'][f'{under}{str(jlow)}'][0]
    elif lnr > Lnr:
        #Flip needed, ex 3D - 3P
        perc_u = perc_data.loc[perc_data.index==f'{over}{str(Jhigh)}'][f'{under}{str(Jlow)}'][0]
        perc_l = perc_data.loc[perc_data.index==f'{over}{str(jhigh)}'][f'{under}{str(jlow)}'][0]
    
    #Check if a np.nan (no data in table) has snuck in
    if (np.isnan(perc_u)) | (np.isnan(perc_l)):
        return('Something about the given J levels breaks LS coupling')
    
    #Uses Newgf function to calculate log(gf) for secondary line
    return(np.round(Newgf(loggf, ghigh, Ghigh, perc_l, perc_u),rnd))
    
