import os

from plone.browserlayer.utils import registered_layers
from plone.resource.directory import FilesystemResourceDirectory

from senaite.multiwellplate.interfaces import ISenaiteMultiWellPlateLayer


class WorksheetPrintResources(FilesystemResourceDirectory):
    """Expose multiwell print templates only on sites with the add-on."""

    def __init__(self):
        directory = os.path.join(os.path.dirname(__file__), "worksheets")
        super(WorksheetPrintResources, self).__init__(
            directory, "MWP print templates")

    def listDirectory(self):
        if ISenaiteMultiWellPlateLayer in registered_layers():
            return super(WorksheetPrintResources, self).listDirectory()
        return []
