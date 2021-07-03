#Base component implementation
from Acspy.Servants.ACSComponent import ACSComponent

#Client stubs and definitions, such as structs, enums, etc.
import Observatory
import Observatory__POA


#Base component implementation
from Acspy.Servants.ACSComponent import ACSComponent
#Services provided by the container to the component
from Acspy.Servants.ContainerServices import ContainerServices
#Basic component lifecycle (initialize, execute, cleanUp and aboutToAbort methods)
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
 
#Error definitions for catching exceptions
import ServiceErr


class SchedulingComponent(Observatory__POA.Scheduling, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._start()

    def _start(self):
        '''
            Initialize an empty collection
            Initialize observing default mode 
            Initialize projects consumption from DB
            Initialize observing mode consumption
        '''
        self._projects_list = []
        self._state = Observatory.Service.OFFLINE
        self._db = None
        pass

    def _priorize_projects(projects):
        pass

    def _get_projects(self):
        pass
    
    def _get_observing_mode(self):
        pass
