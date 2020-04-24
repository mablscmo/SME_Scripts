"""
-----------------------------------------
Created on 2020-03-22
author: Martin Montelius
Version: 0.4
-----------------------------------------
Functions for the PlotSME code
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PlotVariables import *



def PickElement():
    global element
    while True:
        try:
                element = eval(input('Input element (q to quit): '))
        except NameError:
            print('Element not recogniced, check spelling or edit the code if we got a new element')
            continue
        break
    if element in PlotInput:
        print('Plotting {ele}...\n'.format(ele=element))
        
def Comp(Comparison):
    global CompCol, CompleteFlag
    if Comparison == 'ALL':
        print('Plotting comparisons to all datasets')
    else:
        CSplit = Comparison.split()
        try:
            if 'O' not in CSplit:
                CompCol.remove(0)
                print("Not comparing to optical data")
            if 'I' not in CSplit:
                CompCol.remove(1)
                print("Not comparing to Ivalu's data")            
            if 'A' not in CSplit:
                CompCol.remove(2)
                print("Not comparing to APOGEE data")
            if 'C' not in CSplit:
                CompleteFlag = False
                print("Not comparing to complete optical data")
        except ValueError:
            print('Something went wrong with the comparison, might want to try again')
    
def PickComp():
    global Comparison
    while True:
        try:
            print("Available comparisons:\n Optical 'O'\n Ivalu 'I'\n APOGEE 'A'\n Complete optical 'C'\n All 'ALL'")
            
            Comparison = input('Comparisons (whitespace separation): ').upper()
        except NameError:
            print('Input not recogniced')
            continue
        break



def PlotElement(element, DATA, plotdir, CompleteFlag=CompleteFlag, CompCol=CompCol):
    IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
    plt.ioff()
    NCol = len(CompCol)
    if element in Elements:
        fig, ax = plt.subplots(1, NCol, figsize=(7*NCol, 5))
        for i in range(NCol):
            if CompleteFlag == True:
                ax[i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(element)].values,'.',color='silver',label='Complete optical')
            ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim([-2,1])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel('[Fe/H]')
            ax[i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(element)].values,'.',color='black',label='IGRINS')
            ax[i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(element)].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
            ax[i].legend(loc='lower left',fancybox=True, numpoints=1) 
        ax[0].set_ylabel('[{}/Fe]'.format(element))
        
    if element == 'Alpha':
        fig, ax = plt.subplots(len(AlphaElements), NCol, figsize=(7*NCol, len(AlphaElements)*4))
        for row in range(len(AlphaElements)):
            
            for i in range(NCol):
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(AlphaElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(AlphaElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(AlphaElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(AlphaElements[row]))   
        
    if element == 'Odd':
        fig, ax = plt.subplots(len(OddElements), NCol, figsize=(7*NCol, len(OddElements)*4))
        for row in range(len(OddElements)):
            
            for i in range(NCol):
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(OddElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(OddElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(OddElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(OddElements[row]))   

    #Need to measure more iron-peak elements before this code works
    if element == 'Iron_peak':
        fig, ax = plt.subplots(len(IronElements), NCol, figsize=(7*NCol, len(IronElements)*4))
        for row in range(len(IronElements)):
            for i in range(NCol):
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=IronElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(IronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(IronElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(IronElements[row]))   
        
    #Need to measure more neutron-capture elements before this code works
    if element == 'Neutron_capture':
        fig, ax = plt.subplots(len(NeutronElements), NCol, figsize=(7*NCol, len(NeutronElements)*4))
        for row in range(len(NeutronElements)):
            for i in range(NCol):
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(NeutronElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(NeutronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(NeutronElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(NeutronElements[row]))   
            
    #Formatting and saving the figure
    plt.tight_layout()
    try:
        plt.savefig(plotdir+'abundances_'+element+'.pdf',dpi=500)
    except PermissionError:
            print("File is already opened somewhere, you need to close it before you can save.")
    plt.draw()
    plt.show()


    

def PlotDiagnostics(element, diag, DATA, DIF_DATA, plotdir):
    IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
    
    plt.ioff()
    
    if diag == 'diagnostics':
        fig, ax = plt.subplots(1, 4, figsize=(26, 5))
        for i in range(4):
            # ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim(DiagLimits[i])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel(Diagnostics[i+1])
            ax[i].plot(IGRINS_RESULTS[Diagnostics[i+1]].values,DIF_DATA['{}'.format(element)].values,'.',markersize=10,color=DiagColours[i])
        ax[0].set_ylabel(r'[{ele}/Fe]$_{{IGRINS}}$-[{ele}/Fe]$_{{OPTICAL}}$'.format(ele=element))
        plt.tight_layout()
        plt.savefig(plotdir+diag+'_'+element+'.pdf',dpi=500)   
        plt.draw()
        plt.show()
    elif diag == 'Teff':
        i = 0
    elif diag == 'logg':
        i = 1
    elif diag == 'vmic':
        i = 2
    elif diag == '[Fe/H]':
        i = 3
    if diag != 'diagnostics':
        plt.figure(figsize=(9,5))
        # ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
        plt.axhline(0,0,1, color='0.75', linestyle='dashed')
        plt.xlim(DiagLimits[i])
        plt.ylim([-1,1])
        plt.xlabel(Diagnostics[i+1])
        plt.ylabel(r'[{ele}/Fe]$_{{IGRINS}}$-[{ele}/Fe]$_{{OPTICAL}}$'.format(ele=element))
        plt.plot(IGRINS_RESULTS[Diagnostics[i+1]].values,DIF_DATA['{el}'.format(el=element)].values,'.',markersize=10,color=DiagColours[i])
        plt.tight_layout()
        plt.savefig(plotdir+diag+'_'+element+'.pdf',dpi=500)   
        plt.draw()
        plt.show()

