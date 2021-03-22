def well(tray, well, quality, old_df=None, screens=d):
    
    df = pd.DataFrame(columns = ['protein', 'PEG', 'quality', 'tray', 'well', 'pH',
                                 'buffer', 'bufferconc', 'salt', 'saltconc',
                                 'date', 'ss'])
    
    d = dictionary[tray]
    
    if type(well) == str:
        wells = [wells]
        
    if type(wells) != list:
        raise TypeError('Improper format for well name')
    
    for well in wells:
        df.loc[len(df.index)] = [d[well[0]], d[well[1]],
                                 quality, tray, well,
                                 d['pH'], d['buffer'], d['bufferconc'], d['salt'], d['saltconc'],
                                 d['date'], d['ss']]
            
    if old_df is not None:
        df = old_df.append(df)
    
    return df
