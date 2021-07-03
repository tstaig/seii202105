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
 
# Error definitions for catching exceptions
import ServiceErr
import ObservingModeErr
import ObservingModeErrImpl
import DatabaseErr
 
# # Error definitions for creating and raising exceptions
import ServiceErrImpl
# import <Interface>ErrImpl

# custom packages
import time
import random
from interface import implements
# from observing_mode_interface import ObservingModeInterface
from telescope_state import TelescopeState


# implementation

# class <Name>(<Module>__POA.<InterfaceName>, ACSComponent, ContainerServices, ComponentLifecycle):
#     def __init__(self):
#         ACSComponent.__init__(self)
#         ContainerServices.__init__(self)
#         self._logger = self.getLogger()
#         ... #Custom implementation for the server constructor

# raising exceptions
# raise <Interface>ErrImpl.<ExceptionName>ExImpl().get<ExceptionName>Ex()


class ObservingModeComponent(Observatory__POA.ObservingMode, ACSComponent, ContainerServices, ComponentLifecycle):
# class ObservingModeComponent(implements(ObservingModeInterface)):
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
            raise ObservingModeErrImpl.TelescopeAlreadyStartedExImpl().getTelescopeAlreadyStartedEx()
        elif current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl().getTelescopeIsBusyEx()
        else:
            self.state.set('READY')
            print('Telescope is now ready.')
        
    def stopTelescope(self):
        """Turns the telescope off."""
        current_state = self.state.get()

        if current_state == 'STOP':
            raise ObservingModeErrImpl.TelescopeAlreadyStoppedExImpl().getTelescopeAlreadyStoppedEx()
        elif current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl().getTelescopeIsBusyEx()
        else:
            self.state.set('STOP')
            print('Telescope has stopped.')

    def observe(self, uid):
        """Issues an observation."""
        current_state = self.state.get()

        if current_state == 'BUSY':
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl().getTelescopeIsBusyEx()
        elif current_state == 'STOP':
            raise ObservingModeErrImpl.TelescopeIsStoppedExImpl().getTelescopeIsStoppedEx()
        else:
            self.state.set('BUSY')
            print('Telescope is now busy.')
            print(f'Observing the night sky in awe for project {uid}...')
            time.sleep(random.choice([3, 7]))
            print('Observation finished.')
            self.state.set('READY')



print('Testing happy path')
# initialize
obs = ObservingModeComponent()
# get state
state = obs.getState().get
print(f'Telescope is {state}')
# start
obs.startTelescope()
state = obs.getState().get
print(f'Telescope is {state}')
# observe
uid = 3
obs.observe(uid)
state = obs.getState().get
print(f'Telescope is {state}')
# stop
obs.stopTelescope()
state = obs.getState().get
print(f'Telescope is {state}')



print('Testing exceptions')
# initialize
obs = ObservingModeComponent()

# should raise TelescopeAlreadyStoppedEx
obs.stopTelescope()

# start
obs.startTelescope()
state = obs.getState().get
print(f'Telescope is {state}')

# should raise TelescopeAlreadyStartedEx
obs.startTelescope()

# get state
state = obs.getState().get
print(f'Telescope is {state}')
# start observation
obs.startTelescope()
state = obs.getState().get
print(f'Telescope is {state}')
# observe
uid = 3
obs.observe(uid)
state = obs.getState().get
print(f'Telescope is {state}')
# stop telescope
obs.stopTelescope()
state = obs.getState().get
print(f'Telescope is {state}')




uid = 3
obs.observe(uid)
state = ObservingModeComponent().observe(uid)