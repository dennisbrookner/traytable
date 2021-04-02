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
    '''
    Create a screen with global parameters and which can contain trays

    Parameters
    ----------
    row : string
        Parameter encoded by the row letter
    col : string
        Parameter encoded by the column number
    maxwell : string
        Name of the well in the bottom-right corner of each tray, e.g. 'H6'
    **kwargs : any type
        Any named arguments become global parameters applied to all wells in all trays in the screen

    Returns
    -------
    screen : dict
        A dictionary containing the screen and to which trays can be added

    '''
    
    screen = {'row':row,
              'col':col,
              'maxwell':maxwell}
    
    screen['screenstatics'] = {}
    
    for key, value in kwargs.items():
        screen['screenstatics'][key] = value
        
    return screen

def tray(screen, tray, **kwargs):
    '''
    Create a tray and add it to your screen

    Parameters
    ----------
    screen : dict
        Screen to which a tray is being added
    tray : string
        Name of the tray being created
    **kwargs : any type
        Special kwargs 'rows' and 'cols' are passed to setrows() and setcols() respectively.
        All other kwargs become parameters that apply to all wells in the tray

    Returns
    -------
    screen : dict
        Screen including the newly added tray

    '''
        
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
    '''
    Copy a tray, overriding parameters as desired

    Parameters
    ----------
    screen : dict
        Screen containing the tray to be copied
    oldtray : string
        Name of tray to be copied
    newtray : string
        Name of new tray to be created 
    **kwargs : any type
        Accepts all arguments accepted by tray(). 
        Any parameters extant in oldtray not specified here will be copied into newtray

    Returns
    -------
    screen : dict
        Screen containing oldtray and newtray

    '''
    
    screen[newtray] = deepcopy(screen[oldtray])
    
    rows = kwargs.pop('rows', None)
    if rows is not None:
        screen = setrows(screen, newtray, rows)
        
    cols = kwargs.pop('cols', None)
    if cols is not None:
        screen = setcols(screen, newtray, cols)
    
    for key, value in kwargs.items():
        screen[newtray]['traystatics'][key] = value
        
    return screen

def setrows(screen, tray, *args):
    '''
    Set values encoded by row names, e.g. the values static across each row

    Parameters
    ----------
    screen : dict
        Screen containing the tray to which rows will be added.
    tray : string
        Name of tray to which rows will be added.
    *args : list or float
        Row values can be passed as one number to apply to all rows, 
        numrows numbers to map directly to rows, or
        two numbers to create an evenly spaced gradient across the rows

    Returns
    -------
    screen : dict
        Screen containing the tray to which rows have been added

    '''

    numrows = string.ascii_uppercase.find(screen['maxwell'][0])+1
    
    rownames = [i for i in string.ascii_uppercase[:numrows]]
    
    #print(args)
    rowdata = rowcolparser(numrows, args)
    
    for name, data in zip(rownames, rowdata):
       screen[tray][name] = data
    
    return screen

def setcols(screen, tray, *args):  
    '''
    Set values encoded by column names, e.g. the values static down each column

    Parameters
    ----------
    screen : dict
        Screen containing the tray to which columns will be added.
    tray : string
        Name of tray to which columns will be added.
    *args : list or float
        Column values can be passed as one number to apply to all columns, 
        numcols numbers to map directly to columns, or
        two numbers to create an evenly spaced gradient across the columns

    Returns
    -------
    screen : dict
        Screen containing the tray to which columns have been added

    '''     
   
    numcols = int(screen['maxwell'][1])
    
    colnames = [str(i) for i in range(1,numcols+1)]
    
    coldata = rowcolparser(numcols, args)

    for name, data in zip(colnames, coldata):
       screen[tray][name] = data
    
    return screen    

def rowcolparser(n, *args):
    '''
    Helper function not exported
    '''
    
    if len(args) == n:
        data = args
    elif len(args) == 2:
        data = np.linspace(args[0], args[1], n)
    elif len(args) == 1:
        if type(args[0]) is int or type(args[0]) is float:
            data = [args[0]] * n
        elif len(args[0]) == n:
            data = args[0]
        elif len(args[0]) == 2:
            data = np.linspace(args[0][0], args[0][1], n)
        elif len(args[0]) == 1:
            if type(args[0][0]) is int or type(args[0][0]) is float:
                data = [args[0][0]] * n
            elif len(args[0][0]) == n:
                data = args[0][0]
            elif len(args[0][0]) == 2:
                data = np.linspace(args[0][0][0], args[0][0][1], n)
            elif len(args[0][0]) == 1:
                data = args[0][0] * n
                #print(data)
            else:
                raise ValueError("Unexpected row/column specification")

    
    return data


def main():
    
    screen1 = screen('protein', 'PEG', 'H6', construct='wt DHFR')
    
    screen1 = tray(screen1, 'DB1', rows = 3, cols = [4])
    screen1 = setrows(screen1, 'DB1', 3)
    screen1 = setrows(screen1, 'DB1', [3])
    
    screen1 = tray(screen1, 'DB2', rows = [1,8], cols = [1, 2, 3, 4, 5, 6])
    screen1 = setrows(screen1, 'DB2', 1, 8)
    screen1 = setcols(screen1, 'DB2', 1,2,3,4,5,8)

    #screen1 = newtray(screen1, 'DB1', date='2021', rows = [10])

    #screen1 = setrows(screen1, 'DB1', 3)
    #screen1 = setcols(screen1, 'DB1', 4, 9)
    
    #screen1 = clonetray(screen1, 'DB1', 'DB2', season='spring', rows=5)
    #screen1 = setrows(screen1, 'DB2', [1,2,3,5,6.7,5.5,1,16])

    print(screen1)

    return

if __name__ == '__main__': main()
