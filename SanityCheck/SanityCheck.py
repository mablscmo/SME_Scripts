"""
-----------------------------------------
Created on 2020-03-12
author: Martin Montelius
Version: 0.4.2
-----------------------------------------
This script is meant to help you when SME is giving you an error and you don't have the time to look through everything. 
It will look for any and all things that I guess causes errors in the linemask, segments, continuummask, and LineLists.

WARNING: I don't know any IDL and what I think causes errors are based on 2 months of experience. 
    Future plans include: creating a settings file so you can switch between different profiles looking for different things and different directories;
    Creating a proper output file with helpful formatting and (maybe) suggested edits;
    Maybe a system that automatically flags lines in the files with a comment after the final input? 
    Expect updates when I've learned something new or when I'm procrastinating.

New in version 0.4:
    Rewritten output file formatting code, now both simpler and formatts things properly.
    Implemented a check for intersecting linemasks, a check for the length of linemasks (the precise minimum length is a guess, I don't think it's
    a hard limit).
    More messages for things getting checked.
    
    0.4.1:
        Cleanup of formatting, hopefully everything is clearer.
        Minor change for [y/n] check.
    
    0.4.2:
        Output file now indicates which line is the strongest with *** and lines stronger than a threshold with *. Change the threshold 
        by changing the Tolerance parameter (no plan to make it an input), 100 means lines stronger than 1/100th of the main lines 
        strength will get marked. Remember different ionisationstages are not handled correctly.

New in version 0.3:
    Creates an output file for the linelist search with the strengths of the lines from the weak line approximation included.


"""

import numpy as np
import pandas as pd
import socket

"_____________________________________Set up directories_______________________________________"
#Check computer to see if it is known or if manual selection of directories is needed
Computer = socket.gethostname()
if  Computer == 'ValorToMe':
    ###Directories for my home computer
    lmaskdir = ''
    cmaskdir = ''
    lldir = ''
    LineListName = 'LineList'
elif Computer == 'rap':
    ###Directories for rap
    lmaskdir = '/home/martin/Linelists/'
    cmaskdir = '/nfs/henrik/Linelists/'
    lldir = '/home/martin/Linelists/'
    LineListName = 'VALD_nomols_20200123'
else:
    lmaskdir = input('What is your linemask directory?: ')
    cmaskdir = input('What is your continuummask directory?: ')
    lldir = input('What is your linelist directory?: ')
    print('Please update the SanityCheck.py file with your directories, you are meant to preserve sanity, not lose it.')
    
"Change this to suit your filenames. Filenames not structured as element_instrument_list.dat are currently not supported."
instrument = 'igrinsh'

"__________________________________Pick element & find files____________________________________"
"Choose element. Future version might have a whattodo input that enables different functionalities, changing directories, editing which things are being checked etc."
Elements = ['al','c','ca','ce','co','cr','cu','fe','ge','hf','k','mg','mn','na','nd','ni','p','rb','s','sc','si','ti','v','y','yb']
al,c,ca,ce,co,cr,cu,fe,ge,hf,k,mg,mn,na,nd,ni,p,rb,s,sc,si,ti,v,y,yb = Elements
Al,C,Ca,Ce,Co,Cr,Cu,Fe,Ge,Hf,K,Mg,Mn,Na,Nd,Ni,P,Rb,S,Sc,Si,Ti,V,Y,Yb = Elements

while True:
    try:
            element = input('Which element are you sanity checking? ')
    except NameError:
        print('Element not recogniced, check spelling or edit the code if we got a new element')
        continue
    break
print('Checking {ele}...\n'.format(ele=element))

"Reads in files for checking"
lmask = np.loadtxt('{ldir}{ele}_{inst}_lmask.dat'.format(ldir=lmaskdir, ele=element, inst=instrument),comments=';')
segment = np.loadtxt('{ldir}{ele}_{inst}_seg.dat'.format(ldir=lmaskdir, ele=element, inst=instrument),comments=';')
contmask = np.loadtxt('{cdir}{inst}_automatic_cmask.dat'.format(cdir=cmaskdir, inst=instrument),comments=';')



"____________________________________Checking linemasks_______________________________________"
print('Checking linemasks...')
LmaskFlag = True

'''Checks if the central wavelength is outside the linemask, this might not actually be a problem for certain situations 
and almost certainly does not cause errors, but it might be an ok problem indicator. If it's removed in a later version, it isn't.'''
InitCheck = np.where(lmask[:,0]<lmask[:,1])[0]
if len(InitCheck) != 0:
    for i in range(len(InitCheck)):
        print('{line} linemask starts after centre of line'.format(line=lmask[InitCheck[i-1],0]))
