"""
-----------------------------------------
Created on 2020-03-22
author: Martin Montelius
Version: 0.3.2
-----------------------------------------
Text info for the PlotAbundances code
"""

#Header for the pandas directory, should probably have more descriptive names than 2 3 4 5 6 7.. but I'm not sure what they do
SME_Header = ['Star','1','Instrument','Vband','Jband','Hband','Kband','Date','exptime','Original name for object','min (wave)',
              'max (wave)','R','Vhelio','Vrad','RA (GDR2)','dec (GDR2)','pmra (GDR2)','epmra (GDR2)','pmdec (GDR2)','epmdec (GDR2)',
              'parallax (GDR2)','eparallax (GDR2)','d (GDR2)','ed (GDR2)','Ed (GDR2)','d (McM)','ed (McM)','Population','2MASS','SNR','Teff',
              'Teff2','Teff3','Teff4','Teff5','Teff6','Teff7','logg','logg2','logg3','logg4','logg5','logg6','logg7','[Fe/H]','[Fe/H]2','[Fe/H]3',
              '[Fe/H]4','[Fe/H]5','[Fe/H]6','[Fe/H]7','vmic','vmic2','vmic3','vmic4','vmic5','vmic6','vmic7','vmac','vmac2','vmac3','vmac4','vmac5',
              'vmac6','vmac7','vsini','vsini2','vsini3','vsini4','vsini5','vsini6','vsini7','vrad-adjustment','vrad-adjustment2','vrad-adjustment3',
              'vrad-adjustment4','vrad-adjustment5','vrad-adjustment6','vrad-adjustment7','Li','Li2','Li3','Li4','Li5','Li6','Li7','Be','Be2','Be3',
              'Be4','Be5','Be6','Be7','B','B2','B3','B4','B5','B6','B7','C','C2','C3','C4','C5','C6','C7','N','N2','N3','N4','N5','N6','N7','O','O2',
              'O3','O4','O5','O6','O7','F','F2','F3','F4','F5','F6','F7','Ne','Ne2','Ne3','Ne4','Ne5','Ne6','Ne7','Na','Na2','Na3','Na4','Na5','Na6',
              'Na7','Mg','Mg2','Mg3','Mg4','Mg5','Mg6','Mg7','Al','Al2','Al3','Al4','Al5','Al6','Al7','Si','Si2','Si3','Si4','Si5','Si6','Si7','P',
              'P2','P3','P4','P5','P6','P7','S','S2','S3','S4','S5','S6','S7','Cl','Cl2','Cl3','Cl4','Cl5','Cl6','Cl7','Ar','Ar2','Ar3','Ar4','Ar5',
              'Ar6','Ar7','K','K2','K3','K4','K5','K6','K7','Ca','Ca2','Ca3','Ca4','Ca5','Ca6','Ca7','Sc','Sc2','Sc3','Sc4','Sc5','Sc6','Sc7','Ti',
              'Ti2','Ti3','Ti4','Ti5','Ti6','Ti7','V','V2','V3','V4','V5','V6','V7','Cr','Cr2','Cr3','Cr4','Cr5','Cr6','Cr7','Mn','Mn2','Mn3','Mn4',
              'Mn5','Mn6','Mn7','Co','Co2','Co3','Co4','Co5','Co6','Co7','Ni','Ni2','Ni3','Ni4','Ni5','Ni6','Ni7','Cu','Cu2','Cu3','Cu4','Cu5','Cu6',
              'Cu7','Zn','Zn2','Zn3','Zn4','Zn5','Zn6','Zn7','Ga','Ga2','Ga3','Ga4','Ga5','Ga6','Ga7','Ge','Ge2','Ge3','Ge4','Ge5','Ge6','Ge7','Kr',
              'Kr2','Kr3','Kr4','Kr5','Kr6','Kr7','Rb','Rb2','Rb3','Rb4','Rb5','Rb6','Rb7','Sr','Sr2','Sr3','Sr4','Sr5','Sr6','Sr7','Y','Y2','Y3',
              'Y4','Y5','Y6','Y7','Zr','Zr2','Zr3','Zr4','Zr5','Zr6','Zr7','Nb','Nb2','Nb3','Nb4','Nb5','Nb6','Nb7','Mo','Mo2','Mo3','Mo4','Mo5',
              'Mo6','Mo7','Ru','Ru2','Ru3','Ru4','Ru5','Ru6','Ru7','Pd','Pd2','Pd3','Pd4','Pd5','Pd6','Pd7','In','In2','In3','In4','In5','In6','In7',
              'Ba','Ba2','Ba3','Ba4','Ba5','Ba6','Ba7','La','La2','La3','La4','La5','La6','La7','Ce','Ce2','Ce3','Ce4','Ce5','Ce6','Ce7','Pr','Pr2',
              'Pr3','Pr4','Pr5','Pr6','Pr7','Nd','Nd2','Nd3','Nd4','Nd5','Nd6','Nd7','Sm','Sm2','Sm3','Sm4','Sm5','Sm6','Sm7','Eu','Eu2','Eu3','Eu4',
              'Eu5','Eu6','Eu7','Gd','Gd2','Gd3','Gd4','Gd5','Gd6','Gd7','Dy','Dy2','Dy3','Dy4','Dy5','Dy6','Dy7','Tm','Tm2','Tm3','Tm4','Tm5','Tm6',
              'Tm7','Yb','Yb2','Yb3','Yb4','Yb5','Yb6','Yb7']

