#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dennisbrookner
"""
import pandas as pd
import string

def well(screen, tray, well, quality, old_df=None, **kwargs):
    '''
    Add one or more rows to a dataframe of crystal hits

    Parameters
    ----------
    screen : dict
        Screen dictionary, as created by traytable.screen(), trayable.tray()
    tray : string
        Tray name
    well : string
        Well name, in format [letter][number]
    quality : string
        Short description like "good" or "needles"
    old_df : pandas.core.frame.DataFrame, optional
        Working dataframe to append to. If None, creates a new dataframe.
    **kwargs : any type
        Any additional named arguments will become columns in the dataframe

    Raises
    ------
    TypeError
        Improper type for well name
    ValueError
        Row or column specified by 'well' is out of the range specified by screen['maxwell']

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Dataframe containing the new reults, optionally concatenated with old_df

    '''
    # to-do: check whether 'row' and 'column' are present in the tray dictionary, and if so, use that
    df = pd.DataFrame(columns = [screen['row']] + [screen['col']] 
                      + ['quality'] 
                      + list(screen[tray]['traystatics'].keys())
                      + list(screen['screenstatics'].keys())
                      + ['tray'] + ['well'])
    
    if type(well) == str:
        well = [well]
        
    if type(well) != list:
        raise TypeError('Improper type for well name')

    for w in well:
        
                
        if w[0] not in string.ascii_uppercase[:string.ascii_uppercase.find(screen['maxwell'][0])+1]:
            raise ValueError(f"Improper column specification: column is {w[0]}, should be one of {string.ascii_uppercase[:string.ascii_uppercase.find(screen['maxwell'][0])+1]}")
        
        if int(w[1]) not in range(1,int(screen['maxwell'][1])+1):
            raise ValueError(f"Improper row specification: row is {w[1]}, should be one of {list(range(1,int(screen['maxwell'][1])+1))}")
    
                
        df.loc[len(df.index)] = ([screen[tray][w[0]]] + [screen[tray][w[1]]]
                                 + [quality]
                                 + list(screen[tray]['traystatics'].values())
                                 + list(screen['screenstatics'].values())
                                 + [tray] + [w])
    
    if kwargs is not None:
        for key, value in kwargs.items():
            df[key] = value
    
    if old_df is not None:
        df = pd.concat([old_df, df], axis=0, ignore_index=True)
        #df = old_df.append(df)
        
    return df


def main():
    
    from traytable.samples import screen1 as screen
    
    df = well(screen, 'tray1', 'A2', 'good', note='newly appeared')
    df = well(screen, 'tray2', ['A1', 'A2', 'A3'], 'needles', old_df=df, note = 'not mountable yet')
    df = well(screen, 'tray3', 'G2', 'needles', old_df=df)
    
    #df = well(screen, 'tray3', 'J2', 'good')
    #df = well(screen, 'tray3', 'B7', 'good')
    
    print(df)

if __name__ == '__main__': main()
