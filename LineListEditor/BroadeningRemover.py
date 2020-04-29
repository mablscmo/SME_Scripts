"""
Created on 15-03-2020
@author: Martin Montelius
todo: 
"""

import numpy as np
import pandas as pd


"________________________________________________Functions__________________________________________________"
def logic(index):
    '''Sorts the VALD linelist file, first three rows are header, every fourth row contains data, the rest are atomic physics and references '''
    if index in [0, 1, 2]:
        return(True)
    elif (index-3) % 4 == 0:
        return False
    return True

def strength(gf, exc, T=5770):
    '''Determines the strength of spectral lines using the weak-line approximation. Only works for lines of the same element
    and ionisationstage. Takes the gf value and the excitation energy as inputs, temperature is also needed, set to 5770 by 
    default to mimic the Sun. '''
    return((10**gf)*np.exp(-exc/(T*8.6173*10**-5)))


"_____________________________________________Read in all files_____________________________________________"
print('Loading files...')
#Linelist you want to remove van der Waals broadening data you have added
LineListFile ='LineListCurrent.dat'
LLdir = '/Users/monte/OneDrive - Lund University/Uni/Master/LineList_Copies/'

#Linelist without the added van der Waals broadening
SourceFile = 'LinelistOriginal.dat'
Sdir = '/Users/monte/OneDrive - Lund University/Uni/Master/LineList_Copies/'

"___________________________________Actual linelist that we want to modify__________________________________"
ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower',
              'LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
LineList = pd.read_csv(LLdir +LineListFile, index_col=False, names=ListHeader, skiprows= lambda x: logic(x))
LineLength = len(LineList)
TotLength = len(LineList)*4 + 3 

"_____________________________________________Old broadening data____________________________________________"
BroadeningHeader = ListHeader
BroadeningData = pd.read_csv(Sdir + SourceFile, index_col=False, names=BroadeningHeader, skiprows= lambda x: logic(x))


"____________________________Find lines in linelist and insert broadening values____________________________"
print('Restoring broadening values to previous state, this will take a while...')

TrackerFile = open("LinesWithBroadening.txt","w+")
progress = 0
for i in range(LineLength):
    try:
        OrigBroad = LineList.iloc[i]['WaalsDamp']
        LineList.loc[LineList.index == i, 'WaalsDamp'] = BroadeningData.loc[(BroadeningData['EleIon'] == LineList['EleIon'][i]) & (BroadeningData['LambdaAir'] == LineList['LambdaAir'].values[i]), 'WaalsDamp'].values[0]
    except IndexError:
        print("Can't find line {0} at {1} Å".format(i,format(LineList.loc[LineList.index == i, 'LambdaAir'].values[0],'.3f')))
    if OrigBroad != LineList.iloc[i]['WaalsDamp']:
        BroadLine = LineList.iloc[i]
        TrackerFile.write('{0: <8} {1: <11} Old vdW: {2: <9} New vdW: {3: <9} Source: bsyn   Fit: \n'.format(BroadLine['EleIon'], format(BroadLine['LambdaAir'],'.3f'), format(OrigBroad,'.3f'), format(BroadLine['WaalsDamp'],'.3f')))
    if round(100*(1+i)/LineLength) != progress:
        progress = round(100*(1+i)/LineLength)
        print('{nr}% '.format(nr=progress))
TrackerFile.close()

'''_______________________________________NEW FILE CREATION LABORATORY_______________________________________'''



while True:
    try:
            ynq = input('Do you want to create a new linelist? [y/n]: ')
    except NameError:
        print('Input not recogniced')
        continue
    break

if ynq in ['n','N','no','No','NO']:
    raise SystemExit('No new linelist')


#Create a new linelist and open the old one for reading
NewFile = open("NewLineList.dat","w+")
Other = open("LineList.dat","r")


#Keep track of where in the imported dataframe you are
count=0

progress = 0
for i in range(TotLength):
    if logic(i) == False:
        Data = LineList.iloc[count]
        
        #format() creates the appropriate number of decimals, better than round()
        element = Data[0] + ','
        lam=format(Data[1],'.3f')
        gf = format(Data[2],'.3f')
        El = format(Data[3],'.4f')
        Jlow = Data[4]
        Eu = format(Data[5],'.4f') 
        Jhigh = Data[6]
        LaL = format(Data[7],'.3f')
        LaU = format(Data[8],'.3f')
        LaM = format(Data[9],'.3f')
        Rad = format(Data[10],'.3f')
        Stark = format(Data[11],'.3f')
        Waals = format(Data[12],'.3f')
        CD = format(Data[13],'.3f')
        
        NewFile.write('''{0: <14}{1},{2: >8},{3: >8},{4: >5},{5: >8},{6: >5},{7: >7},{8: >7},{9: >7},{10: >6},{11: >6},{12: >8},{13: >6},
'''.format(element, lam, gf, El, Jlow, Eu, Jhigh, LaL, LaU, LaM, Rad, Stark, Waals, CD))
        
        #Uses count instead of i as we only take a value from LineList every fourth iteration
        count += 1
        
        #Open up the line from the file even though we don't use it since we can't choose which lines to open
        Other.readline()
    else:
        #Write the unchanged lines from the old linelist to the new one
        NewFile.write(Other.readline())
    
    if round(10*(1+i)/TotLength) != progress:
        progress = round(10*(1+i)/TotLength)
        print('{nr}% '.format(nr=progress*10))
#Close files to save the changes
Other.close()
NewFile.close()
