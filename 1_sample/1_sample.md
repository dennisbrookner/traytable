```python
import traytable as tt
import matplotlib.pyplot as plt
```

## Making a screen
First, initialize the screen with `screen()`. This function requires that you specify
 - the parameter that varies by row 
 - the parameter that varies by column
 - the plate shape, in the form of a "max well", e.g. the well in the bottom right corner of the plate.
 
Note that `row` refers to the parameter encoded by the row name; this is the parameter that is the same within a row, rather than the parameter that varies across the row. Likewise for columns.

Finally, whatever additional named arguments you pass to `screen()` become "screen static" global parameters that apply to all wells in all trays in the screen. Perhaps you include the protein construct, a nickname for the screen, or the type of plate you're using.


```python
myscreen = tt.screen(row = 'protein', col = 'PEG', maxwell = 'H6', 
                     construct = 'HEWL', buffer = 'imidazole 20mM')
```

Now let's make a tray. Like with `screen()`, `tray()` will parse any additional named arguments as "tray static" parameters that apply to all wells in the tray. A common example might be the date the tray was set, or a buffer or additive that is the same across the plate.

Most importantly, `tray()` accepts arguments `rows` and `cols` to specify the values of the parameters varying across the plate. These can be set in three ways:
 - with a list of two numbers, e.g. `row = [4, 18]` which would evenly space values across the rows (with number of rows determined via the `maxwell` parameter for the screen
 - with a list of numbers equal in length to the number of rows/columns, which get mapped to rows/columns explicitly
 - with a single number, which will be used for all rows/columns


```python
tray1 = tt.tray(myscreen, date = '2021-01-01', pH = 5.8,
                rows = [4,18],
                cols = [20,25])
```

The `clonetray()` method clones a tray with useage `newtray = clonetray(screen, oldtray, **kwargs)` where you can override specific parameters of the tray being cloned. When trays are similar (or identical) this saves some typing.


```python
tray2 = tt.clonetray(tray1, date = '2021-01-03',
                     rows = [4, 5, 6, 7, 8, 10, 12, 14])
```

In this case, using `clonetray()` instead of `tray()` saves you from having to re-specify the pH and the column values, which haven't changed from the previous tray.

## Logging hits!
Our two trays have some crystals! We can log wells with good (or bad!) crystals via the `well()` function. `well()` requires the tray, well, and a short string to describe crystal quality; any other named parameters (perhaps a more verbose description, or a number of crystals) are accepted and get their own column in the resulting dataframe. 

For all but the first call to `well()`, don't forget `old_df=df` to concatenate the new results with the old results.


```python
df = tt.well(tray1, 'A6', 'good', quantity = 3)
df = tt.well(tray1, 'B6', 'good', quantity = 2, note = "chunkier than usual", old_df=df)
df = tt.well(tray1, 'C6', 'needles', old_df=df)
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>protein</th>
      <th>PEG</th>
      <th>quality</th>
      <th>construct</th>
      <th>buffer</th>
      <th>date</th>
      <th>pH</th>
      <th>tray</th>
      <th>well</th>
      <th>quantity</th>
      <th>note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4.0</td>
      <td>25.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>A6</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6.0</td>
      <td>25.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>B6</td>
      <td>2.0</td>
      <td>chunkier than usual</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8.0</td>
      <td>25.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>C6</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



The `well()` function uses the tray and well to look up all the data you've logged in your screens.

If you have many wells, all of the same quality, you can log them all at once:


```python
df = tt.well(tray2, ['B3', 'C3', 'D3', 'E3'], 'needles', old_df=df)
df = tt.well(tray2, ['A5', 'A6', 'B5'], 'good', old_df=df, note='borderline')
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>protein</th>
      <th>PEG</th>
      <th>quality</th>
      <th>construct</th>
      <th>buffer</th>
      <th>date</th>
      <th>pH</th>
      <th>tray</th>
      <th>well</th>
      <th>quantity</th>
      <th>note</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4.0</td>
      <td>25.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>A6</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6.0</td>
      <td>25.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>B6</td>
      <td>2.0</td>
      <td>chunkier than usual</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8.0</td>
      <td>25.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-01</td>
      <td>5.8</td>
      <td>tray1</td>
      <td>C6</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>22.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>B3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>22.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>C3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7</td>
      <td>22.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>D3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>8</td>
      <td>22.0</td>
      <td>needles</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>E3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>4</td>
      <td>24.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>A5</td>
      <td>NaN</td>
      <td>borderline</td>
    </tr>
    <tr>
      <th>8</th>
      <td>4</td>
      <td>25.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>A6</td>
      <td>NaN</td>
      <td>borderline</td>
    </tr>
    <tr>
      <th>9</th>
      <td>5</td>
      <td>24.0</td>
      <td>good</td>
      <td>HEWL</td>
      <td>imidazole 20mM</td>
      <td>2021-01-03</td>
      <td>5.8</td>
      <td>tray2</td>
      <td>B5</td>
      <td>NaN</td>
      <td>borderline</td>
    </tr>
  </tbody>
</table>
</div>



Finally, let's visualize which conditions are giving good crystals vs. needles.


```python
colordict= {'good':'green',
            'needles':'gray'}
df.plot.scatter('protein', 'PEG', alpha=0.6, c=df.quality.map(colordict))
plt.title('What [protein] vs. %PEG gives the best crystals?')
plt.show()
```


    
![png](output_14_0.png)
    


Looks like we should optimize with high PEG, low protein conditions. With `traytable`, no matter how many trays you've set with slightly varied screens, you can always consolidate your results in a single table or plot.

### Other things of note
- You may have noticed that optional parameters present in some calls to `well()`, but not others, are harmlessly treated as `NaN` where missing.
- The `setrows()` and `setcols()` methods are called behind the scenes by `tray()` and `clonetray()` via the `rows` and `cols` keyword arguments, respectively, but are also available as stand-alone functions with usage `tray = setrows(tray, rows)` and likewise for columns.

## Just a code chunk


```python
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
plt.title('What [protein] vs. %PEG gives the best crystals?')
plt.show()
```


    
![png](output_18_0.png)
    

