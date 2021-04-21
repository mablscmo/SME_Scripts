# -*- coding: utf-8 -*-
"""
-----------------------------------------
Created on 2020-12-19
author: Martin Montelius
Version: 0.2.0
-----------------------------------------
New in 0.2.0:
    Changed the code to use Brian's readlinelistfile function, much faster
    
    Implemented more commands to switch variables in interactive mode

To do:
    Write fine/hyperfine combination code, pretty sure we can do mixed hfs
    lines as long as they are from the same LS Multiplet, ex K lines
    
    Improve LS recognicion
"""

import numpy as np
import pandas as pd
from math import factorial as fac
from strength import strength

s, p, d, f, g, h = 'S', 'P', 'D', 'F', 'G', 'H'
S, P, D, F, G, H = 'S', 'P', 'D', 'F', 'G', 'H'

def Ldecomp(L):
    '''Returns L as a number. Need to write code that recognices other forms of L,
    if there's a problem try using manual()'''
    #L values used in LS_table
    ls = np.array(['S','P','D','F','G','H'])
    #Check if given L exists and return numerical representation
    try:
        L = np.where(ls == L.upper())[0][0]
    except IndexError:
        print("Haven't implemented L higher than H, not in tables.\n")
        return(None)
    return L


def Sdecomp(S):
    '''Returns S as a number'''
    return (float(S)-1)/2


def dabc(a,b,c):
    '''delta abc, equation 5.24 in Cowan'''
    return np.sqrt((fac(a+b-c)*fac(a-b+c)*fac(-a+b+c))/fac(a+b+c+1))


def j6(j1,j2,j3,l1,l2,l3):
    '''6-j formula, equation 5.23 in Cowan
    Could use wigner_6j from sympy.physics.wigner, but I wanted to understand what was going on.'''
    #equation 5.24
    deltas = dabc(j1,j2,j3)*dabc(j1,l2,l3)*dabc(l1,j2,l3)*dabc(l1,l2,j3)
    
    #factorial expressions in the denominator of 5.23
    facts = np.array([[-j1-j2-j3,-j1-l2-l3,-l1-j2-l3,-l1-l2-j3],[j1+j2+l1+l2,j2+j3+l2+l3,j3+j1+l3+l1]],dtype=object)
    #find larget and smallest factorial to constrain index k that is summed over
    smin = -np.min(facts[0])
    smax = np.min(facts[1])
    #list that is summed over, +1 as np.arange excludes edges
    s = np.arange(smin,smax+1)
    
    #the large sum in eq 5.23
    rhs = sum(((fac(i+1)*(-1)**i)/(fac(i-j1-j2-j3)*fac(i-j1-l2-l3)*fac(i-l1-j2-l3)*fac(i-l1-l2-j3)))*(1/(fac(j1+j2+l1+l2-i)*fac(j2+j3+l2+l3-i)*fac(j3+j1+l3+l1-i)))  for i in s)
    return deltas*rhs


def Dline2(S,L,J,S2,L2,J2):
    '''Calculates the (D_{line})^2 quantity from equation 14.50 in Cowan
    Will decode L and S if given as strings, ie. a ^3P_1 - ^3D_2 transition can be
    given as either Dline2(3,'P',1,3,'D',2) or Dline2(3,1,1,3,2,2)'''
    
    #Kronecker delta, formula not valid for S != S'
    if S != S2:
        print("S and S' needs to be the same, check your expression")
    
    #Optional S formatting, needs to be more advanced to handle L = X/2 etc
    if type(L) == str:
        L  = Ldecomp(L)
    if type(L2) == str:
        L2 = Ldecomp(L2)
    S  = Sdecomp(S)
    S2 = Sdecomp(S2)
    
    #Squared 6-j symbol from equation 14.50 in Cowan
    D6 = j6(L,S,J,J2,1,L2)**2
    #The [J,J'] term from same equation
    JJ = (J*2 + 1)*(J2*2 +1) 
    return D6*JJ


def Fline2(J,I,F,F2,J2):
    '''Calculates the relative strength of a hyperfine transition, formula taken
    from 2012A&A...545A..31H, called HÃ¶ln-Kronig rule
    Note only five terms in contrast to Dline2's six, this is because there is 
    no "I2" to check if the transition is allowed.'''
    
    #LS selection rule, only allowed transitions, delta F = 0, +-1, 0->0 not allowed
    if (abs(F-F2) > 1) | ((F == 0) & (F2 == 0)):
        return(None)
    
    #Squared 6-j symbol for HÃ¶ln-Kronig rule
    F6 = j6(J,I,F,F2,1,J2)**2
    #The [F,F'] term from same equation
    FF = (F*2 + 1)*(F2*2 +1)
    return F6*FF


