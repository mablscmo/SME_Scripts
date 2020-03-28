"""
-----------------------------------------
Created on 2020-03-12
author: Martin Montelius
Version: 0.2.1
-----------------------------------------
This script is meant to help you when SME is giving you an error and you don't have the time to look through everything. 
It will look for any and all things that I guess causes errors in the linemask, segments, continuummask, and LineLists.

WARNING: I don't know any IDL and what I think causes errors are based on 2 months of experience. 
    Future plans include: creating a settings file so you can switch between different profiles looking for different things and different directories;
    Creating a proper output file with helpful formatting and (maybe) suggested edits;
    Maybe a system that automatically flags lines in the files with a comment after the final input? 
    Expect updates when I've learned something new or when I'm procrastinating.

New in version 0.2:
    SanityCheck searches through the linelist for linemasks containing none or multiple lines. Multiple lines causes trouble for astrophysical gf.
        The linelist features requires pandas version '0.25.3' or higher (or maybe lower as well), so it doesn't work on rap.
    SanityCheck checks which computer it is being run on and has saved directories. Maybe I remove the input and just tell people to update the file.
    
    0.2.1
    Fixed a problem with the continuum/linemask intersection finder
"""

import numpy as np
import pandas as pd
import socket

"Optional input statements that will be integrated in a future version"
# instrument = input('Which instrument are you working with? (no caps please): ')
# print 'Working with {inst}'.format(inst=instrument)


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
    print('Please update the SanityCheck.py file with your directories, you are ment to preserve sanity, not lose it.')


al,c,ca,ce,co,cr,cu,fe,ge,hf,k,mg,mn,na,nd,ni,p,rb,s,sc,si,ti,v,y,yb = 'al','c','ca','ce','co','cr','cu','fe','ge','hf','k','mg','mn','na','nd','ni','p','rb','s','sc','si','ti','v','y','yb'
Al,C,Ca,Ce,Co,Cr,Cu,Fe,Ge,Hf,K,Mg,Mn,Na,Nd,Ni,P,Rb,S,Sc,Si,Ti,V,Y,Yb = 'al','c','ca','ce','co','cr','cu','fe','ge','hf','k','mg','mn','na','nd','ni','p','rb','s','sc','si','ti','v','y','yb'

"Change these to your filenames. Filenames not structured as element_instrument_list.dat are currently not supported."
instrument = 'igrinsh'


"Choose element. Future version might hve a whattodo input that enables different functionalities, changing directories, editing which things are being checked etc."
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

"Checks if the central wavelength is outside the linemask, this might not actually be a problem for certain situations and almost certainly does not cause errors, but it might be an ok problem indicator. If it's removed in a later version, it isn't."
InitCheck = np.where(lmask[:,0]<lmask[:,1])[0]
if len(InitCheck) != 0:
    for i in range(len(InitCheck)):
        print('{line} linemask starts after centre of line'.format(line=lmask[InitCheck[i-1],0]))
EndCheck = np.where(lmask[:,0]>lmask[:,2])[0]
if len(EndCheck) != 0:
    for i in range(len(EndCheck)):
        print('{line} linemask ends before centre of line'.format(line=lmask[EndCheck[i-1],0]))

if (len(InitCheck) == 0) & (len(EndCheck) == 0):
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
    print('Segments overlap at: {segind}'.format(segind=SegFlat[np.where(np.diff(SegFlat) < 0)[0]]))
if SegCheck == True:
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
    
print('\n')


"____________________________________Checking Continuummask__________________________________"
print('Checking continuummasks...')
ContFlag = True 

"Checks if any continuum masks overlap, don't think it causes errors, but is unnecessary."
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


if ContFlag == True:
    print('All continuummasks are properly formatted\n')  


"____________________________________Status report__________________________________"

if (LmaskFlag & SegCheck & InSegFlag & ContFlag ) == True:
    print('No problems detected')

"____________________________________Linelist check__________________________________"
n = 'n'
N = 'n'
no = 'n'

while True:
    try:
            ynq = eval(input('Do you want to check the linelist? [y/n]: '))
    except NameError:
        print('Input not recogniced')
        continue
    break

if ynq == 'n':
    raise SystemExit('Linelist not checked')

NoLinesFlag = False
MultLinesFlag = False

def logic(index):
    if index in [0, 1, 2]:
        return(True)
    elif (index-3) % 4 == 0:
        return False
    return True    


ListHeader = ['EleIon','LambdaAir', 'loggf', 'ExcLow', 'JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth']
LineList = pd.read_csv(lldir + LineListName + '.dat', index_col=False, names=ListHeader, skiprows= lambda x: logic(x))
LineList[['Ele','Ion']] = LineList.EleIon.str.split(expand=True)
LineList['Ele'] = LineList['Ele'].str.lower() + "'"
LineList = LineList.drop(columns=['JLow', 'ExcHigh', 'JHigh', 'LandLower', 'LandUpper', 'LandMean', 'RadDamping', 'StarkDamp', 'WaalsDamp', 'CentralDepth'])


MultLineCount = 0
NoLineCount = 0
for i in range(len(lmask)):
    start = lmask[i,1]
    stop = lmask[i,2]
    LinesInMask = LineList[(LineList['LambdaAir']>=start) & (LineList['LambdaAir']<=stop) & (LineList['Ele'].values == "'" + element + "'")]
    LinesInMask = LinesInMask.drop(columns=['Ele', 'Ion'])
    if len(LinesInMask) > 1:
        print('Multiple lines in linemask {lam}:'.format(lam=lmask[i,0]))
        print(LinesInMask)
        MultLinesFlag = True
        MultLineCount += 1
    if len(LinesInMask) == 0:
        print('No line found in the linelist for linemask at {lam}'.format(lam=lmask[i,0]))
        NoLinesFlag = True
        NoLineCount += 1
        
print('\n')
if MultLinesFlag == False:
    print('No additional lines found within the linemasks')
else:
    print('{count}/{tot} linemasks with multiple lines'.format(count=MultLineCount, tot = len(lmask)))

if NoLinesFlag == False:
    print('No linemasks without lines')
else:
    print('{count}/{tot} linemasks without lines'.format(count=NoLineCount, tot = len(lmask)))
