"""
Created on 15-03-2020
@author: Martin Montelius

Alternate version of BroadeningAdder.py, only adds broadeningdata for one element at a time and only for 
strong lines (you define what strong means based on testing). Also uses a VALD linelist as input since
BroadeningAdder has already created a VALD linelist that we can use.

todo: when pandas is on rap, add a directory line with input. This requires changing names, remember that.
    create alternate logic function that picks out the references and can find all the astr lines+
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
    and ionisationstage. Takes the gf value and the excitation energy [eV] as inputs, temperature is also needed, set to 5770 by 
    default to mimic the Sun. '''
    return((10**gf)*np.exp(-exc/(T*8.6173*10**-5)))
    


"__________________________Elements we might want to add vdW broadening data for____________________________"
Elements = ['Al','C','Ca','Ce','Co','Cr','Cu','Fe','Ge','HF','K','Mg','Mn','Na','Nd','Ni','P','Rb','S','Sc','Si','Ti','V','Y','Yb']
al,c,ca,ce,co,cr,cu,fe,ge,hf,k,mg,mn,na,nd,ni,p,rb,s,sc,si,ti,v,y,yb = Elements
Al,C,Ca,Ce,Co,Cr,Cu,Fe,Ge,Hf,K,Mg,Mn,Na,Nd,Ni,P,Rb,S,Sc,Si,Ti,V,Y,Yb = Elements

while True:
    try:
        element = eval(input('Input element: '))
    except NameError:
        print('Element not recogniced, check spelling or edit the code if we got a new element')
        continue
    print('Inserting vdW broadening data for {ele}...\n'.format(ele=element))
    break

while True:
    try:
        ionstage = eval(input('Input ionisationstage: '))
        if not isinstance(ionstage,int): raise NameError()
    except NameError:
        print('Please give the ionisationstage as an integer')
        continue
    print('Ioniationstage {io}...\n'.format(io=ionstage))
    break

ElementIon = "'{ele} {ion}'".format(ele=element, ion=ionstage)

"____________________Selects how strong a line has to be before we add vdW broad. data______________________"
while True:
    try:
        Depth = eval(input('Insert vdW broadening data for lines deeper than: '))
        if not isinstance(Depth,(float,int)): raise NameError()
    except NameError:
        print('Please input the depth as a float or int')
        continue
    print('Inserting vdW broadening data for lines deeper than {dep} ...\n'.format(dep=Depth))
    break


"_____________________________________________Read in all files_____________________________________________"
LineListFile ='LineList.dat'
LLdir = ''

SourceFile = 'LinelistOriginal.dat'
Sdir = '/Users/monte/OneDrive - Lund University/Uni/Master/LineList_Copies/'

SunDataFile = 'SUN_CERES_H_air.ascii'
SDdir = ''

LineMaskFile = '{ele}_igrinsh_lmask.dat'.format(ele=element.lower())
LMdir = '/Users/monte/OneDrive - Lund University/Uni/Master/OriginalFiles/'

"___________________________________Actual linelist that we want to modify__________________________________"
ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
LineList = pd.read_csv(LLdir +LineListFile, index_col=False, names=ListHeader, skiprows= lambda x: logic(x))
LineList['Strength'] = strength(LineList['loggf'],LineList['ExcLow'])
TotLength = len(LineList)*4 + 3 

"__________________________________________________Solar data_______________________________________________"
SunHeader = ['Wavelength', 'Flux']
SunData = pd.read_csv(SDdir + SunDataFile, index_col=False, names=SunHeader, delim_whitespace=True)

"__________________________________________________Line mask________________________________________________"
MaskHeader = ['Line', 'Start', 'Stop']
LineMask = pd.read_csv(LMdir + LineMaskFile, index_col=False, names=MaskHeader, delim_whitespace=True)
LMlen = len(LineMask)

"_______________________________________________Broadening data_____________________________________________"
BroadeningHeader = ListHeader
BroadeningData = pd.read_csv(Sdir + SourceFile, index_col=False, names=BroadeningHeader, skiprows= lambda x: logic(x))


"______________________Find lines in linemask, check depth and insert broadening values_____________________"

'''For each line in the linemask, check the resultsfile to see if the spectra is below the set minimum flux at any point with the mask.
   If that is the case, we pick out the lines within the linemask of the same element and ionisationstage from the linelist. Using strength
   to find which line should be strongest according to the weak line approximation, the line we are interested in in the linemask is selected.
   The line designation in the linemask file is not used because they sometimes seem to be from a different linelist than the one we are 
   working with. If the element has been checked previously the strongest line should always be the correct one, as adjust_lines wouldn't work 
   otherwise.
   Excepts cases where a line has been added to the linelist and the list with the broadeningvalues has not been updated.'''
   
BroadCount = 0
for i in range(LMlen):
    start, stop = LineMask[['Start', 'Stop']].iloc[i].values
    MaxDepth = SunData.loc[(SunData['Wavelength'] > start) & (SunData['Wavelength'] < stop), 'Flux'].min()
    if MaxDepth < Depth:
        try:
            LinesInMask = LineList.loc[(LineList['LambdaAir']>start) & (LineList['LambdaAir']<stop) & (LineList['EleIon'] == ElementIon)]
            Line = LinesInMask.loc[LinesInMask['Strength'] == LinesInMask['Strength'].max()]
            LineList.loc[LineList.index == Line.index.values[0], 'WaalsDamp'] = BroadeningData.loc[BroadeningData['LambdaAir'] == Line['LambdaAir'].values[0]]['WaalsDamp'].values[0]
            BroadCount += 1
        except IndexError:
            print('The linelist with broadeningdata is incomplete at {wave} Ångström'.format(wave=format(Line['LambdaAir'].values[0],'.3f')))
            
print('Broadening data added to ' + str(BroadCount) + ' lines\n')    
    

'''_______________________________________NEW FILE CREATION LABORATORY_______________________________________'''

print('Creating a new linelist (this takes a while)...\n')

#Create a new linelist and open the old one for reading
NewFileName = "NewLineList_" + str(element) + str(ionstage) + "_vdW.dat"
NewFile = open(NewFileName,"w+")
Other = open("LineList.dat","r")

#Keep track of where in the imported dataframe you are
count=0

#len(LineList)*4+3 gives the total length of the linelist file, remember LineList is only the data
progress = 0
for i in range(TotLength):
    if logic(i) == False:
        Data = LineList.iloc[count]
        
        #format() creates the appropriate number of decimals, better than round()
        element = Data[0] + ','
        lam = format(Data[1],'.3f')
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

print('\n{name} with {num} new vdW broadening values for lines deeper than {dep} has been created'.format(name = NewFileName, num = BroadCount, dep = Depth))