def Newgf(loggf2,gu1,gu2,perc_l,perc_u):
    '''Calculates log(gf) for a secondary line, given statistical weights and 
    the ratio between secondary/primary line Einstein coefficients
    loggf2: primary line log(gf
    gu1: secondary line statistical weight
    gu2: primary line statistical weight
    perc_l: secondary line percent strength
    perc_u: primary line percent strength'''
    return np.log10((10**loggf2)*(gu1/gu2)*(perc_l/perc_u))


def statW(j):
    '''Returns statistical weight, give j
    Follows formula g = 2j +1'''
    return 2*j+1


def getI(element):
    '''Returns the nuclear spin of the most common isotope of the given element. 
    Numbers taken from Wikipedia, individual elements list of isotope pages.
    Implemented odd elements from Na to Cu'''
    data = pd.DataFrame({'I': [3/2,5/2,1/2,3/2,7/2,7/2,5/2,7/2,3/2],'A':[23,27,31,39,45,51,55,59,63]},index = ['Na','Al','P','K','Sc','V','Mn','Co','Cu'])
    return data.loc[data.index == f'{element}', 'I']


def manual(astr,S1,L1,S2,L2,Jlow,Jhigh,jlow,jhigh,prec = 3): 
    '''Manual alternative to the linelist searching algorithm in multiplet().
    Hopefully udeful for cases where the VALD configurations can't be decoded.
    astr: astrophysically measured log(gf) value
    S1, L1: first row of LS terms, eg ^3P -> S1 = 3, L1 = 'P', same for S2, L2
    Jlow, Jhigh: lower and upper J numbers for MEASURED line
    jlow, jhigh: lower and upper J numbers for CALCULATED line
    prec: number of decimals given'''
    primary_D2 = Dline2(S1, L1, Jlow, S2, L2, Jhigh)
    secondary_D2 = Dline2(S1, L1, jlow, S2, L2, jhigh)
    return round(Newgf(astr,statW(jhigh),statW(Jhigh),secondary_D2*100/primary_D2,100),3)


