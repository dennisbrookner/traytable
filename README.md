# crystalscreening
### A simple python package for organizing crystallization screening results.
Logging and optimizing crystal hits can involve either a lot of redundant notetaking, or frequent look-ups of varying conditions across numerous trays. With this package, you input all information about your crystal conditions just once, and that information is automatically included when you log a 'hit'.  

You can find a working example in [sample.ipynb](https://github.com/dennisbrookner/crystalscreening/blob/main/sample.ipynb), with the slight caveat that the package isn't pip-installable yet, so to run the code yourself you'd need to download this repo and add it to your `PYTHONPATH` via something like 

```bash
export PYTHONPATH="${PYTHONPATH}:/Path/to/local/copy/of/crystalscreening"
```
in your `.bashrc`
