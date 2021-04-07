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
The return `results` from `tt.well()` is a pandas data frame where every crystal you've logged gets its own row, and every parameter you've indicated gets its own column. This makes it easy to keep track of the best conditions for your crystals across many trays with slightly different conditions. Note that upon logging your "hits", there's no need to input [protein] or %PEG; that information is already encoded by the tray and well you specified.  

### Required arguments
##### `tt.screen()`
`tt.screen()` requires:
 - `row`: a string indicating the parameter that is encoded by each row in a tray
 - `col`: a string indicating the parameter that is encoded by each column in a tray
 - `maxwell`: a string indicating the name of the well in the bottom right corner of each tray. Any size tray is supported; however, currently, trays must be named with letters, and columns must be named with numbers
##### `tt.tray()`
`tt.tray()` requires:
 - `screen`: The screen, as created by `tt.screen()`, that this tray should inherit parameters from. You can't create a tray without a screen.
 - `row`: Specify the values to assign to each row with either a single number (to assign to all rows), a list of two numbers (to evenly space among the rows) or a list of numbers explicitly specifying a value for each row. With 8 rows, you might say `rows=5`, `rows=[1,8]` or `rows=[1,2,3,4,6,8,10,12]`.
 - `col`: Specify values for columns, with the same format as for `row`.
##### `tt.well()`
`tt.well()` requires:
 - `tray`: The tray
 - `well`: The well; must be a string of format '[letter][number]', and must fall into the range specified by the screen's `maxwell`
 - `quality`: Any type, though I recommend a short categorical string like 'good', 'bad', 'needles', or 'multilattice'
 - `old_df`: Not strictly required, but to append previous results, pass previous returns from `tt.well()` to the next call as `old_df = `
  
### Optional arguments
All three of these methods (`tt.screen()`, `tt.tray()`, and `tt.well()`) will accept any additional named arguments, and include them as columns in the final data frame. As you would expect, arguments passed to `tt.screen()` will apply to all wells in all trays in the screen,  For example: *(to be continued)*