def multiplet(wl,gf,linelist,sec_width = 0.5,prime_width=0.005,guess=True):
    '''Takes wavelength and linelist, finds strongest line and possible secondaries.
    Returns the relative strengths of the secondary lines.
    
    Will attempt to recognice hyperfine structure lines: since no F values are
    given in VALD, relative strengths are calculated for all possible lines and
    are distributed to existing lines, assuming that their initial values have 
    correct relative distributions. Will warn and return None if the expected 
    and found lines do not match.
    
    sec_width: +- wl area where secondary lines are searched for
    prime_width: +- wl area where the primary line is searched for
    guess: experimental feature to estimate how wrong the formula is, as it 
        only adjusts one of the lines. So far it's limited to cases where
        new_gf > astr_gf
    '''
    
    #Attempt to find line, if multiple have exact same wavelength, take strongest
    primary = linelist.loc[(linelist['wlcent'] > wl - prime_width) & (linelist['wlcent'] < wl + prime_width)].reset_index(drop = True)
    
    if len(primary.index) == 0:
        print('Primary line not found')
        return None
    elif len(primary.index) > 1:
        #If multiple lines, use weak line approximation to find the strongest line
        primary = primary.iloc[strength(primary.gflog,primary.excit).idxmax()]
    else:
        #Reformatting if only one line is found to match other cases
        primary = primary.iloc[0]
    print(f'\nIdentified {primary.species} line as primary at {primary.wlcent} \n')
    
    #Search surrounding area for lines of same elementand ionisation stage
    secondary = linelist.loc[(linelist.species == primary.species) & (linelist.wlcent > primary.wlcent - sec_width) & (linelist.wlcent < primary.wlcent + sec_width)].copy()
    
    if len(secondary.index) == 1:
        print('Secondary lines not found\n')
        return None        
    elif (len(np.unique(secondary.LS1)) != 1) | (len(np.unique(secondary.LS2)) != 1):
        #Checks if LS terms are the same for all levels, if multiple multiplets
        #contribute, the contributions can't be calulated
        print('Mismatch between LS multiplets, lines not compatible\n')
    elif (len(np.unique(secondary.j_lo)) == 1) & (len(np.unique(secondary.j_up)) == 1):
        #Identified as hfs, multiple lines with same J values
        print('Attempting hfs analysis\n')
        #VALD formatting removal
        element = primary.species.split()[0]
        #Looks up the nuclear spin of the most common isotope
        I = getI(element)[0]
        #F values for lower and upper level
        F_low = np.arange(abs(I - primary.j_lo), I + primary.j_lo + 1)
        F_high = np.arange(abs(I - primary.j_up), I + primary.j_up + 1)
        
        #All allowed transitions between hyperfine structure lines
        hfs = [[i,j] for i in F_low for j in F_high if abs(i-j)<=1]
        if [0,0] in hfs: hfs.remove([0,0])
        if len(hfs) != len(secondary):
            #Problem with finding hfs line, needs to be same number as the F 
            #numbers are not known, need sort by gf to identify strong/weak
            if len(hfs) < len(secondary):
                print('Problem with finding hyperfine structure:\nExpected {} lines, found {}\nAttempting smaller search width of {} Ã…\n'.format(len(hfs),len(secondary),round(2*sec_width/3,2)))
                while True:
                    try:
                        sec_width = 2*sec_width/3
                        secondary = linelist.loc[(linelist.species == primary.species) & (linelist.wlcent > primary.wlcent - sec_width) & (linelist.wlcent < primary.wlcent + sec_width)]
                        if len(hfs) != len(secondary):
                            raise ValueError
                        else:
                            break
                    except ValueError:
                        print(f'Smaller search width failed, expected {len(hfs)} lines, found {len(secondary)}\n')
                        if sec_width < 0.1:
                            print('Minimum search width of 0.1 Ã… reached, check linelist and modify the search width accordingly\n')
                            return None
                        else:
                            continue
            else:
                print('Problem with finding hyperfine structure:\nExpected {} lines, found {}\nAttempting larger search width of {} Ã…\n'.format(len(hfs),len(secondary),round(4*sec_width/3,2)))
                while True:
                    try:
                        sec_width = 4*sec_width/3
                        secondary = linelist.loc[(linelist.species == primary.species) & (linelist.wlcent > primary.wlcent - sec_width) & (linelist.wlcent < primary.wlcent + sec_width)]
                        if len(hfs) != len(secondary):
                            raise ValueError
                        else:
                            break
                    except ValueError:
                        print(f'Larger search width failed, expected {len(hfs)} lines, found {len(secondary)}\n')
                        if sec_width > 2:
                            print('Maximum search width of 2 Ã… reached, check linelist and modify the search width accordingly\n')
                            return None
                        else:
                            continue                
        
        #All lines relative strength
        sec_F2 = [Fline2(primary.j_up, I, hfs[i][1], hfs[i][0], primary.j_lo) for i in range(len(hfs))]
        
        #Primary lines strength
        prime_A = np.max(sec_F2)
            
        #Sorts lines to get same strength distribution as previously
        secondary = secondary.sort_values('gflog')
        secondary['percent'] = np.sort(sec_F2/prime_A)*100
        secondary = secondary.sort_index()
        #Finds new log(gf) values for all lines based on astrophysical measurement
        secondary['new_gf'] = secondary.apply(lambda line: Newgf(gf,statW(line.j_up),statW(primary.j_up),line.percent,100),axis=1)
        if guess == True:
            #Ratio of primary to all secondaries
            ratio = prime_A/np.sum(sec_F2)
            #My guess_gf algorithm, adjust more when secondaries are weak and vice versa
            guess_gf = gf - (1 - ratio) * (gf - secondary.gflog.max())
            secondary['guess_gf'] = secondary.apply(lambda line: Newgf(guess_gf,statW(line.j_up),statW(primary.j_up),line.percent,100),axis=1)
            return secondary[['wlcent','gflog','new_gf','guess_gf']]
        else:
            return secondary[['wlcent','gflog','new_gf']]
    else: 
        #Assuming fine structure multiplet
        #Primary lines strength
        main_D2 = Dline2(primary.LS1[0], primary.LS1[1], primary.j_lo, primary.LS2[0], primary.LS2[1], primary.j_up)
        
        #Relative strengths
        secondary['percent'] = secondary.apply(lambda line: 100*Dline2(line.LS1[0],line.LS1[1],line.j_lo,line.LS2[0],line.LS2[1],line.j_up)/main_D2,axis=1)
        
        #New log(gf) values for secondary lines based on astrophysical measurement
        secondary['new_gf'] = secondary.apply(lambda line: Newgf(gf,statW(line.j_up),statW(primary.j_up),line.percent,100),axis=1)
        
        #Rescale measured gf value to sum of all lines
        if guess == True:
            #Finds relative strengths for all lines
            sec_D2 = secondary.apply(lambda line: Dline2(line.LS1[0],line.LS1[1],line.j_lo,line.LS2[0],line.LS2[1],line.j_up),axis=1).sum()
            #Ratio of primary to all secondaries (includes itself now)
            ratio = main_D2/sec_D2
            #My guess_gf algorithm, adjust more when secondaries are weak and vice versa
            guess_gf = gf - (1 - ratio) * (gf - primary.gflog)
            secondary['guess_gf'] = secondary.apply(lambda line: Newgf(guess_gf,statW(line.j_up),statW(primary.j_up),line.percent,100),axis=1)
            return secondary[['wlcent','gflog','new_gf','guess_gf']]
        else:
            return secondary[['wlcent','gflog','new_gf']]

