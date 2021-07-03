# custom packages
from interface import Interface


class ObservingModeInterface(Interface):
    """Interface for ObservingModeComponent."""

    def getState(self):
        """Returns the telescope's state object."""
        pass

    def startTelescope(self):
        """Turns the telescope on."""
        pass

    def stopTelescope(self):
        """Turns the telescope off."""
        pass

    def observe(self, uid):
        """Issues an observation."""
        pass
