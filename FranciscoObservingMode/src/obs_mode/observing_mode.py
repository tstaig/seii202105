# # Client stubs and definitions, such as structs, enums, etc.
# import <Module>
# # Skeleton infrastructure for server implementation
import Observatory__POA
 
# # Base component implementation
from Acspy.Servants.ACSComponent import ACSComponent
# # Services provided by the container to the component
from Acspy.Servants.ContainerServices import ContainerServices
# # Basic component lifecycle (initialize, execute, cleanUp and aboutToAbort methods)
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
 
#Error definitions for catching exceptions
# import ServiceErr
# import <Interface>Err
 
# # Error definitions for creating and raising exceptions
import ServiceErrImpl
import ObservingModeErrImpl
import DatabaseErrImpl

# custom packages
import time
import random
from telescope_state import TelescopeState

# raising exceptions
# raise <Interface>ErrImpl.<ExceptionName>ExImpl()


class ObservingModeComponent(Observatory__POA.ObservingMode, ACSComponent, ContainerServices, ComponentLifecycle):
    """This component abstracts an observation."""

    def __init__(self):
        # initializes with state = STOP
        self.state = TelescopeState()

    def getState(self):
        """Returns the telescope's state object."""
        return self.state

    def startTelescope(self):
        """Turns the telescope on."""
        current_state = self.state.get()

        if current_state == 'READY':
            raise ObservingModeErrImpl.TelescopeAlreadyStartedExImpl()
        elif current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        else:
            self.state.set('READY')
            print('Telescope is now ready.')
        
    def stopTelescope(self):
        """Turns the telescope off."""
        current_state = self.state.get()

        if current_state == 'STOP':
            raise ObservingModeErrImpl.TelescopeAlreadyStoppedExImpl()
        elif current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        else:
            self.state.set('STOP')
            print('Telescope has stopped.')

    def observe(self, uid):
        """Issues an observation."""
        current_state = self.state.get()

        if current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        elif current_state == 'STOP':
            raise ObservingModeErrImpl.TelescopeIsStoppedExImpl()
        else:
            self.state.set('BUSY')
            print('Telescope is now busy.')
            print(f'Observing the night sky in awe for project {uid}...')
            time.sleep(random.choice([3, 7]))
            print('Observation finished.')
            self.state.set('READY')
