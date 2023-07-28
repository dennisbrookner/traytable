import traytable as tt
import pytest


@pytest.fixture
def project():
    """
    Example project to use in test functions
    """

    p = tt.Project()
    p.add_screen("example screen", row="PEG", col="protein", maxwell="H6")
    p.add_tray("example screen", "example tray", rows=5, cols=6)

    return p


def test_screens_and_trays(project):

    assert project.trays["example tray"]["C"] == 5
    assert project.trays["example tray"]["3"] == 6
    assert "example screen" in project.screens.keys()
    assert "example tray" in project.trays.keys()


def test_bad_maxwell(project):
    with pytest.raises(ValueError):
        project.add_screen("bad screen", row="PEG", col="protein", maxwell="H3H")

    with pytest.raises(ValueError):
        project.add_screen("bad screen", row="PEG", col="protein", maxwell="3H")


def test_gradients(project):

    project.add_tray("example screen", "gradient tray", rows=[1, 8], cols=[10, 15])

    assert project.trays["gradient tray"]["C"] == 3

    assert project.trays["gradient tray"]["3"] == 12


def test_assigned(project):

    project.add_tray(
        "example screen",
        "explicit tray",
        rows=[1, 2, 3, 4, 5, 7, 7, 8],
        cols=[10, 11, 12, 14, 14, 15],
    )

    assert project.trays["explicit tray"]["F"] == 7

    assert project.trays["explicit tray"]["4"] == 14


def test_bad_assigned(project):

    with pytest.raises(ValueError):
        project.add_tray(
            "example screen",
            "bad tray",
            rows=[1, 2, 3, 4, 5, 7, 7],
            cols=[10, 11, 12, 14, 14, 15],
        )
