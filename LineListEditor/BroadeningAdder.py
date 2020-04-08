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


"______________________________________________Broadening data______________________________________________"
BroadeningHeader = ['Element','Ion','Lambda','Exc','loggf','DampGrade','DampSig','DampVel','W','Wobs','error','abund','not sure','Waals','CombName']
BroadeningData = pd.read_csv('s4000_g+1.5_m1.0_t02_mc_z+0.00_a+0.00_c-0.13_n+0.31_o+0.00_r+0.00_s+0.00_H_abo.eqw', delim_whitespace=True, index_col=False, names=BroadeningHeader, skiprows=1)
BroadeningData['Waals'] = np.floor(BroadeningData['DampSig'])+BroadeningData['DampVel'] #Combines values to SME format
BroadeningData['CombName'] = "'" + BroadeningData['Element'] + ' ' + BroadeningData["Ion"].map(str) + "'" #Combines names to mimic VALD format
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

#len(LineList)*4+3 gives the total length of the linelist file, remember LineList is only the data
for i in range(len(LineList)*4+3):
    if logic(i) == False:
        Data = LineList.iloc[count]
        
        #format() creates the appropriate number of decimals, better than round()
        element = Data[0]
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
        
        NewFile.write('''{ele},{wsp1}{lam},{wsp2}{gf},{wsp3}{El},{wsp4}{Jlow},{wsp5}{Eu},{wsp6}{Jhigh},{wsp7}{LaL},{wsp8}{LaU},{wsp9}{LaM},{wsp10}{Rad},{wsp11}{Stark},{wsp12}{Waals}, {CD},
'''.format(ele = element, wsp1=' '*(13-len(element)), lam=format(Data[1],'.3f'), wsp2=' '*(8-len(str(gf))), gf=gf, wsp3=' '*(8-len(str(El))),El=El, wsp4=' '*(5-len(str(Jlow)))  ,Jlow=Jlow, wsp5=' '*(8-len(str(Eu))), Eu=Eu, wsp6=' '*(5-len(str(Jhigh)))  ,Jhigh=Jhigh, wsp7=' '*(7-len(str(LaL))), LaL=LaL, wsp8=' '*(7-len(str(LaU))), LaU=LaU, wsp9=' '*(7-len(str(LaM))), LaM=LaM, wsp10=' '*(6-len(str(Rad))), Rad=Rad, wsp11=' '*(6-len(str(Stark))), Stark=Stark, wsp12=' '*(8-len(str(Waals))), Waals=Waals, CD = CD))
        
        #Uses count instead of i as we only take a value from LineList every fourth iteration
        count += 1
        
        #Open up the line from the file even though we don't use it since we can't choose which lines to open
        Other.readline()
    else:
        #Write the unchanged lines from the old linelist to the new one
        NewFile.write(Other.readline())

#Close files to save the changes
Other.close()
NewFile.close()
