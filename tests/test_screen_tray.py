import traytable as tt
import pytest


def test_screen_well():
    screen = tt.screen(row="PEG", col="protein", maxwell="H6")
    assert len(screen) == 4

    tray = tt.tray(screen, rows=5, cols=6)

    assert tray["C"] == 5
    assert tray["3"] == 6
    assert len(tray) == 18


def test_bad_maxwell():
    with pytest.raises(ValueError):
        tt.screen(row="PEG", col="protein", maxwell="H3H")


def test_gradients():
    screen = tt.screen(row="PEG", col="protein", maxwell="H6")
    tray = tt.tray(screen, rows=[1, 8], cols=[10, 15])

    assert tray["C"] == 3

    assert tray["3"] == 12


def test_assigned():
    screen = tt.screen(row="PEG", col="protein", maxwell="H6")
    tray = tt.tray(screen, rows=[1, 2, 3, 4, 5, 7, 7, 8], cols=[10, 11, 12, 14, 14, 15])

    assert tray["F"] == 7

    assert tray["4"] == 14


def test_bad_assigned():
    screen = tt.screen(row="PEG", col="protein", maxwell="H6")
    with pytest.raises(ValueError):
        tt.tray(screen, rows=[1, 2, 3, 4, 5, 7, 7], cols=[10, 11, 12, 14, 14, 15])