DROP_LIST = ['Star','1','Instrument','Vband','Jband','Hband','Kband','Date','exptime','Original name for object','min (wave)',
              'max (wave)','R','Vhelio','Vrad','RA (GDR2)','dec (GDR2)','pmra (GDR2)','epmra (GDR2)','pmdec (GDR2)','epmdec (GDR2)',
              'parallax (GDR2)','eparallax (GDR2)','d (GDR2)','ed (GDR2)','Ed (GDR2)','d (McM)','ed (McM)','Population','2MASS','SNR','Teff',
              'Teff2','Teff3','Teff4','Teff5','Teff6','Teff7','logg','logg2','logg3','logg4','logg5','logg6','logg7','[Fe/H]2','[Fe/H]3',
              '[Fe/H]4','[Fe/H]5','[Fe/H]6','[Fe/H]7','vmic','vmic2','vmic3','vmic4','vmic5','vmic6','vmic7','vmac','vmac2','vmac3','vmac4','vmac5',
              'vmac6','vmac7','vsini','vsini2','vsini3','vsini4','vsini5','vsini6','vsini7','vrad-adjustment','vrad-adjustment2','vrad-adjustment3',
              'vrad-adjustment4','vrad-adjustment5','vrad-adjustment6','vrad-adjustment7','Li2','Li3','Li4','Li5','Li6','Li7','Be2','Be3',
              'Be4','Be5','Be6','Be7','B2','B3','B4','B5','B6','B7','C2','C3','C4','C5','C6','C7','N2','N3','N4','N5','N6','N7','O2',
              'O3','O4','O5','O6','O7','F2','F3','F4','F5','F6','F7','Ne2','Ne3','Ne4','Ne5','Ne6','Ne7','Na2','Na3','Na4','Na5','Na6',
              'Na7','Mg2','Mg3','Mg4','Mg5','Mg6','Mg7','Al2','Al3','Al4','Al5','Al6','Al7','Si2','Si3','Si4','Si5','Si6','Si7',
              'P2','P3','P4','P5','P6','P7','S2','S3','S4','S5','S6','S7','Cl2','Cl3','Cl4','Cl5','Cl6','Cl7','Ar2','Ar3','Ar4','Ar5',
              'Ar6','Ar7','K2','K3','K4','K5','K6','K7','Ca2','Ca3','Ca4','Ca5','Ca6','Ca7','Sc2','Sc3','Sc4','Sc5','Sc6','Sc7',
              'Ti2','Ti3','Ti4','Ti5','Ti6','Ti7','V2','V3','V4','V5','V6','V7','Cr2','Cr3','Cr4','Cr5','Cr6','Cr7','Mn2','Mn3','Mn4',
              'Mn5','Mn6','Mn7','Co2','Co3','Co4','Co5','Co6','Co7','Ni2','Ni3','Ni4','Ni5','Ni6','Ni7','Cu2','Cu3','Cu4','Cu5','Cu6',
              'Cu7','Zn2','Zn3','Zn4','Zn5','Zn6','Zn7','Ga2','Ga3','Ga4','Ga5','Ga6','Ga7','Ge2','Ge3','Ge4','Ge5','Ge6','Ge7',
              'Kr2','Kr3','Kr4','Kr5','Kr6','Kr7','Rb2','Rb3','Rb4','Rb5','Rb6','Rb7','Sr2','Sr3','Sr4','Sr5','Sr6','Sr7','Y2','Y3',
              'Y4','Y5','Y6','Y7','Zr2','Zr3','Zr4','Zr5','Zr6','Zr7','Nb2','Nb3','Nb4','Nb5','Nb6','Nb7','Mo2','Mo3','Mo4','Mo5',
              'Mo6','Mo7','Ru2','Ru3','Ru4','Ru5','Ru6','Ru7','Pd2','Pd3','Pd4','Pd5','Pd6','Pd7','In2','In3','In4','In5','In6','In7',
              'Ba2','Ba3','Ba4','Ba5','Ba6','Ba7','La2','La3','La4','La5','La6','La7','Ce2','Ce3','Ce4','Ce5','Ce6','Ce7','Pr2',
              'Pr3','Pr4','Pr5','Pr6','Pr7','Nd2','Nd3','Nd4','Nd5','Nd6','Nd7','Sm2','Sm3','Sm4','Sm5','Sm6','Sm7','Eu2','Eu3','Eu4',
              'Eu5','Eu6','Eu7','Gd2','Gd3','Gd4','Gd5','Gd6','Gd7','Dy2','Dy3','Dy4','Dy5','Dy6','Dy7','Tm2','Tm3','Tm4','Tm5','Tm6',
              'Tm7','Yb2','Yb3','Yb4','Yb5','Yb6','Yb7']

