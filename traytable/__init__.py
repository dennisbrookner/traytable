def getVersionNumber():
    import pkg_resources

    version = pkg_resources.require("traytable")[0].version
    return version


__version__ = getVersionNumber()

from .screen import Screen, Tray
from .project import Project
