screens = {}
screens['row'] = 'protein'
screens['column'] = 'PEG'
screens['statics'] = ['PEGtype', 'buffer', 'salt', 'pH', 'date', 'solutionsetname']
screens['maxwell'] = 'H6'

screens['tray1'] = { 'A': 4, # assuming units of mg/ml; this could be specified as a static parameter if desired
                     'B': 6,
                     'C': 8,
                     'D': 10,
                     'E': 12,
                     'F': 14,
                     'G': 16,
                     'H': 18,
               
                     '1': 16, # assuming units of %
                     '2': 17,
                     '3': 18,
                     '4': 19,
                     '5': 20,
                     '6': 21,
           
                     'PEGtype': 400,
                     'buffer': 'imidazole 20mM', # buffer identity and buffer concentration could be separate parameters
                     'salt': 'MnCl2 125mM', # salt identity and buffer concentration could be separate parameters
                     'pH': 5.8,
                     'date': '2021-02-02',
                     'solutionsetname': 'firsttry'}
                     
screens['tray2'] = { 'A': 10,
                     'B': 11,
                     'C': 12,
                     'D': 13,
                     'E': 14,
                     'F': 15,
                     'G': 16,
                     'H': 17,
               
                     '1': 15,
                     '2': 16,
                     '3': 17,
                     '4': 18,
                     '5': 19,
                     '6': 20,
           
                     'PEGtype': 400,
                     'buffer': 'imidazole 20mM',
                     'salt': 'MnCl2 125mM',
                     'pH': 5.8,
                     'date': '2021-02-02',
                     'solutionsetname': 'secondtry'}
