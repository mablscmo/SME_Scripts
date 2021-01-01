# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:48:30 2021

@author: monte
"""
import numpy as np

def strength(gf, exc, T=5770):
    '''Determines the strength of spectral lines using the weak-line approximation. Only works for lines of the same element
    and ionisationstage. Takes the gf value and the excitation energy as inputs, temperature is also needed, set to 5770 by 
    default to mimic the Sun. '''
    return((10**gf)*np.exp(-exc/(T*8.6173*10**-5)))
