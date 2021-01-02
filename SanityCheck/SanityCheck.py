"""
-----------------------------------------
Created on 2020-03-12
author: Martin Montelius
Version: 0.5
-----------------------------------------
This script is meant to help you when SME is giving you an error and you don't 
have the time to look through everything. It will look for any and all things 
that I guess causes errors in the linemask, segments, continuummask, and LineLists.

WARNING: I don't know any IDL and what I think causes errors are based on 3 months of experience. 
    Future plans include: creating a settings file so you can switch between different profiles looking for different things and different directories;
    Creating a proper output file with helpful formatting and (maybe) suggested edits;
    Maybe a system that automatically flags lines in the files with a comment after the final input? 
    Expect updates when I've learned something new or when I'm procrastinating.

New in version 0.5:
    Now uses LineListReader.py to handle the linelist in a much smoother way, 
    should now work for older pandas versions.
    Weak-line approximation moved to separate file.
    Some of the linelist checking code has been optimised.

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
    
    0.4.3:
        Continuummask checking output now gives you actually useful information on the mask. Something that actually tells you where 
        the overlap is, not yet implemented or planned. 
        Formatting cleanup.
    
    0.4.4:
        Implemented a check to see if the mask files are actually there, will polish later with a proper quit option.
        You can now alter which linelist you are using on the fly:
            When prompted [y/n] to choose if you will check the linelist, give 'update' to be promted to change which
            linelist you are currently working with.
        If the code can't find your linelist, you are now prompted to change it's name.
    
    0.4.5:
        Implemented sys.argv to pick element to make things easier on rap/fedtmule
"""

import numpy as np
import pandas as pd
import socket
import sys

"_____________________________________Set up directories_______________________________________"
#Check computer to see if it is known or if manual selection of directories is needed
Computer = socket.gethostname()
if  (Computer == 'ValorToMe') | (Computer == 'SQWAAK2'):
    ###Directories for my home computer
    lmaskdir = ''
    cmaskdir = ''
    LL_dir = '/Users/monte/OneDrive - Lund University/Uni/Master/LineList_Copies/'
    LL_name = 'VALD_nomols_20200123.dat'
elif (Computer == 'rap') | (Computer == 'fedtmule'):
    ###Directories for rap
    lmaskdir = '/home/martin/Linelists/'
    cmaskdir = '/nfs/henrik/Linelists/'
    LL_dir = '/home/martin/Linelists/'
    LL_name = 'VALD_nomols_20200123.dat'
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
q = 'quit'

while True:
    if len(sys.argv) > 1:
        try:
            element = sys.argv[1]
            if element not in Elements + [q]: raise NameError
        except NameError:
            raise SystemExit('Element not recogniced, check spelling or edit the code if we got a new element')
    else:
        try:
            element = eval(input('Which element are you sanity checking?: '))
        except NameError:
            print('Element not recogniced, check spelling or edit the code if we got a new element')
            continue
    if element == q:
        raise SystemExit('Sanity not checked')
    try:
        "Reads in files for checking"
        lmask = np.loadtxt('{ldir}{ele}_{inst}_lmask.dat'.format(ldir=lmaskdir, ele=element, inst=instrument),comments=';')
        segment = np.loadtxt('{ldir}{ele}_{inst}_seg.dat'.format(ldir=lmaskdir, ele=element, inst=instrument),comments=';')
        contmask = np.loadtxt('{cdir}{inst}_automatic_cmask.dat'.format(cdir=cmaskdir, inst=instrument),comments=';')
    except FileNotFoundError:
        print("The files for {} were not found, try another element or press 'q' to quit".format(element))
        continue        
    except OSError:
        print("The files for {} were not found, try another element or press 'q' to quit".format(element))
        continue        
        
    break
print('Checking {}...\n'.format(element))

print('{} linemasks found...\n'.format(len(lmask)))


"____________________________________Checking linemasks_______________________________________"
print('Checking linemasks...')
LmaskFlag = True

'''Checks if the central wavelength is outside the linemask, this might not actually be a problem for certain situations 
and almost certainly does not cause errors, but it might be an ok problem indicator. If it's removed in a later version, it isn't.'''
InitCheck = np.where(lmask[:,0]<lmask[:,1])[0]
if len(InitCheck) != 0:
    for i in range(len(InitCheck)):
        print('{} linemask starts after centre of line'.format(lmask[InitCheck[i-1],0]))
