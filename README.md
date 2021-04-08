# `traytable`
### A python package for tabulating crystallization results across many trays  
`traytable` provides methods for 
 - storing all information about a crystallization screen in a dictionary of dictionaries
 - extracting and tabulating all data about "hits" into a `pandas` dataframe.  

The goal of `traytable` is for all crystallization data to be inputted once and only once, and then conveniently looked up and reused whenever needed.

You can find a jupyter notebook with a brief demonstration of package functionality [here](https://github.com/dennisbrookner/traytable/blob/main/1_sample.ipynb).

#### Installation
```bash
pip install traytable
```
## Usage
A super brief example:
```python
import traytable as tt

myscreen = tt.screen(row='protein', col='PEG', maxwell='H6') # Each row is a different [protein], and each column is a different %PEG
tray1 = tt.tray(myscreen, rows=[1,8], cols=[10,20]) # Rows vary from 1 to 8, columns vary from 10 to 20
results = tt.well(tray1, 'A3', 'good') # there is a good crystal in well A3 of tray 1
results = tt.well(tray1, ['E4', 'E5'], 'needle', old_df=results) # there are needle-y crystals in wells E4 and E5 of tray 1
```
The return `results` from `tt.well()` is a `pandas` data frame where every crystal you've logged gets its own row, and every parameter you've indicated gets its own column. This makes it easy to keep track of the best conditions for your crystals across many trays with slightly different conditions. Note that upon logging your "hits", there's no need to input [protein] or %PEG; that information is already encoded by the tray and well you specified!  

### Required arguments
##### `tt.screen()` requires:
 - `row`: a string indicating the parameter that is encoded by each row in a tray
 - `col`: a string indicating the parameter that is encoded by each column in a tray
 - `maxwell`: a string indicating the name of the well in the bottom right corner of each tray. Any size tray is supported; however, currently, rows must be named with letters, and columns must be named with numbers
##### `tt.tray()` requires:
 - `screen`: The screen, as created by `tt.screen()`, that this tray should inherit parameters from. You can't create a tray without a screen.
 - `rows`: Specify the values to assign to each row with either a single number (to assign to all rows), a list of two numbers (to evenly space among the rows) or a list of numbers explicitly specifying a value for each row. With 8 rows, you might say `rows=5`, `rows=[1,8]` or `rows=[1,2,3,4,6,8,10,12]`.
 - `cols`: Specify values for columns, with the same format as for `rows`.
##### `tt.well()` requires:
 - `tray`: The tray
 - `well`: The well; must be a string of format '[letter][number]', and must fall into the range specified by the screen's `maxwell`
 - `quality`: Any type, though I recommend a short categorical string like 'good', 'bad', 'needles', or 'multilattice'
 - `old_df`: Not strictly required, but to append previous results, pass previous returns from `tt.well()` to the next call as `old_df = `
  
### Optional arguments
All three of these methods (`tt.screen()`, `tt.tray()`, and `tt.well()`) will accept any additional named arguments, and include them as columns in the final data frame. As you would expect, arguments passed to `tt.screen()` will apply to all wells in all trays in the screen, and arguments passed to `tt.tray()` will apply to all wells in that tray. For example:
```python
detailedscreen = tt.screen(row='protein', col='PEG', maxwell='H6', construct='HEWL', buffer='imidazole', bufferconc=20, salt='MnCl2', saltconc=125)
tray1 = tt.tray(detailedscreen, rows=[1,8], cols=[10,20], date='2021-01-01', setby='robot', weathernotes='very humid day') 
results = tt.well(tray1, 'A1', 'good', appxnum=3, notes='rod-shaped')
```

### Other things of note
#### The `clonetray()` method
To save some typing, you can create trays with `tt.clonetray()`. Usage is `newtray = tt.clonetray(oldtray, **kwargs)`. Any additional arguments passed to `clonetray()` will supercede the associated parameter from the parent tray. For example:
```python
# assume screen already exists
tray1 = tt.tray(screen, rows=[1,8], cols=[5,10], date='2021-01-02'
tray2 = tt.clonetray(tray1, date='2021-01-03')
```
#### Using `pandas` methods
As mentioned above, `tt.well()` returns a `pandas` dataframe. This means that you can use `pandas` methods and features as desired. One frequent usage might be printing out only select columns with bracket notation, or accessing a certain column with dot notation, e.g. 
```python
results[['protein', 'PEG', 'quality']]

import numpy as np
number_of_crystals = np.sum(results.appxnum())
```
You can also use the built-in plotting backend of `pandas`, which can be nifty to visualize what conditions are working best.
```python
results.plot.scatter('protein', 'PEG')
```
A slightly fancier plot:
```python
import numpy as np

results['proteinplot'] = results.protein +  np.random.normal(scale=0.15, size=len(results))
results['PEGplot'] = results.PEG +  np.random.normal(scale=0.15, size=len(results))

colordict= {'good':'green',
            'needles':'red'}

results.plot.scatter('proteinplot', 'PEGplot', alpha=0.5, c=results.quality.map(colordict))
```
