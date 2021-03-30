# CrystalScreening
#### Jupyter notebooks for organizing crystallization screening results
When logging crystal hits, the only information necessary to log should be tray, well, and crystal quality: information about crystallization conditions is entirely encoded by the tray and well. This repo is a template for storing all of your tray information as a dictionary of dictionaries, and accessing those dictionaroes to log your crystal hits in a `pandas` dataframe.  
  
Start by editing the dictionary of dictionaries to contain your tray information. The easiest (and most typical) case is where you always vary the same component across rows and columns. Indicate these conditions, along with the other "static" conditions that are the same for entire trays. Finally, indicate tray shape via the "maximum well," e.g. H6 for a 48-well plate. A typical example might look like this:
```python
screens = {}
screens['row'] = 'protein'
screens['column'] = 'PEG'
screens['statics'] = ['PEGtype', 'buffer', 'salt', 'pH', 'date', 'solutionsetname']
screens['maxwell'] = 'H6'
```
This is a little tedious, but you should only have to do it once!  
  
Then, you set two trays, with slightly different %PEG vs. [protein] screens, and log each tray as a dictionary within your main dictionary:
```python
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
                     'solutionsetname': 'firsttry'}
```
Typically, I like to `pickle` this dictionary for safekeeping and easy access in other files, but for now we'll just press on.  
  
This package provides a function `well()` to automate the retrieval of information from these dictionaries. 
```python
from crystalscreening import well

df = well(tray='tray1', well='B3', quality='good')
```
Add more rows to your dataframe with the `old_df` flag:
```python
df = well(tray='tray1', well='B4', quality='needles', old_df=df)
```
Or if there are many wells from the same plate with crystals of the same quality, log them all in one function call:
```python
df = well(tray='tray1', well=['A2', 'A3', 'A4', 'B2', 'B5'], quality='good')
```
