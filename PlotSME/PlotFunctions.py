"""
-----------------------------------------
Created on 2020-03-22
author: Martin Montelius
Version: 0.3.2
-----------------------------------------
Functions for the PlotAbundances code
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
    
def PlotInternal(subject,row,rows):
    if rows == 1:
        for i in range(3):
            ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim([-2,1])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel('[Fe/H]')
            ax[i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=subject)].values,'.',color='crimson',label='IGRINS')
            ax[i].plot(Comparison[i]['[Fe/H]'].values,Comparison[i]['{el}'.format(el=subject)].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
            ax[i].legend(loc='lower left',fancybox=True, numpoints=1)    
    else:
        for i in range(3):
            ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[row,i].set_xlim([-2,1])
            ax[row,i].set_ylim([-1,1])
            ax[row,i].set_xlabel('[Fe/H]')
            ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=subject)].values,'.',color='crimson',label='IGRINS')
            ax[row,i].plot(Comparison[i]['[Fe/H]'].values,Comparison[i]['{el}'.format(el=subject)].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
            ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1)         

def PlotElement(element, DATA, plotdir):
    IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS, OPTICAL_COMPLETE = DATA
    plt.ioff()
    if element in Elements:
        fig, ax = plt.subplots(1, 3, figsize=(21, 5))
       
        for i in range(3):
            ax[i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=element)].values,'.',color='silver',label='Complete optical')
            ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim([-2,1])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel('[Fe/H]')
            ax[i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=element)].values,'.',color='black',label='IGRINS')
            ax[i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=element)].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
            ax[i].legend(loc='lower left',fancybox=True, numpoints=1) 
        ax[0].set_ylabel('[{ele}/Fe]'.format(ele=element))
        plt.tight_layout()
        plt.savefig(plotdir+'abundances_'+element+'.pdf',dpi=500)   
        plt.draw()
        plt.show()
        
    if element == 'Alpha':
        fig, ax = plt.subplots(len(AlphaElements), 3, figsize=(21, len(AlphaElements)*4))
        for row in range(len(AlphaElements)):
            
            for i in range(3):
                ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=AlphaElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=AlphaElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=AlphaElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=AlphaElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+'abundances_'+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()
        
    if element == 'Odd':
        fig, ax = plt.subplots(len(OddElements), 3, figsize=(21, len(OddElements)*4))
        for row in range(len(OddElements)):
            
            for i in range(3):
                ax[row,i].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=OddElements[row])].values,'.',color='silver',label='Complete optical')
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=OddElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=OddElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=OddElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+'abundances_'+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()
         
    #Need to measure more iron-peak elements before this code works
    if element == 'Iron_peak':
        fig, ax = plt.subplots(len(IronElements), 3, figsize=(21, len(IronElements)*4))
        for row in range(len(IronElements)):
            ax[0].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=IronElements[row])].values,'.',color='silver',label='Complete optical')
            for i in range(3):
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=IronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=IronElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=IronElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()
        
    #Need to measure more neutron-capture elements before this code works
    if element == 'Neutron_capture':
        fig, ax = plt.subplots(len(NeutronElements), 3, figsize=(21, len(NeutronElements)*4))
        for row in range(len(NeutronElements)):
            ax[0].plot(OPTICAL_COMPLETE['[Fe/H]'].values,OPTICAL_COMPLETE['{el}'.format(el=NeutronElements[row])].values,'.',color='silver',label='Complete optical')
            for i in range(3):
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=NeutronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=NeutronElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True, numpoints=1) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=NeutronElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)
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
            ax[i].plot(IGRINS_RESULTS[Diagnostics[i+1]].values,DIF_DATA['{el}'.format(el=element)].values,'.',markersize=10,color=DiagColours[i])
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

