import traytable as tt
import matplotlib.pyplot as plt


myscreen = tt.screen(row = 'protein', col = 'PEG', maxwell = 'H6', 
                     construct = 'HEWL', buffer = 'imidazole 20mM')


tray1 = tt.tray(myscreen, date = '2021-01-01', pH = 5.8,
                rows = [4,18],
                cols = [20,25])


tray2 = tt.clonetray(tray1, date = '2021-01-03',
                     rows = [4, 5, 6, 7, 8, 10, 12, 14])


df = tt.well(tray1, 'A6', 'good', quantity = 3)
df = tt.well(tray1, 'B6', 'good', quantity = 2, note = "chunkier than usual", old_df=df)
df = tt.well(tray1, 'C6', 'needles', old_df=df)


df


df = tt.well(tray2, ['B3', 'C3', 'D3', 'E3'], 'needles', old_df=df)
df = tt.well(tray2, ['A5', 'A6', 'B5'], 'good', old_df=df, note='borderline')
df


colordict= {'good':'green',
            'needles':'gray'}
df.plot.scatter('protein', 'PEG', alpha=0.6, c=df.quality.map(colordict))
plt.title('What [protein] vs. get_ipython().run_line_magic("PEG", " gives the best crystals?')")
plt.show()


import traytable as tt
import matplotlib.pyplot as plt

# make trays
myscreen = tt.screen(row = 'protein', col = 'PEG', maxwell = 'H6', 
                     construct = 'HEWL', buffer = 'imidazole 20mM')
tray1 = tt.tray(myscreen, date = '2021-01-01', pH = 5.8,
                rows = [4,18],
                cols = [20,25])
tray2 = tt.clonetray(tray1, date = '2021-01-03',
                     rows = [4, 5, 6, 7, 8, 10, 12, 14])

# log results
df = tt.well(tray1, 'A6', 'good', quantity = 3)
df = tt.well(tray1, 'B6', 'good', quantity = 2, note = "chunkier than usual", old_df=df)
df = tt.well(tray1, 'C6', 'needles', old_df=df)
df = tt.well(tray2, ['B3', 'C3', 'D3', 'E3'], 'needles', old_df=df)
df = tt.well(tray2, ['A5', 'A6', 'B5'], 'good', old_df=df, note='borderline')

# plot results
colordict= {'good':'green',
            'needles':'gray'}
df.plot.scatter('protein', 'PEG', alpha=0.6, c=df.quality.map(colordict))
plt.title('What [protein] vs. get_ipython().run_line_magic("PEG", " gives the best crystals?')")
plt.show()
