"""
-----------------------------------------
Created on 2020-03-13
author: Martin Montelius
Version: 0.3
-----------------------------------------
Plan:
    Ok, så planen är att du ger åtminstånde två inputs i början: element och jämförelse. Kanske skippar att ge jämförelse som input.
    
    Element kan vara vilket som helst av de olika elementen eller en elementgrupp, alpha, iron-peak eller neutron capture (fråga efter fler grupper). 

    Jämförelse parametern säger vad det ska plottas mot, kolumnerna ifall det är en grupplot. Jag tänker "optical", "Ivalu", "APOGEE", "all", "none",
    men också en specialare, "other", som promptar att du ger ett annat element som du plottar mot. Kanske kan implementera som ett "compare" kommando.

    Man kanske kan skriva nån kod som hittar rätt resultatfil, eller resultat filer för specifika linjer. Skriv det som ett update kommando,  
    
    Plan till diagnostic: ge input 'diagnostic' för allting, annars 'teff' 'logg' etc, sätt en if statement i PA som omdefinierar element till diagnostic
    och frågar efter en extra element input. Kör en "If element in PlotInput: pl.PlotElement, If element in Diagnostics: pl.PlotDiagnostics"

New in version 0.3:
    Renamed from PlotAbundances to PlotSME
    Complete optical sample implemented as background for the optical comparison, doesn't work on rap, rap still running 0.2.
    Implemented diagnostics, give "diag" as input to start comparison between IGRINS and optical results. Individual plots available.

Top priority:
    Get the name of the element on the plots.
    Create a all plots grop with coloured backgrounds.
    

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import socket
from PlotVariables import *
import PlotFunctions as pl

###These are just the plotting parameters, so they become in this document
plt.rcParams['font.size']= 16
plt.rcParams['xtick.minor.visible'], plt.rcParams['xtick.top'] = True,True
plt.rcParams['ytick.minor.visible'], plt.rcParams['ytick.right'] = True,True
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
IGRINS_RESULTS = pd.read_csv(resdir+'result_H_val08_ni_20200314_175239.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
OPTICAL_RESULTS = pd.read_csv(resdir+'result_optical_start_H_si_update.txt', skiprows=[0,1,2,6], delim_whitespace=True, names=SME_Header)
OPTICAL_COMPLETE = pd.read_csv(resdir+'results_val08_all-correct.txt', skiprows=[0,1,2,6], delim_whitespace=True, names=SME_Header)
IVALU_DATA = pd.read_csv(homedir+'IVALU_Results.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
IVALU_RESULTS = IVALU_DATA[IVALU_DATA['2MASS'].isin(IGRINS_RESULTS['2MASS'].values)]
APOGEE_RESULTS = pd.read_csv(homedir+'APOGEE_DATA.txt',names=APOGEE_Header,delim_whitespace=True)

OPTICAL_DIF = IGRINS_RESULTS.drop(columns=DROP_LIST) - OPTICAL_RESULTS.drop(columns=DROP_LIST)

DATA = [IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE]


while True:
    if diagFlag == False:
        pl.PickElement()
        element = pl.element
    if element == 'quit':
        print('Plotting stopped')
        break  
    elif (element in PlotInput) and (diagFlag == False):
        pl.PlotElement(element, DATA, plotdir)
        print('Plotted {el}'.format(el=element))
    elif (element in Diagnostics) or (diagFlag == True):
        print('\n Diagnosing...')
        if diagFlag == False:
            diag = element
        pl.PickElement()
        element = pl.element
        if element == 'quit':
            print('Diagnosing stopped')
            break
        pl.PlotDiagnostics(element, diag, DATA, OPTICAL_DIF, plotdir)
        diagFlag = True
    continue
