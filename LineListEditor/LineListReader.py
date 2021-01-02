# -*- coding: utf-8 -*-
"""
-----------------------------------------
Created on 2020-10-14
author: Martin Montelius
Version: 0.1.1
-----------------------------------------

Skulle kunna skriva column mergers som en list comprahension, ge inte names till read csv, ha bara nummer

NOTE: Reading in the inelist currently assumes that the references have been removed from the end of the linelist, since they have been in my list. Change the [-21] in the pd.read_csv lines to match your linelist.

New in 0.1.1:
    Added optional filtering by element and ionisation stage
    Removed the "'" markers around element and ionisation stage

To do:
    Ponder if I want EleIon or Ele Ion, truly a question for the ages
    Improve how LS terms are read in, need to change from using ListHeader to 
    something that means something
"""

import pandas as pd

def LL_reader(LL_name, LL_dir,write=True,element=False,ion=False):   
    '''Reads in VALD3 "extract stellar" linelists. To read other formats, such
    as "extract element" the column names need to be changed, alo how the LS
    terms are extracted, as the formatting is inconsistent between different 
    extraction methods.
    
    LL_name: filename of the linelist
    LL_dir:  directory of the linelist
    write: Boolean, True will read in additional columns with the atomic config
    lines unformatted so that a new linelist can be created. 
    
    A LL_writer is coming sooner or later.'''
    
    #Need to use the full header to make Pandas happy, wants as many names as there are columns and with the [:-21][4::4] method it gets all columns at the start
    #LS_names for the long format VALD list atomic configurations
    ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
    
    #Reads in the main information inn the linelist
    ll = pd.read_csv(LL_dir + LL_name, index_col=False, names=ListHeader, low_memory=False)[:-21][3::4]
    
    #Reads atomic config. does its best to identify which parts are which. Fails for some weird Fe and H lines, probably others too.
    LS1 = pd.read_csv(LL_dir + LL_name, index_col=False, names=ListHeader, delim_whitespace=True,low_memory=False)[:-21][4::4].dropna(1,'all')
    LS1['LS1'] = LS1['LambdaAir']
    
    #Checks if more terms than expected are present, should use better column names, preliminary.
    LS1.loc[LS1['JLow'].isnull() == False, 'base1'] = LS1['loggf'] + LS1['ExcLow']
    LS1.loc[LS1['JLow'].isnull() == True, 'base1'] = LS1['loggf']
    LS1.loc[LS1['JLow'].isnull() == False, 'end1'] = LS1['JLow']
    LS1.loc[LS1['JLow'].isnull() == True, 'end1'] = LS1['ExcLow']
    #removes ' from extract stellar VALD formatting
    LS1['end1'] = LS1['end1'].apply(lambda x: str(x).strip("'"))
    if write == True:
        #Copy of entire string for file creation. Stupidly coded because some references have a , in them
        LS1_write = pd.read_csv(LL_dir + LL_name,names=ListHeader,index_col=False,dtype=str,low_memory=False)[:-21][4::4].dropna(1,'all')
        LS1_write.loc[LS1_write['LambdaAir'].isnull() == False, 'EleIon'] = LS1_write['EleIon'] + ',' + LS1_write['LambdaAir']
        LS1_write = LS1_write.drop('LambdaAir',axis=1)
        LS1_write.columns = ['LS1_write']

    
    
    LS2 = pd.read_csv(LL_dir + LL_name, index_col=False, names=ListHeader, delim_whitespace=True, low_memory=False)[:-21][5::4].dropna(1,'all')
    LS2['LS2'] = LS2['LambdaAir']
    LS2.loc[LS2['JLow'].isnull() == False, 'base2'] = LS2['loggf'] + LS2['ExcLow']
    LS2.loc[LS2['JLow'].isnull() == True, 'base2'] = LS2['loggf']
    LS2.loc[LS2['JLow'].isnull() == False, 'end2'] = LS2['JLow']
    LS2.loc[LS2['JLow'].isnull() == True, 'end2'] = LS2['ExcLow']
    LS2['end2'] = LS2['end2'].apply(lambda x: str(x).strip("'"))
    if write == True:
        LS2_write = pd.read_csv(LL_dir + LL_name,names=ListHeader,index_col=False,dtype=str,low_memory=False)[:-21][5::4].dropna(1,'all')
        LS2_write.loc[LS2_write['LambdaAir'].isnull() == False, 'EleIon'] = LS2_write['EleIon'] + ',' + LS2_write['LambdaAir']
        LS2_write = LS2_write.drop('LambdaAir',axis=1)
        LS2_write.columns = ['LS2_write']

    
    
    #Reads in references, does bot divide into columns since I have butchered VALDs system for this
    ref = pd.read_csv(LL_dir + LL_name,names=ListHeader,index_col=False,dtype=str)[:-21][6::4].dropna(1,'all')
    ref.loc[ref['loggf'].isnull() == False, 'EleIon'] = ref['EleIon'] + ',' + ref['LambdaAir'] + ',' + ref ['loggf']
    ref = ref.drop(['LambdaAir', 'loggf'],axis=1)
    ref.columns = ['ref']
    
    #Resets indexes of all files. drop=True makes sure the index isn't saved.
    ll = ll.reset_index(drop=True)
    LS1 = LS1.reset_index(drop=True)
    LS2 = LS2.reset_index(drop=True)
    ref = ref.reset_index(drop=True)
    if write == True:
        LS1_write = LS1_write.reset_index(drop=True)
        LS2_write = LS2_write.reset_index(drop=True)
    
    #Combines to make one big linelist
    ll['LS1'],ll['base1'],ll['end1'] = LS1['LS1'], LS1['base1'], LS1['end1']
    ll['LS2'],ll['base2'],ll['end2'] = LS2['LS2'], LS2['base2'], LS2['end2']
    ll['ref'] = ref['ref']
    if write == True:
        ll['LS1_write'],ll['LS2_write'] = LS1_write['LS1_write'],LS2_write['LS2_write']
    
    #Convert columns with numbers to numbers
    ll[['LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']] = ll[['LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']].astype(float)
    #Removes unnecessary extra "'"
    ll['EleIon'] = ll.EleIon.apply(lambda x: x.strip("'"))
    if element != False:
        ll = ll.loc[ll.EleIon.apply(lambda x: x.split()[0]) == element.capitalize()]
    if ion != False:
        ll = ll.loc[ll.EleIon.apply(lambda x: x.split()[1]) == str(ion)]
            
    return(ll)
