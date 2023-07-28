#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """
# import pandas as pd
import string
import numpy as np
from copy import deepcopy


class Screen(dict):
    """
    Screen object

    This object inherits from the built-in class `dict`, meaning it still has key/value pairs and such.
    I think this is good because it makes parameter names available as strings throughout
    """

    def __init__(self, row, col, maxwell, **kwargs):
        """
        _summary_

        Parameters
        ----------
        row : _type_
            _description_
        col : _type_
            _description_
        maxwell : _type_
            _description_

        """

        # Make sure maxwell is formatted properly
        if len(maxwell) != 2:
            raise ValueError(
                f"maxwell must have length 2, supplied {maxwell} has length {len(maxwell)}"
            )
        elif not maxwell[0].isalpha():
            raise ValueError(
                f"first character of maxwell must be a letter, supplied {maxwell} has first character {maxwell[0]}"
            )
        elif not maxwell[1].isdigit():
            raise ValueError(
                f"second character of maxwell must be a number, supplied {maxwell} has second character {maxwell[1]}"
            )

        self["row"] = row
        self["col"] = col
        self["maxwell"] = maxwell

        for key, value in kwargs.items():
            self[key] = value


class Tray(dict):
    """
    Tray object
    """

    def __init__(self, screen_params, screen, rows, cols, **kwargs):
        """
        Construct a tray

        Parameters
        ----------
        screen_params : dict
            _description_
        rows : _type_
            _description_
        cols : _type_
            _description_
        """
        params = deepcopy(screen_params)

        self.row = params.pop("row")
        self.col = params.pop("col")
        self.maxwell = params.pop("maxwell")
        self.screen = screen

        self.params = params

        self.setrows(rows)
        self.setcols(cols)

        self.params.update(**kwargs)

    # def __repr__(self):
    #     return f"tt.Tray of {self['row']} vs {self['col']}"

    def setrows(self, *args):
        """
        Set values encoded by row names, e.g. the values static across each row

        Parameters
        ----------
        tray : dict
            Tray to which rows will be added.
        *args : list or float
            Row values can be passed as one number to apply to all rows,
            numrows numbers to map directly to rows, or
            two numbers to create an evenly spaced gradient across the rows

        Returns
        -------
        screen : dict
            Screen containing the tray to which rows have been added

        """

        numrows = string.ascii_uppercase.find(self.maxwell[0]) + 1

        rownames = [i for i in string.ascii_uppercase[:numrows]]

        rowdata = rowcolparser(numrows, "rows", args)

        for name, data in zip(rownames, rowdata):
            self[name] = data

    def setcols(self, *args):
        """
        Set values encoded by column names, e.g. the values static down each column

        Parameters
        ----------
        tray : dict
            Tray to which columns will be added.
        *args : list or float
            Column values can be passed as one number to apply to all columns,
            numcols numbers to map directly to columns, or
            two numbers to create an evenly spaced gradient across the columns

        Returns
        -------
        screen : dict
            Screen containing the tray to which columns have been added

        """

        numcols = int(self.maxwell[1])

        colnames = [str(i) for i in range(1, numcols + 1)]

        coldata = rowcolparser(numcols, "column", args)

        for name, data in zip(colnames, coldata):
            self[name] = data


def rowcolparser(n, which, *args):
    """
    Helper function not exported

    Handles passing of a single value, pair of values, or list of values to setrows or setcols
    """

    if len(args) == n:
        data = args
    elif len(args) == 2:
        data = np.linspace(args[0], args[1], n)
    elif len(args) == 1:
        if type(args[0]) is int or type(args[0]) is float:
            data = [args[0]] * n
        elif len(args[0]) == n:
            data = args[0]
        elif len(args[0]) == 2:
            data = np.linspace(args[0][0], args[0][1], n)
        elif len(args[0]) == 1:
            if type(args[0][0]) is int or type(args[0][0]) is float:
                data = [args[0][0]] * n
            elif len(args[0][0]) == n:
                data = args[0][0]
            elif len(args[0][0]) == 2:
                data = np.linspace(args[0][0][0], args[0][0][1], n)
            elif len(args[0][0]) == 1:
                data = args[0][0] * n
            else:
                raise ValueError(f"Unexpected {which} specification")

    return data


def main():

    screen = Screen("PEG", "protein", "H6", foo="bar")
    print(screen)
    print(screen.trays)

    screen.add_tray("DBtest", [1, 7], [2, 3])
    screen.add_tray("another one", 6, 9, foo2="bar2")
    screen.clone_tray("DBtest", "DBclone", cols=5)
    print(screen.trays)

    return


if __name__ == "__main__":
    main()
