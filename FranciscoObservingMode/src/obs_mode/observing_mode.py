import Observatory
import Observatory__POA
from Acspy.Servants.ACSComponent import ACSComponent
from Acspy.Servants.ContainerServices import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
 
# Error definitions for creating and raising exceptions
import ServiceErrImpl
import ObservingModeErrImpl
import DatabaseErrImpl

# custom packages
import time
import random


class ObservingModeComponent(Observatory__POA.ObservingMode, ACSComponent, ContainerServices, ComponentLifecycle):
    """This component abstracts an observation."""

    def __init__(self):
        # initializes with state = STOP
        self.state = Observatory.ObservingMode.STOP

    def getState(self):
        """Returns the telescope's state object."""
        return self.state

    def startTelescope(self):
        """Turns the telescope on."""
        if self.state == Observatory.ObservingMode.READY:
            raise ObservingModeErrImpl.TelescopeAlreadyStartedExImpl()
        elif self.state == Observatory.ObservingMode.BUSY:
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        else:
            self.state = Observatory.ObservingMode.READY
            print('Telescope is now ready.')
        
    def stopTelescope(self):
        """Turns the telescope off."""
        if self.state == Observatory.ObservingMode.STOP:
            raise ObservingModeErrImpl.TelescopeAlreadyStoppedExImpl()
        elif self.state == Observatory.ObservingMode.BUSY:
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        else:
            self.state = Observatory.ObservingMode.STOP
            print('Telescope has stopped.')

    def observe(self, uid):
        """Issues an observation."""
        if self.state == Observatory.ObservingMode.BUSY:
            raise ObservingModeErrImpl.TelescopeIsBusyExImpl()
        elif self.state == Observatory.ObservingMode.STOP:
            raise ObservingModeErrImpl.TelescopeIsStoppedExImpl()
        else:
            self.state = Observatory.ObservingMode.BUSY
            print('Telescope is now busy.')
            print(f'Observing the night sky in awe for project {uid}...')
            time.sleep(random.choice([3, 7]))
            print('Observation finished.')
            self.state = Observatory.ObservingMode.READY
