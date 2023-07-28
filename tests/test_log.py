import traytable as tt
import pytest

from test_project import project


def test_minimal(project):

    project.log("example tray", "A3", "good")

    assert len(project.hits) == 1


def test_log_multiple(project):
    project.log("example tray", ["A3", "A4"], "good")

    assert len(project.hits) == 2


def test_append(project):
    project.log("example tray", "A3", "good")
    project.log("example tray", "A4", "bad")

    assert len(project.hits) == 2


def test_maxwell_violation(project):
    with pytest.raises(ValueError):
        project.log("example tray", "A7", "good")


def test_missing_argument(project):
    with pytest.raises(TypeError):
        project.log("example tray", "good")