EndCheck = np.where(lmask[:,0]>lmask[:,2])[0]
if len(EndCheck) != 0:
    for i in range(len(EndCheck)):
        print('{line} linemask ends before centre of line'.format(line=lmask[EndCheck[i-1],0]))
if (len(InitCheck) == 0) & (len(EndCheck) == 0):
    print('All linemask contain the central wavelength')


"Checks for linemask intersections"
LmaskFlat = lmask[:,[1,2]].flatten()
LmaskCheck = np.all(np.diff(LmaskFlat) > 0)
if LmaskCheck == False:
    print('Linemasks overlap at: {lmaskind}'.format(lmaskind=LmaskFlat[np.where((np.diff(LmaskFlat) > 0)==False)]))
else:
    print('No linemasks overlap')


"Check width of lmask, email Henrik to find critical length."
lCrit = 0.3
lLength = lmask[:,2] - lmask[:,1]
LengthFlag = False
for i in range(len(lLength)):
    if lLength[i] < lCrit:
        print('{line} linemask width = {lW}, recommended is {lC} Å'.format(line=lmask[i,0], lW=format(lLength[i],'.2f'), lC = lCrit))
        LengthFlag = True
if LengthFlag == False:
    print('No linemasks too short')


"Anything wrong?"
if (len(InitCheck) == 0) & (len(EndCheck) == 0) & (LmaskCheck == True) & (LengthFlag == False):
    print('No issues found in linemasks')
else:
    LmaskFlag = False

print('\n')

  
"____________________________________Checking segments_______________________________________"
print('Checking segments...')

"Checks if segments are continually increasing, i.e. not overlapping. I think this causes errors somewhere, but I'm not sure."
SegFlat = segment.flatten()
SegCheck = np.all(np.diff(SegFlat) > 0)
if SegCheck == False:
    print('Segments overlap at: {segind}'.format(segind=SegFlat[np.where((np.diff(SegFlat) > 0)==False)]))
else:
    print('No segments overlap')
    

"Checks if each line in the linemask is in a segment."
InSegFlag = True 
for i in range(len(lmask)):
    InSegCheck = np.any((lmask[i,1]>segment[:,0])&(lmask[i,2]<segment[:,1]))
    if InSegCheck == False:
        print('Linemask for {line} is not contained within a segment'.format(line=lmask[i,0]))
        InSegFlag = False
if InSegFlag == True:
    print('All linemasks have proper segments')   


"Anything wrong?"    
if (SegCheck & InSegFlag) == True:
    print('No issues found for the segments')

print('\n')


"____________________________________Checking Continuummask__________________________________"
print('Checking continuummasks...')
ContFlag = True 


"Checks if any continuum masks overlap, don't think it causes errors, but it's unnecessary."
ContFlat = contmask.flatten()
ContFlatCheck = np.all(np.diff(ContFlat) > 0)
if ContFlatCheck == False:
    print('Continuummasks overlap at: {contind}'.format(contind=ContFlat[np.where(np.diff(ContFlat) < 0)[0]]))
    ContFlag = False
if ContFlatCheck == True:
    print('No continuummasks overlap')


"Checks  if continuummask intersects segment edges. This definitely causes errors."
for i in range(len(contmask)):
    ContCheck = np.any([(contmask[i,0]<segment[:,1])&(contmask[i,1]>segment[:,1]),(contmask[i,0]<segment[:,0])&(contmask[i,1]>segment[:,0])],axis=1)
    if np.any(ContCheck) == True:
        print('Continuummask at {cont} intersects the segmentborder'.format(cont=contmask[i,0]))
        ContFlag = False


"Checks  if continuummask intersects linemask edges. Not sure if it causes errors, but it would seem counterintuitive that a section is both line and continuum."
for i in range(len(contmask)):
    ContLineCheck = np.any([(contmask[i,0]<lmask[:,2])&(contmask[i,1]>lmask[:,2]),(contmask[i,0]<lmask[:,1])&(contmask[i,1]>lmask[:,1])],axis=1)
    if np.any(ContLineCheck) == True:
        InterruptedLine = np.where((contmask[i,0]<lmask[:,2])&(contmask[i,1]>lmask[:,2]) | (contmask[i,0]<lmask[:,1])&(contmask[i,1]>lmask[:,1]))[0]
        # print(InterruptedLine, i)
        print('Continuummask at {cont} intersects the linemask for {line}'.format(cont=format(contmask[i,0],'.3f'), line=lmask[InterruptedLine,0]))
        ContFlag = False


"Anything wrong?"
if ContFlag == True:
    print('No issues found in the continuummasks\n')  


