#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:30:13 2021

@author: dennisbrookner
"""
#import pandas as pd
import string
import numpy as np
from copy import deepcopy

def screen(row, col, maxwell, **kwargs):
    #print("Reminder: 'row' is the parameter encoded by the row name, not the parameter that varies across a row")
    
    screen = {'row':row,
              'col':col,
              'maxwell':maxwell}
    
    screen['screenstatics'] = {}
    
    for key, value in kwargs.items():
        screen['screenstatics'][key] = value
        
    return(screen)

def tray(screen, tray, **kwargs):
        
    screen[tray] = {}
        
    screen[tray]['traystatics'] = {}
    
    rows = kwargs.pop('rows', None)
    if rows is not None:
        screen = setrows(screen, tray, rows)
        
    cols = kwargs.pop('cols', None)
    if cols is not None:
        screen = setcols(screen, tray, cols)
        
    for key, value in kwargs.items():
        screen[tray]['traystatics'][key] = value
    
    return screen

def clonetray(screen, oldtray, newtray, **kwargs):
    
    screen[newtray] = deepcopy(screen[oldtray])
    
    for key, value in kwargs.items():
        screen[newtray]['traystatics'][key] = value
        
    return screen

def setrows(screen, tray, *args):

    numrows = string.ascii_uppercase.find(screen['maxwell'][0])+1
    
    rownames = [i for i in string.ascii_uppercase[:numrows]]
    
    #print(args)
    rowdata = rowcolparser(numrows, args)
    
    for name, data in zip(rownames, rowdata):
       screen[tray][name] = data
    
    return screen

def setcols(screen, tray, *args):       
   
    numcols = int(screen['maxwell'][1])
    
    colnames = [str(i) for i in range(1,numcols+1)]
    
    coldata = rowcolparser(numcols, args)

    for name, data in zip(colnames, coldata):
       screen[tray][name] = data
    
    return screen    

def rowcolparser(n, args):
    #print(args)
    if len(args) == n:
        data = args
    elif len(args) == 2:
        data = np.linspace(args[0], args[1], n)
    elif len(args) == 1:
        if len(args[0]) == n:
            data = args[0]
        elif len(args[0]) == 2:
            data = np.linspace(args[0][0], args[0][1], n)
        elif len(args[0]) == 1:
            data = args[0] * n
            print(data)

    #print(data)    
    return data


def main():
    
    screen1 = screen('protein', 'PEG', 'H6', construct='wt DHFR')
    screen1 = tray(screen1, 'DB1', date='2021', rows = [3,10],
                      cols = [4,9])
    
    #screen1 = newtray(screen1, 'DB1', date='2021', rows = [10])

    #screen1 = setrows(screen1, 'DB1', 3, 10)
    #screen1 = setcols(screen1, 'DB1', 4, 9)
    
    screen1 = clonetray(screen1, 'DB1', 'DB2', season='spring')
    #screen1 = setrows(screen1, 'DB2', [1,2,3,5,6.7,5.5,1,16])

    print(screen1['DB1'])

    return

if __name__ == '__main__': main()
