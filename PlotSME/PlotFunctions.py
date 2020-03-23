"""
-----------------------------------------
Created on 2020-03-22
author: Martin Montelius
Version: 0.1
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
            ax[i].legend(loc='lower left',fancybox=True)    
    else:
        for i in range(3):
            ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[row,i].set_xlim([-2,1])
            ax[row,i].set_ylim([-1,1])
            ax[row,i].set_xlabel('[Fe/H]')
            ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=subject)].values,'.',color='crimson',label='IGRINS')
            ax[row,i].plot(Comparison[i]['[Fe/H]'].values,Comparison[i]['{el}'.format(el=subject)].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
            ax[row,i].legend(loc='lower left',fancybox=True)         

def PlotElement(element, DATA, plotdir):
    IGRINS_RESULTS, OPTICAL_RESULTS, IVALU_RESULTS, APOGEE_RESULTS = DATA
    plt.ioff()
    if element in Elements:
        fig, ax = plt.subplots(1, 3, figsize=(21, 5))
        for i in range(3):
            ax[i].axvline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].axhline(0,0,1, color='0.75', linestyle='dashed')
            ax[i].set_xlim([-2,1])
            ax[i].set_ylim([-1,1])
            ax[i].set_xlabel('[Fe/H]')
            ax[i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=element)].values,'.',color='black',label='IGRINS')
            ax[i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=element)].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
            ax[i].legend(loc='lower left',fancybox=True) 
        ax[0].set_ylabel('[{ele}/Fe]'.format(ele=element))
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)   
        plt.draw()
        plt.show()
        
    if element == 'Alpha':
        fig, ax = plt.subplots(len(AlphaElements), 3, figsize=(21, len(AlphaElements)*4))
        for row in range(len(AlphaElements)):
            for i in range(3):
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=AlphaElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=AlphaElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=AlphaElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()
        
    #Need to measure more iron-peak elements before this code works
    if element == 'Iron_peak':
        fig, ax = plt.subplots(len(IronElements), 3, figsize=(21, len(IronElements)*4))
        for row in range(len(IronElements)):
            for i in range(3):
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=IronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=IronElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=IronElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()
        
    #Need to measure more neutron-capture elements before this code works
    if element == 'Neutron_capture':
        fig, ax = plt.subplots(len(NeutronElements), 3, figsize=(21, len(NeutronElements)*4))
        for row in range(len(NeutronElements)):
            for i in range(3):
                ax[row,i,].axvline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].axhline(0,0,1, color='0.75', linestyle='dashed')
                ax[row,i].set_xlim([-2,1])
                ax[row,i].set_ylim([-1,1])
                ax[row,i].set_xlabel('[Fe/H]')
                ax[row,i].plot(IGRINS_RESULTS['[Fe/H]'].values,IGRINS_RESULTS['{el}'.format(el=NeutronElements[row])].values,'.',color='black',label='IGRINS')
                ax[row,i].plot(DATA[i+1]['[Fe/H]'].values,DATA[i+1]['{el}'.format(el=NeutronElements[row])].values,'.',color=Colours[i],alpha=0.75,label=CompLabel[i])
                ax[row,i].legend(loc='lower left',fancybox=True) 
            ax[row,0].set_ylabel('[{el}/Fe]'.format(el=NeutronElements[row]))   
        plt.tight_layout()
        plt.savefig(plotdir+element+'.pdf',dpi=500)
        plt.draw()
        plt.show()

    














