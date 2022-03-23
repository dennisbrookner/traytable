#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
from varname import argname
from copy import deepcopy
import traytable as tt


def read_rockmaker(tray, filename=None, path=".", score_dict=None, old_df=None):

    if filename is None:
        temp = argname(tray)
        filename = f"Score Report - {temp}.csv"

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
    data["tray"] = argname(tray)
    data["date_logged"] = pd.to_datetime(
        data["date_logged"], infer_datetime_format=True
    )

    data["wellrow"] = data.well.str.get(0)
    data[tray["row"]] = data["wellrow"].map(tray)

    data["wellcol"] = data.well.str.get(1)
    data[tray["col"]] = data["wellcol"].map(tray)

    data.drop(["wellrow", "wellcol"], axis=1, inplace=True)

    statics = deepcopy(tray["statics"])

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
        if score_dict == "default":
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

    if old_df is not None:
        data = pd.concat([old_df, data], axis=0, ignore_index=True)

    return data


def main():

    FFscreen = tt.screen(
        row="protein",
        col="PEG",
        maxwell="H6",
        construct="wt DHFR",
        PEGtype=400,
        buffer="imidazole 20 mM",
        salt="MnCl2 125 mM",
    )

    DB191 = tt.tray(
        FFscreen,
        rows=(3, 17),
        cols=(18, 33),
        ss="1.8",
        pH=5.6,
        date="2022-03-18",
        ligand="10-methyl folate",
    )

    # filename = 'DB191.csv'
    path = "../../crystalrecords"

    data = read_rockmaker(DB191, path=path)

    print(data.quality)


if __name__ == "__main__":
    main()
