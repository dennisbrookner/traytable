#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
import string
import datetime
from copy import deepcopy

from traytable import Screen, Tray


class Project:
    """
    One big object that can access all screens, trays, and hits
    """

    def __init__(self):

        self.screens = {}
        self.trays = {}

        self.hits = pd.DataFrame()

    def add_screen(self, screen_name, row, col, maxwell, **kwargs):

        self.screens[screen_name] = Screen(row, col, maxwell, **kwargs)

    def add_tray(self, screen_name, tray_name, rows, cols, **kwargs):
        """
        _summary_

        Parameters
        ----------
        name : _type_
            _description_
        rows : _type_
            _description_
        cols : _type_
            _description_
        """

        self.trays[tray_name] = Tray(
            screen_params=dict(self.screens[screen_name]),
            screen=screen_name,
            rows=rows,
            cols=cols,
            **kwargs,
        )

    def clone_tray(self, old, new, **kwargs):

        """
        Copy a tray, overriding parameters as desired

        Parameters
        ----------
        old : str
            Name of tray to be copied
        new : str
            Name of new tray to be created
        **kwargs : any type
            Accepts all arguments accepted by add_tray(), including rows and cols.
            Any parameters extant in old_name not specified here will be copied into new_name

        """

        self.trays[new] = deepcopy(self.trays[old])

        rows = kwargs.pop("rows", None)
        if rows is not None:
            self.trays[new].setrows(rows)

        cols = kwargs.pop("cols", None)
        if cols is not None:
            self.trays[new].setcols(cols)

        self.trays[new].params.update(**kwargs)

    def log(self, tray, well, quality, **kwargs):
        """
        Log one or more crystal hits

        Parameters
        ----------
        tray : str
            Name of tray
        well : str or list
            Well name or list of well names
        quality : any
            Quality of crystal being logged
        """

        fancy_dates = 0

        params = deepcopy(self.trays[tray].params)
        if "date" in params.keys():
            fancy_dates += 1
            params["date_set"] = params.pop("date")
            try:
                set_date = datetime.date.fromisoformat(params["date_set"])
            except ValueError:
                fancy_dates -= 1
                pass

        if "date" in kwargs.keys():
            fancy_dates += 1
            kwargs["date_logged"] = kwargs.pop("date")
            try:
                log_date = datetime.date.fromisoformat(kwargs["date_logged"])
            except ValueError:
                fancy_dates -= 1
                pass

        df = pd.DataFrame(
            columns=[self.trays[tray].row]
            + [self.trays[tray].col]
            + ["quality"]
            + list(params.keys())
            + ["tray"]
            + ["well"]
        )

        if type(well) == str:
            well = [well]

        if type(well) != list:
            raise TypeError("Improper type for well name")

        for w in well:

            if (
                w[0]
                not in string.ascii_uppercase[
                    : string.ascii_uppercase.find(self.trays[tray].maxwell[0]) + 1
                ]
            ):
                raise ValueError(
                    f"Improper column specification: column is {w[0]}, should be one of {string.ascii_uppercase[:string.ascii_uppercase.find(self.trays[tray].maxwell[0])+1]}"
                )

            if int(w[1]) not in range(1, int(self.trays[tray].maxwell[1]) + 1):
                raise ValueError(
                    f"Improper row specification: row is {w[1]}, should be one of {list(range(1,int(self.trays[tray].maxwell[1])+1))}"
                )

            df.loc[len(df.index)] = (
                [self.trays[tray][w[0]]]
                + [self.trays[tray][w[1]]]
                + [quality]
                + list(params.values())
                + [tray]
                + [w]
            )

        if kwargs is not None:

            for key, value in kwargs.items():
                df[key] = value

        if fancy_dates == 2:
            df["days_elapsed"] = (log_date - set_date).days

        self.hits = pd.concat([df, self.hits], axis=0, ignore_index=True)

    def hits_to_csv(self, filename):
        """
        This is silly because project.hits_to_csv() is exactly identical to project.hits.to_csv() lol
        """

        self.hits.to_csv(filename)

    def trays_to_df(self, filename=None):
        """
        Write out all trays in project to a csv file

        Parameters
        ----------
        filename : str
            If included, write csv to filename in addition to returning pandas DataFrame

        Returns
        -------
        df : pandas.DataFrame
            Dataframe of files
        """

        tray_df = pd.DataFrame()

        for name, tray in self.trays.items():

            df = pd.DataFrame(
                columns=["name"]
                # + ["row"]
                # + ["col"]
                + [f"min_{tray.row}"]
                + [f"max_{tray.row}"]
                + [f"min_{tray.col}"]
                + [f"max_{tray.col}"]
                + list(tray.params.keys())
            )

            df.loc[len(df.index)] = (
                [name]
                # + [tray.row]
                # + [tray.col]
                + [tray["A"]]
                + [tray[tray.maxwell[0]]]
                + [tray["1"]]
                + [tray[tray.maxwell[1]]]
                + list(tray.params.values())
            )

            tray_df = pd.concat([tray_df, df], axis=0)

        if filename is not None:
            tray_df.to_csv(filename)

        return tray_df.set_index("name")

    def read_rockmaker(self, tray, filename=None, path=".", score_dict=None):
        """
        Import crystal hits via a RockMaker-style csv file

        Parameters
        ----------
        tray : str
            Name of tray for which you are logging hits. Must be a valid key in project.trays
        filename : string, optional
            The name of the csv file. Defaults to "Score Report - {tray}.csv"
        path : string, optional
            Filepath to the csv file, if not in the current directory
        score_dict : dict, optional
            If None (default), scores are left as integers 1-9. If "rockmaker", integers are converted via the rockmaker naming convention.
            Any other dictionary can be passed and used to convert integer scores as desired.

        """
        if filename is None:
            filename = f"Score Report - {tray}.csv"

        data = pd.read_csv(f"{path}/{filename}")

        data.rename(
            columns={
                "Well": "well",
                "Inspection Date": "date_logged",
                "Score Hotkey": "quality",
            },
            inplace=True,
        )
        data.drop(
            ["Well Ingredients", "Drop #", "Plate ID", "Default"], axis=1, inplace=True
        )
        data["tray"] = tray
        data["date_logged"] = pd.to_datetime(
            data["date_logged"], infer_datetime_format=True
        )

        data["wellrow"] = data.well.str.get(0)
        data[self.trays[tray].row] = data["wellrow"].map(self.trays[tray])

        data["wellcol"] = data.well.str.get(1)
        data[self.trays[tray].col] = data["wellcol"].map(self.trays[tray])

        data.drop(["wellrow", "wellcol"], axis=1, inplace=True)

        statics = deepcopy(self.trays[tray].params)

        # special handling of dates
        if "date" in statics.keys():
            isodate = True
            statics["date_set"] = statics.pop("date")

            try:
                data["date_set"] = pd.Timestamp(statics.pop("date_set"))
            except ValueError:
                data["date_set"] = statics.pop("date_set")
                isodate = False
                pass

        if isodate:
            data["days_elapsed"] = (data["date_logged"] - data["date_set"]).dt.days

        for key, value in statics.items():
            data[key] = value

        if score_dict is not None:
            if score_dict == "rockmaker":
                score_dict = {
                    0: "Clear",
                    1: "Dust",
                    2: "Granular Precipitate",
                    3: "Full Precipitate",
                    4: "Good Precipitate",
                    5: "Phase Separation",
                    6: "Microcrystalline",
                    7: "Needles",
                    8: "Plates",
                    9: "Crystals",
                }
            data["quality"] = data["quality"].map(score_dict)

        self.hits = pd.concat([self.hits, data], axis=0, ignore_index=True)


def main():

    p = Project()

    p.add_screen("wt MC", row="protein", col="PEG", maxwell="H6")

    p.add_tray("wt MC", "DB1", rows=[8, 20], cols=[15, 20], date="2022-05-06")
    p.clone_tray("DB1", "DB2", rows=5, weather="sunny")

    p.log("DB1", "A2", "neat", date="2022-05-09")
    p.log("DB1", ["A3", "A4"], "meh")

    p.add_tray(
        "wt MC",
        "DB191",
        rows=(3, 17),
        cols=(18, 33),
        ss="1.8",
        pH=5.6,
        date="2022-03-18",
        ligand="10-methyl folate",
    )

    # filename = 'DB191.csv'
    path = "../../crystallization/crystalrecords/rockmaker/20220323"

    p.read_rockmaker("DB191", path=path)

    print(p.hits)


if __name__ == "__main__":
    main()
