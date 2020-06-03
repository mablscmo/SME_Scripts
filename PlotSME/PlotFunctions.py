"""
-----------------------------------------
Created on 2020-03-22
author: Martin Montelius
Version: 0.5

Updated: tried implementing a list function for the comparison input, not trialled yet
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
        try:
            CSplit = Comparison.split()
        except ValueError:
            CSplit = list(Comparison)
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
    BoxProps = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    StatFlag = False
    plt.ioff()
    NCol = len(CompCol)
    if element in Elements:
        fig, ax = plt.subplots(1, NCol, figsize=(7*NCol, 5))
        for i in range(NCol):
            if DATA[CompCol[i]+1].name == 'Optical':
                DIF_DATA = IGRINS_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values
                StatFlag = True
            elif DATA[CompCol[i]+1].name == 'Ivalu':
                OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(IVALU_RESULTS['2MASS'].values)]
                if len(OPTICAL_RESULTS) != len(IVALU_RESULTS):
                    OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])
                DIF_DATA = IVALU_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values
                StatFlag = True
            elif DATA[CompCol[i]+1].name == 'Apogee':
                OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(APOGEE_RESULTS['2MASS'].values)]
                if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                    APOGEE_RESULTS = APOGEE_RESULTS.drop([2,4])
                    if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                        OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])                
                DIF_DATA = APOGEE_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(element)].values
                StatFlag = True

            if CompleteFlag == True:
                ax[i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(element)].values,'.',color='silver',label='Complete optical')
            ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim([-2,1])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel('[Fe/H]')
            ax[i].plot(IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['[Fe/H]'].values,IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['{}'.format(element)].values,'.',color='black',label='IGRINS')
            ax[i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(element)].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
            if StatFlag == True:
                mean, std = round(DIF_DATA.mean(),3), round(DIF_DATA.std(),3)
                StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
                ax[i].text(0.95, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', horizontalalignment='right', bbox=BoxProps, transform=ax[i].transAxes)
            ax[i].legend(loc='lower left',fancybox=True, numpoints=1, framealpha=0.5) 
        ax[0].set_ylabel('[{}/Fe]'.format(element))
        if Naming == True:
            ax[NCol-1].text(0.96,0.95,element,fontsize=25, verticalalignment='top', horizontalalignment='right', bbox=BoxProps, transform=ax[NCol-1].transAxes)

    if element == 'Alpha':
        fig, ax = plt.subplots(len(AlphaElements), NCol, figsize=(7*NCol, len(AlphaElements)*4))
        
        for row in range(len(AlphaElements)):
            
            for i in range(NCol):
                IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
                if DATA[CompCol[i]+1].name == 'Optical':
                    DIF_DATA = IGRINS_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Ivalu':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(IVALU_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(IVALU_RESULTS):
                        OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])
                    DIF_DATA = IVALU_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Apogee':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(APOGEE_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                        APOGEE_RESULTS = APOGEE_RESULTS.drop([2,4])
                        if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                            OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])                
                    DIF_DATA = APOGEE_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(AlphaElements[row])].values
                    StatFlag = True
                    
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(AlphaElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['[Fe/H]'].values,IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['{}'.format(AlphaElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(AlphaElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                if StatFlag == True:
                    mean, std = round(DIF_DATA.mean(),3), round(DIF_DATA.std(),3)
                    StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
                    ax[row,i].text(0.95, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', horizontalalignment='right', bbox=BoxProps, transform=ax[row,i].transAxes)
                
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(AlphaElements[row]))
            if Naming == True:
                ax[row,NCol-1].text(0.973,0.95,AlphaElements[row],fontsize=25, verticalalignment='top', horizontalalignment='right', bbox=BoxProps, transform=ax[row,NCol-1].transAxes)
    if element == 'Odd':
        fig, ax = plt.subplots(len(OddElements), NCol, figsize=(7*NCol, len(OddElements)*4))
        for row in range(len(OddElements)):
            
            for i in range(NCol):
                IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
                if DATA[CompCol[i]+1].name == 'Optical':
                    DIF_DATA = IGRINS_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Ivalu':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(IVALU_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(IVALU_RESULTS):
                        OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])
                    DIF_DATA = IVALU_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Apogee':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(APOGEE_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                        APOGEE_RESULTS = APOGEE_RESULTS.drop([2,4])
                        if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                            OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])                
                    DIF_DATA = APOGEE_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(OddElements[row])].values
                    StatFlag = True
                    
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(OddElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['[Fe/H]'].values,IGRINS_RESULTS[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])]['{}'.format(OddElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[CompCol[i]+1]['[Fe/H]'].values,DATA[CompCol[i]+1]['{}'.format(OddElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                if StatFlag == True:
                    mean, std = round(DIF_DATA.mean(),3), round(DIF_DATA.std(),3)
                    StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
                    ax[row,i].text(0.95, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', horizontalalignment='right', bbox=BoxProps, transform=ax[row,i].transAxes)
                                
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(OddElements[row]))
            if Naming == True:
                ax[row,NCol-1].text(0.973,0.95,OddElements[row], fontsize=25, verticalalignment='top', horizontalalignment='right', bbox=BoxProps, transform=ax[row,NCol-1].transAxes)

    #Need to measure more iron-peak elements before this code works
    if element == 'Iron_peak':
        fig, ax = plt.subplots(len(IronElements), NCol, figsize=(7*NCol, len(IronElements)*4))
        for row in range(len(IronElements)):
            for i in range(NCol):
                IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
                if DATA[CompCol[i]+1].name == 'Optical':
                    DIF_DATA = IGRINS_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Ivalu':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(IVALU_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(IVALU_RESULTS):
                        OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])
                    DIF_DATA = IVALU_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Apogee':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(APOGEE_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                        APOGEE_RESULTS = APOGEE_RESULTS.drop([2,4])
                        if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                            OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])                
                    DIF_DATA = APOGEE_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(IronElements[row])].values
                    StatFlag = True                
                
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=IronElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(IronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])][CompCol[i]+1]['[Fe/H]'].values,DATA[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])][CompCol[i]+1]['{}'.format(IronElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                if StatFlag == True:
                    mean, std = round(DIF_DATA.mean(),3), round(DIF_DATA.std(),3)
                    StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
                    ax[row,i].text(0.95, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', horizontalalignment='right', bbox=BoxProps, transform=ax[row,i].transAxes)
                                
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(IronElements[row]))
            if Naming == True:
                ax[row,NCol-1].text(0.973,0.95,IronElements[row], fontsize=25, verticalalignment='top', horizontalalignment='right', bbox=BoxProps, transform=ax[row,NCol-1].transAxes)
        
    #Need to measure more neutron-capture elements before this code works
    if element == 'Neutron_capture':
        fig, ax = plt.subplots(len(NeutronElements), NCol, figsize=(7*NCol, len(NeutronElements)*4))
        for row in range(len(NeutronElements)):
            for i in range(NCol):
                IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
                if DATA[CompCol[i]+1].name == 'Optical':
                    DIF_DATA = IGRINS_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Ivalu':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(IVALU_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(IVALU_RESULTS):
                        OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])
                    DIF_DATA = IVALU_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values
                    StatFlag = True
                elif DATA[CompCol[i]+1].name == 'Apogee':
                    OPTICAL_RESULTS = OPTICAL_RESULTS[OPTICAL_RESULTS['2MASS'].isin(APOGEE_RESULTS['2MASS'].values)]
                    if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                        APOGEE_RESULTS = APOGEE_RESULTS.drop([2,4])
                        if len(OPTICAL_RESULTS) != len(APOGEE_RESULTS):
                            OPTICAL_RESULTS = OPTICAL_RESULTS.drop([3])                
                    DIF_DATA = APOGEE_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values - OPTICAL_RESULTS.sort_values(by='2MASS')['{}'.format(NeutronElements[row])].values
                    StatFlag = True                
                
                if CompleteFlag == True:
                    ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{}'.format(NeutronElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{}'.format(NeutronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])][CompCol[i]+1]['[Fe/H]'].values,DATA[IGRINS_RESULTS['2MASS'].isin(DATA[CompCol[i]+1]['2MASS'])][CompCol[i]+1]['{}'.format(NeutronElements[row])].values,'.',color=Colours[CompCol[i]],alpha=0.75,label=CompLabel[CompCol[i]])
                if StatFlag == True:
                    mean, std = round(DIF_DATA.mean(),3), round(DIF_DATA.std(),3)
                    StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
                    ax[row,i].text(0.95, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', horizontalalignment='right', bbox=BoxProps, transform=ax[row,i].transAxes)
                                
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{}/Fe]'.format(NeutronElements[row]))
            if Naming == True:
                ax[row,NCol-1].text(0.973,0.95,NeutronElements[row], fontsize=25, verticalalignment='top', horizontalalignment='right', bbox=BoxProps, transform=ax[row,NCol-1].transAxes)
            
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
        mean, std = round(DIF_DATA['{}'.format(element)].mean(),3), round(DIF_DATA['{}'.format(element)].std(),3)
        StatInfo = r'$\mu$={}  $\sigma$={}'.format(mean,std)
        BoxProps = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        fig, ax = plt.subplots(1, 4, figsize=(26, 5))
        if Naming == True:
            ax[3].text(0.96,0.95,element, fontsize=25, verticalalignment='top', horizontalalignment='right',bbox=BoxProps, transform=ax[3].transAxes)
        for i in range(4):
            # ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim(DiagLimits[i])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel(Diagnostics[i+1])
            ax[i].plot(IGRINS_RESULTS[Diagnostics[i+1]].values,DIF_DATA['{}'.format(element)].values,'.',markersize=10,color=DiagColours[i])
            ax[i].text(0.05, 0.05, StatInfo, fontsize=14, verticalalignment='bottom', bbox=BoxProps, transform=ax[i].transAxes)
        ax[0].set_ylabel('IGRINS-OPTICAL')
        plt.tight_layout()
        try:
            plt.savefig(plotdir+diag+'_'+element+'.pdf',dpi=500)   
        except PermissionError:
            print("File is already opened somewhere, you need to close it before you can save.")

        plt.draw()
        plt.show()
    elif diag == 'Teff':
        i = 0
    elif diag == 'logg':
        i = 1
    elif diag == '[Fe/H]':
        i = 2
    elif diag == 'vmic':
        i = 3
    if diag != 'diagnostics':
        plt.figure(figsize=(9,5))
        # ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
        plt.axhline(0,0,1, color='0.75', linestyle='dashed')
        plt.xlim(DiagLimits[i])
        plt.ylim([-1,1])
        plt.xlabel(Diagnostics[i+1])
        plt.ylabel('IGRINS-OPTICAL')
        plt.plot(IGRINS_RESULTS[Diagnostics[i+1]].values,DIF_DATA['{}'.format(element)].values,'.',markersize=10,color=DiagColours[i])
        plt.tight_layout()
        try:
            plt.savefig(plotdir+diag+'_'+element+'.pdf',dpi=500)   
        except PermissionError:
            print("File is already opened somewhere, you need to close it before you can save.")
        plt.draw()
        plt.show()

def UpdateAll(FinishedElements, DATA, plotdir):
    for i in FinishedElements:
        print('Plotting {}...'.format(i))
        try:
            PlotElement(i, DATA, plotdir)
        except KeyError:
            print('Problem with ' + i)
        except IndexError:
            print('No data for ' + i)
def DiagnoseAll(FinishedElements, diag, DATA, DIF_DATA, plotdir):
    for i in FinishedElements:
        print('Diagnosing {}...'.format(i))
        PlotDiagnostics(i, diag, DATA, DIF_DATA, plotdir)
 
