import pandas as pd

from crystalscreening.examples.samplescreens import screens

def well(tray, well, quality, old_df=None, screens=screens):
    
    #rowparam = screens['row']
    #colparam = screens['column']
    
    df = pd.DataFrame(columns = [screens['row']] + [screens['column']]
                      + ['quality'] + screens['statics'])
                      
                      #['protein', 'PEG', 'quality', 'tray', 'well', 'pH',
                       #          'buffer', 'bufferconc', 'salt', 'saltconc',
                        #         'date', 'ss'])
    
    #t = screens[tray]
    
    if type(well) == str:
        well = [well]
        
    if type(well) != list:
        raise TypeError('Improper type for well name')
    
    for w in well:
        
        #wstatics = [t[param] for param in screens['statics']]
        
        df.loc[len(df.index)] = [screens[tray][w[0]], screens[tray][w[1]], quality] + [screens[tray][param] for param in screens['statics']]
                                 #quality, tray, well,
                                 #t['pH'], t['buffer'], t['bufferconc'], t['salt'], t['saltconc'],
                                 #t['date'], t['ss']]
            
    if old_df is not None:
        df = old_df.append(df)
    
    return df


def main():
    df = well('tray1', 'A2', 'good')
    df = well('tray2', ['A1', 'A2', 'A3'], 'needles', old_df=df)
    print(df)

if __name__ == '__main__': main()
