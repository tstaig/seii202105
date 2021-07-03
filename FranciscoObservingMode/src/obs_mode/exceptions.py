# service exceptions
class ServiceErr(Exception):
    """Base class for ACS service exceptions."""
    pass


class ServiceIsNotOnlineEx(ServiceErr):
    """Raised when service is not online."""
    pass


# observing mode exceptions
class ObservingModeErr(Exception):
    """Base class for observing mode exceptions."""
    pass


class TelescopeAlreadyStartedEx(ObservingModeErr):
    """Raised when the telescope is already started."""
    pass


class TelescopeIsBusyEx(ObservingModeErr):
    """Raised when the telescope is busy."""
    pass


class TelescopeAlreadyStoppedEx(ObservingModeErr):
    """Raised when the telescope is already stopped."""
    pass


class ProjectInUnexpectedStateEx(ObservingModeErr):
    """Raised when the project is in an unexpected state."""
    pass


# db exceptions
class DatabaseErr(Exception):
    """Base class for databse exceptions."""
    pass


class ProjectDoesNotExistEx(DatabaseErr):
    """Raised when the project does not exist."""
    pass