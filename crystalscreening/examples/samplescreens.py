import crystalscreening.screens as cs

screen1 = cs.newscreen('protein', 'PEG', 'H6', construct='wt DHFR', buffer='imidazole')
screen1 = cs.newtray(screen1, 'tray1', date='2021-01-01', pH=5.4, additive='NaOAc')
screen1 = cs.setrows(screen1, 'tray1', 4, 18)
screen1 = cs.setcols(screen1, 'tray1', 16, 21)

screen1 = cs.newtray(screen1, 'tray2', date='2021-01-03', pH=5.6, other='humid day')
screen1 = cs.setrows(screen1, 'tray2', 10, 17)
screen1 = cs.setcols(screen1, 'tray2', 15, 20)

screen1 = cs.clonetray(screen1, 'tray2', 'tray3', date='2021-01-04')
screen1 = cs.setrows(screen1, 'tray3', 11, 18)

# samplescreen1 = {}
# samplescreen1['row'] = 'protein'
# samplescreen1['column'] = 'PEG'
# samplescreen1['statics'] = ['PEGtype', 'buffer', 'salt', 'pH', 'date', 'solutionsetname']
# samplescreen1['maxwell'] = 'H6'

# samplescreen1['tray1'] = { 'A': 4, # assuming units of mg/ml; this could be specified as a static parameter if desired
#                      'B': 6,
#                      'C': 8,
#                      'D': 10,
#                      'E': 12,
#                      'F': 14,
#                      'G': 16,
#                      'H': 18,
               
#                      '1': 16, # assuming units of %
#                      '2': 17,
#                      '3': 18,
#                      '4': 19,
#                      '5': 20,
#                      '6': 21,
           
#                      'PEGtype': 400,
#                      'buffer': 'imidazole 20mM', # buffer identity and buffer concentration could be separate parameters
#                      'salt': 'MnCl2 125mM', # salt identity and buffer concentration could be separate parameters
#                      'pH': 5.8,
#                      'date': '2021-02-02',
#                      'solutionsetname': 'firsttry'}
                     
# samplescreen1['tray2'] = { 'A': 10,
#                      'B': 11,
#                      'C': 12,
#                      'D': 13,
#                      'E': 14,
#                      'F': 15,
#                      'G': 16,
#                      'H': 17,
               
#                      '1': 15,
#                      '2': 16,
#                      '3': 17,
#                      '4': 18,
#                      '5': 19,
#                      '6': 20,
           
#                      'PEGtype': 400,
#                      'buffer': 'imidazole 20mM',
#                      'salt': 'MnCl2 125mM',
#                      'pH': 5.8,
#                      'date': '2021-02-02',
#                      'solutionsetname': 'secondtry'}