EndCheck = np.where(lmask[:,0]>lmask[:,2])[0]
if len(EndCheck) != 0:
    for i in range(len(EndCheck)):
        print('{} linemask ends before centre of line'.format(lmask[EndCheck[i-1],0]))
if (len(InitCheck) == 0) & (len(EndCheck) == 0):
    print('All linemask contain the central wavelength')


"Checks for linemask intersections"
LmaskFlat = lmask[:,[1,2]].flatten()
LmaskCheck = np.all(np.diff(LmaskFlat) > 0)
if LmaskCheck == False:
    print('Linemasks overlap at: {}'.format(LmaskFlat[np.where((np.diff(LmaskFlat) > 0)==False)]))
else:
    print('No linemasks overlap')


"Check width of lmask, email Henrik to find critical length."
lCrit = 0.3
lLength = lmask[:,2] - lmask[:,1]
LengthFlag = False
for i in range(len(lLength)):
    if lLength[i] < lCrit:
        print('{} linemask width = {}, recommended is {} Ã…'.format(lmask[i,0], format(lLength[i],'.2f'), lCrit))
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
    print('Segments overlap at: {}'.format(SegFlat[np.where((np.diff(SegFlat) > 0)==False)]))
else:
    print('No segments overlap')
    

"Checks if each line in the linemask is in a segment."
InSegFlag = True 
for i in range(len(lmask)):
    InSegCheck = np.any((lmask[i,1]>segment[:,0])&(lmask[i,2]<segment[:,1]))
    if InSegCheck == False:
        print('Linemask for {} is not contained within a segment'.format(lmask[i,0]))
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
    print('Continuummasks overlap at: {}'.format(ContFlat[np.where(np.diff(ContFlat) < 0)[0]]))
    ContFlag = False
if ContFlatCheck == True:
    print('No continuummasks overlap')


"Checks  if continuummask intersects segment edges. This definitely causes errors."
for i in range(len(contmask)):
    ContCheck = np.any([(contmask[i,0]<segment[:,1])&(contmask[i,1]>segment[:,1]),(contmask[i,0]<segment[:,0])&(contmask[i,1]>segment[:,0])],axis=1)
    if np.any(ContCheck) == True:
        InterruptedSegment = np.where((contmask[i,0]<segment[:,1])&(contmask[i,1]>segment[:,1]) | (contmask[i,0]<segment[:,0])&(contmask[i,1]>segment[:,0]))[0]
        for j in range(len(InterruptedSegment)):
            print('Continuummask {} intersects the segmentborder at {}'.format(contmask[i],segment[InterruptedSegment][j]))
        ContFlag = False


"Checks  if continuummask intersects linemask edges. Not sure if it causes errors, but it would seem counterintuitive that a section is both line and continuum."
for i in range(len(contmask)):
    ContLineCheck = np.any([(contmask[i,0]<lmask[:,2])&(contmask[i,1]>lmask[:,2]),(contmask[i,0]<lmask[:,1])&(contmask[i,1]>lmask[:,1])],axis=1)
    if np.any(ContLineCheck) == True:
        InterruptedLine = np.where((contmask[i,0]<lmask[:,2])&(contmask[i,1]>lmask[:,2]) | (contmask[i,0]<lmask[:,1])&(contmask[i,1]>lmask[:,1]))[0]
        for j in range(len(InterruptedLine)):
            print('Continuummask at {} intersects the linemask for {}'.format(contmask[i], lmask[InterruptedLine,0][j]))
        ContFlag = False


"Anything wrong?"
if ContFlag == True:
    print('No issues found in the continuummasks\n')  


"____________________________________Status report__________________________________"
if (LmaskFlag & SegCheck & InSegFlag & ContFlag ) == True:
    print('No issues found in the masks')


"____________________________________Linelist check__________________________________"
update = 'update'

while True:
    try:
        ynq = input('Do you want to check the linelist? [y/n]: ')
    except NameError:
        print('Input not recogniced')
        continue
    break

if ynq in ['n','N','no','No','NO']:
    raise SystemExit('Linelist not checked')
elif ynq == 'update':
    LineListName = input('Linelist name: ')
else:
    print('Checking linelist...')
    
NoLinesFlag = False
MultLinesFlag = False


"______________________________Reads in linelist_____________________________________"

