"""
-----------------------------------------
Created on 2020-03-13
author: Martin Montelius
Version: 0.4.1
-----------------------------------------
Plan:
    Ok, så planen är att du ger åtminstånde två inputs i början: element och jämförelse. Kanske skippar att ge jämförelse som input.
    
    Element kan vara vilket som helst av de olika elementen eller en elementgrupp, alpha, odd, iron-peak eller neutron capture (fråga efter fler grupper). 

    Jämförelse parametern säger vad det ska plottas mot, kolumnerna ifall det är en grupplot. Jag tänker "optical", "Ivalu", "APOGEE", "all", "none",
    men också en specialare, "other", som promptar att du ger ett annat element som du plottar mot. Kanske kan implementera som ett "compare" kommando.

    Man kanske kan skriva nån kod som hittar rätt resultatfil, eller resultat filer för specifika linjer. Skriv det som ett update kommando,  
    
New in version 0.4:
    A tentative implementation of choosing what to compare to is implemented:
        Give 'comp' as a command to see options and choose which datasets should be compared to. 
        So far the code only works when at least 2 different comparisons are made. 
        You can change the comparison from the Comparison parameter to not have to do it every time.
        You can only change comparison once via the comp command.
    
    Improvements in PlotFunctions: 
        A figure failing to save will now not crash the code.
        General cleanup and improvements.
    
    Provisional update feature added: 
        The new 'update' command checks for new resultfiles and will use that file for plotting.
        The command won't change the file permanently, maybe in another version?
    
    0.4.1
    Improvements and statistical imformation for diagnosticsplots.
    Name of element now displayed on the plots, aside from on the y-axis, control via Naming parameter in PlotVariables.
    Created UpdateAll and DiagnoseAll subroutines:
        Update all figures with the 'update' command, simply say yes to updating everything. NB: Also updates all groups. 
        For an element to be updated, add it to the FinishedElements list, or try the 'ALL' command (not advised).
        
        Diagnose all is accessed by typing ALL as element when diagnosing. NB: Groups are not diagnosed at the moment.
        
    Known problems:
        Plot formatting on rap is wonky, the legend is way too big. Will look into it.
        
Top priority:
    Create an all plots group with coloured backgrounds.
    Diagnostics:
        Calculate mean shift and standard deviation
        Fit line to points
        Group diagnosing
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import socket
from PlotVariables import *
import PlotFunctions as pl

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
IGRINS_RESULTS = pd.read_csv(resdir+'result_H_val08_na_20200324_232448.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
OPTICAL_RESULTS = pd.read_csv(resdir+'result_optical_start_H_si_update.txt', skiprows=[0,1,2,6], delim_whitespace=True, names=SME_Header)
OPTICAL_COMPLETE = pd.read_csv(resdir+'results_val08_all-correct.txt', skiprows=[0,1,2,6], delim_whitespace=True, names=SME_Header)
IVALU_DATA = pd.read_csv(homedir+'IVALU_Results.txt', skiprows=[0,1,2], delim_whitespace=True, names=SME_Header)
IVALU_RESULTS = IVALU_DATA[IVALU_DATA['2MASS'].isin(IGRINS_RESULTS['2MASS'].values)]
APOGEE_RESULTS = pd.read_csv(homedir+'APOGEE_DATA.txt',names=APOGEE_Header,delim_whitespace=True)


OPTICAL_DIF = IGRINS_RESULTS.drop(DROP_LIST, axis=1) - OPTICAL_RESULTS.drop(DROP_LIST, axis=1)

DATA = [IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE]

Comparison = 'ALL'
pl.Comp(Comparison)


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
            pl.UpdateAll(Groups, DATA, plotdir)            
        else:
            pl.UpdateAll(FinishedElements, DATA, plotdir)
            pl.UpdateAll(Groups, DATA, plotdir)
        continue
    continue
