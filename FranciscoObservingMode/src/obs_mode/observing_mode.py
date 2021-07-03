# # Client stubs and definitions, such as structs, enums, etc.
# import <Module>
# # Skeleton infrastructure for server implementation
# import <Module>__POA
 
# # Base component implementation
# from Acspy.Servants.ACSComponent import ACSComponent
# # Services provided by the container to the component
# from Acspy.Servants.ContainerServices import ContainerServices
# # Basic component lifecycle (initialize, execute, cleanUp and aboutToAbort methods)
# from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
 
# # Error definitions for catching exceptions
# import ServiceErr
# import <Interface>Err
 
# # Error definitions for creating and raising exceptions
# import ServiceErrImpl
# import <Interface>ErrImpl

# custom packages
import time
import random
from interface import implements
from observing_mode_interface import ObservingModeInterface
from telescope_state import TelescopeState
from exceptions import *


# implementation

# class <Name>(<Module>__POA.<InterfaceName>, ACSComponent, ContainerServices, ComponentLifecycle):
#     def __init__(self):
#         ACSComponent.__init__(self)
#         ContainerServices.__init__(self)
#         self._logger = self.getLogger()
#         ... #Custom implementation for the server constructor


class ObservingModeComponent(implements(ObservingModeInterface)):
    """This component abstracts an observation."""

    def __init__(self):
        # initializes with state = STOP
        self.state = TelescopeState()

    def getState(self):
        """Returns the telescope's state object."""
        return self.state

    def startTelescope(self):
        """Turns the telescope on."""
        pass

    def stopTelescope(self):
        """Turns the telescope off."""
        pass

    def observe(self, uid):
        """Issues an observation."""

        print('Observing the night sky in awe...')
        time.sleep(random.choice([3, 7]))


uid = 3
ObservingModeComponent().observe(uid)