"____________________________________Status report__________________________________"
if (LmaskFlag & SegCheck & InSegFlag & ContFlag ) == True:
    print('No issues found in the masks')


"____________________________________Linelist check__________________________________"
if Computer != 'rap':
    while True:
        try:
                ynq = input('Do you want to check the linelist? [y/n]: ')
        except NameError:
            print('Input not recogniced')
            continue
        break
else:
    ynq = 'n'
    print('\n')
    print("Can't check the linelist on rap at the moment due to pandas limitations")


if ynq in ['n','N','no','No','NO']:
    raise SystemExit('Linelist not checked')

NoLinesFlag = False
MultLinesFlag = False

"______________________________________Functions_____________________________________"
def logic(index):
    '''Sorts the VALD linelist file, first three rows are header, every fourth row contains data, the rest are atomic physics and references '''
    if index in [0, 1, 2]:
        return(True)
    elif (index-3) % 4 == 0:
        return False
    return True    

def strength(gf, exc, T=5770):
    '''Determines the strength of spectral lines using the weak-line approximation. Only works for lines of the same element and ionisationstage. 
    Takes the gf value and the excitation energy [eV] as inputs, temperature is also needed, set to 5770 K by default to mimic the Sun. '''
    return((10**gf)*np.exp(-exc/(T*8.6173*10**-5)))


"______________________________Reads in linelist_____________________________________"
ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
LineList = pd.read_csv(lldir + LineListName + '.dat', index_col=False, names=ListHeader, skiprows= lambda x: logic(x))

LineList[['Ele','Ion']] = LineList.EleIon.str.split(expand=True)
LineList['Ele'] = LineList['Ele'].str.lower() + "'"
LineList = LineList.drop(columns=['JLow', 'ExcHigh', 'JHigh', 'LandLower', 'LandUpper', 'LandMean', 'RadDamping', 'StarkDamp', 'WaalsDamp', 'CentralDepth'])
LineList['strength'] = strength(LineList['loggf'],LineList['ExcLow'],5700)


"_______________________Checks linelist and writes report file_______________________"
'''Goes through ther linemask to identify which lines are of interest. If there are multiple lines, it lets yuo know and adds the lines
to a report file. Also alerts and writes down linemasks that do not contain any lines of the correct element.'''

ReportFile = open("{el}_report.txt".format(el=element),"w+")

MultLineCount = 0
NoLineCount = 0
Tolerance = 100
for i in range(len(lmask)):
    start = lmask[i,1]
    stop = lmask[i,2]
    LinesInMask = LineList[(LineList['LambdaAir']>=start) & (LineList['LambdaAir']<=stop) & (LineList['Ele'].values == "'" + element + "'")]
    LinesInMask = LinesInMask.drop(columns=['Ele', 'Ion'])
    if len(LinesInMask) > 1:
        print('Multiple lines in linemask {lam}:'.format(lam=lmask[i,0]))
        print(LinesInMask)
        MaxStrength = LinesInMask.strength.max()
        ReportFile.write('Multiple lines in linemask {lam}:\n'.format(lam=lmask[i,0]))
        for i in range(len(LinesInMask)):
            StrengthFlag = ''
            if LinesInMask.strength.iloc[i] == MaxStrength:
                StrengthFlag = '***'
            elif LinesInMask.strength.iloc[i] > MaxStrength/Tolerance:
                StrengthFlag = '*'
            InLine = LinesInMask.values[i]
            ReportFile.write("{0: <8}   lam_air: {1} AA     log gf:{2: >8}     Exc:{3: >7} eV     strength: {4}  {5}\n".format(InLine[0], format(InLine[1],'.3f'), format(InLine[2],'.3f'), format(InLine[3],'.3f'), "{:.3e}".format(InLine[4]), StrengthFlag))
        MultLinesFlag = True
        MultLineCount += 1
        ReportFile.write("\n")
    if len(LinesInMask) == 0:
        print('No line found in the linelist for linemask at {lam}'.format(lam=lmask[i,0]))
        ReportFile.write('No line found in the linelist for linemask at {lam}\n'.format(lam=lmask[i,0]))
        NoLinesFlag = True
        NoLineCount += 1
        ReportFile.write("\n")

ReportFile.close()

"_____________________________________Final status___________________________________"
print('\n')
if MultLinesFlag == False:
    print('No additional lines found within the linemasks')
else:
    print('{count}/{tot} linemasks with multiple lines'.format(count=MultLineCount, tot = len(lmask)))

if NoLinesFlag == False:
    print('No linemasks without lines')
else:
    print('{count}/{tot} linemasks without lines'.format(count=NoLineCount, tot = len(lmask)))