if __name__ == "__main__":
    #Change to match linelist names and directories, socket part and if statement 
    #only necessary if the code will be run on multiple systems
    import sys
    import socket
    Computer = socket.gethostname()
    if  (Computer == 'ValorToMe') | (Computer == 'SQWAAK2'):
        ###Directories for my home computer
        LL_dir = '/Users/monte/OneDrive - Lund University/Uni/Master/LineList_Copies/'
        LL_name = 'VALD_nomols_20200123.dat'
        # LL_name = 'test.dat'
    elif (Computer == 'rap') | (Computer == 'fedtmule'):
        ###Directories for rap and fedtmule
        LL_dir = '/home/martin/Linelists/'
        LL_name = 'VALD_nomols_20200123.dat'
    
    #Importing my linelist reader from LineListReader.py, can use another version as long as multiplet() is modified to match the column names
    from llreader import llreader
    ll = llreader(LL_name,LL_dir)

    while True:
        #Checks if arguments have been passed from the command line
        if len(sys.argv) > 1:
            import argparse
            parser = argparse.ArgumentParser(description='''Python code to assist in measuring astrophysical log(gf) values of merged fine or hyperfine structure lines. For lines that are too close to measure individually, this code lets you measure the whole line and calculate what the log(gf) values of the components should be.\nRunning the code from the command line lets you give wavelength and astrophysically measured log(gf) value for the strongest component line as either arguments or input once the code is running.''')
            parser.add_argument("s_line", type=float, help="wavelength of primary line in Ã…ngstrÃ¶m")
            parser.add_argument("gf_astr", type=float, help="log(gf) of primary line")
            parser.add_argument("guess_flag", nargs='?', type=bool, help="calculate corrected log(gf) value based on previous value", default=True)
            args = parser.parse_args()
            s_line, gf_astr, guess_flag = args.s_line, args.gf_astr, args.guess_flag
        else:
        #Manual input of lines, needs to be reset after saving the linelist
            s_line = input('Wavelength: ')
            if s_line in ['n','N','no','No','NO']:
                print('\nGuessing how gf should be adjusted: False\n')
                guess_flag = False
                continue
            elif s_line in ['y','Y','yes','Yes','YES']:
                print('\nGuessing how gf should be adjusted: True\n')
                guess_flag = True
                continue
            elif s_line in ['u','U','update']:
                print('\nUpdating linelist...\n')
                try:
                  ll = llreader(LL_name,LL_dir)
                except Exception as e:
                  print(f'\nProblem with loading the new linelist:\n{e}\n')
                  continue
                print('\nSuccessful update.\n')
                continue
            else:
                guess_flag = True
            if s_line in ['q','Q','quit','Quit','QUIT','exit','Exit','EXIT']:
                print('\nClosing LSMultiplet..\n')
                break
            else:
                try:
                    s_line = float(s_line)
                except ValueError:
                    print('\n ERROR: input not recogniced as a number, try again\n')
                    continue
            try:
                gf_astr = float(input('Astrophysical log(gf): '))
            except ValueError:
                print('\n ERROR: input not recogniced as a number, try again\n')
                continue
            
        LSMult = multiplet(wl = s_line, gf = gf_astr, linelist = ll, guess = guess_flag)
        if LSMult is None:
            #When multiplet() finds an error it returns None and hopefully its own error message
            if len(sys.argv) > 1:
                break
            else:
                continue
        elif guess_flag:
            print('\nWavelength   old log(gf)     new log(gf)     guess log(gf)\n')
            for i in range(len(LSMult)):
                sec_line = LSMult.iloc[i]
                print('{0: <10}{1:>11}    -->{2:>9}     -->{3:>9}\n'.format(format(sec_line.wlcent,'.4f'),format(sec_line.gflog,'.3f'),format(sec_line.new_gf,'.3f'),format(sec_line.guess_gf,'.3f')))
            if len(sys.argv) > 1:
                break            
        else:
            print('\nWavelength   old log(gf)     new log(gf)\n')
            for i in range(len(LSMult)):
                sec_line = LSMult.iloc[i]
                print('{0: <10}{1:>11}    -->{2:>9}\n'.format(format(sec_line.wlcent,'.4f'),format(sec_line.gflog,'.3f'),format(sec_line.new_gf,'.3f')))
            if len(sys.argv) > 1:
                break