while True:
    try:
        from LineListReader import LL_reader
        from strength import strength
        ll = LL_reader(LL_name,LL_dir,write=False,element=element)
    except ModuleNotFoundError:
        raise SystemExit('Missing modules for linelist reading and weak-line approximation, download from https://github.com/mablscmo/SME_Scripts/ or check that PYTHONPATH can find them.')
    except FileNotFoundError:
        print("The linelist {} was not found, try another or press 'q' to quit".format(LineListName))
        LL_name = input('Linelist name: ')
        if LL_name == 'quit':
            raise SystemExit('Linelist not checked')
        continue        
    except OSError:
        print("The linelist {} was not found, try another or press 'q' to quit".format(LineListName))
        LL_name = input('Linelist name: ')
        if LL_name == 'quit':
            raise SystemExit('Linelist not checked')
        continue
    break
        
#ll['Ele'] = ll.EleIon.apply(lambda x: x.strip("'").split()[0])
ll['strength'] = strength(ll['loggf'],ll['ExcLow'])
ll = ll.drop(columns=['JLow', 'ExcHigh', 'JHigh', 'LandLower','LandUpper','LandMean','RadDamping','StarkDamp','WaalsDamp','CentralDepth','LS1', 'base1', 'end1', 'LS2', 'base2','end2', 'ref'])

"_______________________Checks linelist and writes report file_______________________"
'''Goes through ther linemask to identify which lines are of interest. If there are multiple lines, it lets yuo know and adds the lines
to a report file. Also alerts and writes down linemasks that do not contain any lines of the correct element.'''

ReportFile = open("{}_report.txt".format(element),"w+")


MultLineCount = 0
NoLineCount = 0
Tolerance = 100
TolCount = 0
for i in range(len(lmask)):
    start = lmask[i,1]
    stop = lmask[i,2]
    LinesInMask = ll[(ll['LambdaAir']>=start) & (ll['LambdaAir']<=stop)]
    if len(LinesInMask) > 1:
        print('Multiple lines in linemask {}:'.format(lmask[i,0]))
        print(LinesInMask)
        MaxStrength = LinesInMask.strength.max()
        ReportFile.write('Multiple lines in linemask {}:\n'.format(lmask[i,0]))
        for i in range(len(LinesInMask)):
            StrengthFlag = ''
            if LinesInMask.strength.iloc[i] == MaxStrength:
                StrengthFlag = '***'
            elif LinesInMask.strength.iloc[i] > MaxStrength/Tolerance:
                StrengthFlag = '*'
                TolCount += 1
            InLine = LinesInMask.values[i]
            ReportFile.write("{0: <8}   lam_air: {1} AA     log gf:{2: >8}     Exc:{3: >7} eV     strength: {4}  {5}\n".format(InLine[0], format(InLine[1],'.3f'), format(InLine[2],'.3f'), format(InLine[3],'.3f'), "{:.3e}".format(InLine[4]), StrengthFlag))
        MultLinesFlag = True
        MultLineCount += 1
        ReportFile.write("\n")
    if len(LinesInMask) == 0:
        print('No line found in the linelist for linemask at {}'.format(lmask[i,0]))
        ReportFile.write('No line found in the linelist for linemask at {}\n'.format(lmask[i,0]))
        NoLinesFlag = True
        NoLineCount += 1
        ReportFile.write("\n")
        
if MultLinesFlag == False:
    ReportFile.write('No additional lines found within the linemasks\n')
else:
    ReportFile.write('{count}/{tot} linemasks with multiple lines\n'.format(count=MultLineCount, tot = len(lmask)))
    ReportFile.write('{} linemasks contain secondary lines crossing the strength threshold of 1/{}\n'.format(TolCount,Tolerance))

if NoLinesFlag == False:
    ReportFile.write('No linemasks without lines\n')
else:
    ReportFile.write('{count}/{tot} linemasks without lines'.format(count=NoLineCount, tot = len(lmask)))

ReportFile.close()

"_____________________________________Final status___________________________________"
print('\n')
if MultLinesFlag == False:
    print('No additional lines found within the linemasks')
else:
    print('{count}/{tot} linemasks with multiple lines'.format(count=MultLineCount, tot = len(lmask)))
    print('{} secondary lines cross the strength threshold of 1/{}'.format(TolCount,Tolerance))

if NoLinesFlag == False:
    print('No linemasks without lines')
else:
    print('{count}/{tot} linemasks without lines'.format(count=NoLineCount, tot = len(lmask)))
