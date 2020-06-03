"""
-----------------------------------------
Created on 2020-03-13
author: Martin Montelius
Version: 0.5
-----------------------------------------
Plan:
    Ok, så planen är att du ger åtminstånde två inputs i början: element och jämförelse. Kanske skippar att ge jämförelse som input.
    
    Element kan vara vilket som helst av de olika elementen eller en elementgrupp, alpha, odd, iron-peak eller neutron capture (fråga efter fler grupper). 

    Jämförelse parametern säger vad det ska plottas mot, kolumnerna ifall det är en grupplot. Jag tänker "optical", "Ivalu", "APOGEE", "all", "none",
    men också en specialare, "other", som promptar att du ger ett annat element som du plottar mot. Kanske kan implementera som ett "compare" kommando.

    Man kanske kan skriva nån kod som hittar rätt resultatfil, eller resultat filer för specifika linjer. Skriv det som ett update kommando. 
    
New in version 0.5:
    Fix for all comparisons:
        Comparison plots will now display the correct amount of IGRINS stars. This depends on 2MASS names, meaning that if there are more than one spectra 
        from the same star, it should turn up multiple times.
    Statistical information, mean and standard deviation compared to optical results, has implemented for abundance plots as well:
        The code is a bit janky, see it as a preliminary version, or rather as a "I don't know how to do this in a sensible way,
        and I will probably never fix it" version.
        For when there are multiple spectra for the same star, I have randomly selected one spectra, this is what's causing most of the trouble.
        This works for the element group plots as well.
        
Top priority:
    Create an all plots group with coloured backgrounds.
    Create a 'single' comparison command to plot only one set of results
    Diagnostics:
        Fit line to points
        Group diagnosing

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import socket
from PlotVariables import *
import PlotFunctions as pl

#Settings
AutoUpdate = False

###These are just the plotting parameters, so they become in this document
plt.rcParams['font.size']= 16
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.direction'], plt.rcParams['ytick.direction'] = 'in','in'
plt.rcParams['xtick.labelsize'] = plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['mathtext.fontset'] = 'cm'


#Check computer to get directories and names
Computer = socket.gethostname()
if  Computer == 'ValorToMe':
    ###Directories for my home computer
    resdir = '/Users/monte/OneDrive - Lund University/Uni/Master/Scripts/'
    homedir = '/Users/monte/OneDrive - Lund University/Uni/Master/Scripts/'
    plotdir = '/Users/monte/OneDrive - Lund University/Uni/Master/Scripts/PlotFolder/'
elif Computer == 'rap':
    ###Directories for rap
    resdir = '/home/martin/Analysis/smeresults/'
    homedir = '/home/martin/'
    plotdir = '/home/martin/AbundancePlots/'
else:
    print('Unfamiliar computer, please identify yourself by adding your directories to the code')


#Read in results files
if AutoUpdate == True:
    import glob
    import os
    ResFiles = glob.glob(resdir + 'result_H_val08*.txt') # * means all if need specific format then *.csv
    NewRes = max(ResFiles, key=os.path.getctime)
    print('Latest file:' + NewRes)
    IGRINS_RESULTS = pd.read_csv(NewRes, skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
else:
    IGRINS_RESULTS = pd.read_csv(resdir+'result_H_val08_k_20200527_161740.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
OPTICAL_RESULTS = pd.read_csv(resdir+'result_optical_start_H_si_update.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
OPTICAL_COMPLETE = pd.read_csv(resdir+'results_val08_all-correct.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
IVALU_DATA = pd.read_csv(homedir+'IVALU_Results.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
IVALU_RESULTS = IVALU_DATA[IVALU_DATA['2MASS'].isin(IGRINS_RESULTS['2MASS'].values)]
APOGEE_RESULTS = pd.read_csv(homedir+'APOGEE_DATA.txt',names=APOGEE_Header,delim_whitespace=True)


OPTICAL_DIF = IGRINS_RESULTS.drop(DROP_LIST, axis=1) - OPTICAL_RESULTS.drop(DROP_LIST, axis=1)


DATA = [IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE]

Comparison = 'ALL'
pl.Comp(Comparison)


OPTICAL_RESULTS.name = 'Optical'
OPTICAL_COMPLETE.name = 'OComplete'
IVALU_RESULTS.name = 'Ivalu'
IGRINS_RESULTS.name = 'Igrins'
APOGEE_RESULTS.name = 'Apogee'


while True:
    if diagFlag == False:
        pl.PickElement()
        element = pl.element
    if element == 'quit':
        print('Plotting stopped')
        break  
    elif (element in PlotInput) and (diagFlag == False):
        pl.PlotElement(element, DATA, plotdir)
        print('Plotted {}'.format(element))
    elif element == 'comp':
        pl.PickComp()
        Comparison = pl.Comparison
        pl.Comp(Comparison)
        CompleteFlag = pl.CompleteFlag
        CompCol = pl.CompCol
        continue
    elif (element in Diagnostics) or (diagFlag == True):
        print('\n Diagnosing...')
        if diagFlag == False:
            diag = element
        pl.PickElement()
        element = pl.element
        if element == 'quit':
            print('Diagnosing stopped')
            diagFlag = False
            break
        elif element == 'ALL':
            pl.DiagnoseAll(FinishedElements, diag, DATA, OPTICAL_DIF, plotdir)
        else:
            pl.PlotDiagnostics(element, diag, DATA, OPTICAL_DIF, plotdir)
        diagFlag = True
    elif element == 'update':
        import glob
        import os
        
        ResFiles = glob.glob(resdir + 'result_H_val08*.txt') # * means all if need specific format then *.csv
        NewRes = max(ResFiles, key=os.path.getctime)
        print('Latest file:' + NewRes)
        IGRINS_RESULTS = pd.read_csv(NewRes, skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
        DATA = [IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE]
        while True:
            try:
                ynq = eval(input('Update all plots? [y/n]: '))
            except NameError:
                print('Input not recogniced')
                continue   
            break
        if ynq == 'N':
            continue
        if ynq == 'ALL':
            pl.UpdateAll(Elements, DATA, plotdir+'test/')
            pl.UpdateAll(Groups, DATA, plotdir+'test/')
        else:
            pl.UpdateAll(FinishedElements, DATA, plotdir)
            pl.UpdateAll(Groups, DATA, plotdir)
        continue
    continue