APOGEE_Header = ['2MASS','[Fe/H]','Teff','logg','Na','Mg','Si','S','P','K','Ca','Ti','V','Cr','Mn','Co','Ni','Cu','Ce','Al','NaH','MgH','SiH','PH',
                 'SH','KH','CaH','TiH','VH','CrH','MnH','CoH','NiH','CuH','CeH','AlH','FFe','FNaH','FNa','FMg','FMgH','FSi','FSiH','FPH','FP','FS',
                 'FSH','FKH','FK','FCa','FCaH','FTi','FTiH','FVH','FV','FCrH','FCr','FMnH','FMn','FCoH','FCo','FNiH','FNi','FCuH','FCu','FCeH','FCe',
                 'FAlH','FAl','SNR']

#Element names
Elements = ['Al','C','Ca','Ce','Co','Cr','Cu','Fe','Ge','HF','K','Mg','Mn','Na','Nd','Ni','P','Rb','S','Sc','Si','Ti','V','Y','Yb']
al,c,ca,ce,co,cr,cu,fe,ge,hf,k,mg,mn,na,nd,ni,p,rb,s,sc,si,ti,v,y,yb = Elements
Al,C,Ca,Ce,Co,Cr,Cu,Fe,Ge,Hf,K,Mg,Mn,Na,Nd,Ni,P,Rb,S,Sc,Si,Ti,V,Y,Yb = Elements

Groups = ['Alpha', 'Odd', 'Iron_peak', 'Neutron_capture']
alpha, odd, ironpeak, neutroncapture = Groups
Alpha, Odd, iron, neutron = Groups

PlotInput = Elements + Groups

#Commands
q = 'quit'


#Comparison details
CompLabel = ['Optical', 'Ivalu', 'APOGEE']
Colours = ['royalblue', 'crimson', 'forestgreen']#darkviolet


#Elements within groups
AlphaElements = ['Si','Mg','S','Ca']
OddElements = ['Al', 'Na']
IronElements = ['Ni','Cr']
NeutronElements = []


#Diagnostics
Diagnostics = ['diagnostics', 'Teff', 'logg', 'vmic', '[Fe/H]']

diag, teff, logg, vmic, metal = Diagnostics

DiagLimits = [[4000,5250],[1.15,3.6],[1.1,2.0],[-1.2,0.4]]

DiagColours = ['crimson', 'teal', 'forestgreen', 'saddlebrown']

diagFlag = False



