"""
Created on 15-03-2020
@author: Martin Montelius
todo: when pandas is on rap, add a directory line with input. This requires changing names, remember that.
"""

import numpy as np
import pandas as pd


#Sorts the linelist file, first three rows are header, every fourth row contains data, the rest are atomic physics and references
def logic(index):
    if index in [0, 1, 2]:
        return(True)
    elif (index-3) % 4 == 0:
        return False
    return True


"___________________________________Actual linelist that we want to modify___________________________________"
ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
LineList = pd.read_csv('LineList.dat', index_col=False, names=ListHeader, skiprows= lambda x: logic(x))
TotLength = len(LineList)*4 + 3 

"______________________________________________Broadening data______________________________________________"
BroadeningHeader = ['Element','Ion','Lambda','Exc','loggf','DampGrade','DampSig','DampVel','W','Wobs','error','abund','not sure','Waals','CombName']
BroadeningData = pd.read_csv('s4000_g+1.5_m1.0_t02_mc_z+0.00_a+0.00_c-0.13_n+0.31_o+0.00_r+0.00_s+0.00_H_abo.eqw', delim_whitespace=True, index_col=False, names=BroadeningHeader, skiprows=1)
BroadeningData['Waals'] = np.floor(BroadeningData['DampSig'])+BroadeningData['DampVel'] #Combines values to SME format
BroadeningData['CombName'] = "'" + BroadeningData['Element'] + ' ' + BroadeningData["Ion"].map(str) + "'" #Combines names to VALD format
BroadeningValues = BroadeningData.loc[BroadeningData.Waals != 0] #Limits the document to where there is broadening data
BVindex = BroadeningValues.index #Index of broadening values, this is probably stupid


"____________________________Find lines in linelist and insert broadening values____________________________"

for i in range(len(BroadeningValues)): 
    try:#__________________wavelength where Linelist name == Broadeninglist name_____________________with wavelength________________________closest to the one in the linelist
        llindex = LineList['LambdaAir'][LineList['EleIon'] == BroadeningValues['CombName'].values[i]].sub(BroadeningValues['Lambda'].values[i]).abs().idxmin()
        #Value of Waals broadening in linelist__________ = New value of broadening from Broadeninglist
        LineList.loc[LineList.index == llindex, 'WaalsDamp'] = BroadeningValues.loc[BroadeningValues.index == BVindex[i], 'Waals'].values
    except ValueError:
        #If a value is present in the broadening list but not in the linelist, except error
        print('The VALD linelist is incomplete for {ele} at {wave} Ångström'.format(ele=BroadeningValues['CombName'].values[i], wave=BroadeningValues['Lambda'].values[i]))
    

'''_______________________________________NEW FILE CREATION LABORATORY_______________________________________'''

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
