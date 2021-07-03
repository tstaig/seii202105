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

import RecurrentJob
from datetime import timedelta

class SchedulingComponent(Observatory__POA.Scheduling, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()


        self.DB_INTERVAL_IN_SECONDS = 5
        self.SCHEDULING_INTERVAL_IN_SECONDS = 3

        '''
            Initialize an empty collection
            Initialize observing default mode 
            Initialize projects consumption from DB
            Initialize observing mode consumption
        '''
        self._projects_list = []
        self._state = Observatory.Service.OFFLINE
        self._db = None
        self._observing_mode = None
        self._db_job = None
        self._scheduling_job = None

    def execute(self):
        if self._state == Observatory.Service.OFFLINE:
            self._start_services()
            self._load_projects_job()
            self._make_it_happend_job()

    def cleanUp(self):
        if self._state == Observatory.Service.ONLINE or self._state == Observatory.Service.ERROR:
            self.stopService()

    def stopService(self):
        if self._state == Observatory.Service.OFFLINE:
            raise ServiceErr.ServiceAlreadyStoppedEx()

        try:
            if self._db:
                self._db.stopService()
                self.releaseComponent(self._db.name())
        except:
            self._logger("Scheduling: Problem releasing database component")

        try:
            if self._observing_mode:
                self._observing_mode.stopService()
                self.releaseComponent(self._observing_mode.name())
        except:
            self._logger("Scheduling: Problem releasing observing mode component")

        try:
            if self._db_job:
                self._db_job.stop()
        except:
            self._logger("Scheduling: Problem cancel db job")

        try:
            if self._scheduling_job:
                self._scheduling_job.stop()
        except:
            self._logger("Scheduling: Problem cancel scheduling job")

        self._db = None
        self._observing_mode = None
        self._db_job = None
        self._scheduling_job = None

    def getServiceState(self):
        return self._state

    def _start_services(self):
        self._set_state_or_die() 

        # load components
        try:
            self._db = self.getDefaultComponent("IDL:alma/Observatory/Database:1.0")
            if self._is_offline(self._db):
                self._db.startService()
            
            self._observing_mode = self.getDefaultComponent("IDL:alma/Observatory/ObservingMode:1.0")
            if self._is_offline(self._observing_mode):
                self._observing_mode.startService()

        except:
            self._logger.logWarning("Scheduling: Problem loading components")

        

    def _is_offline(self, service):
        return (service and service.getServiceState() == Observatory.Service.OFFLINE)

    def _set_state_or_die(self):
        if self._state == Observatory.Service.ONLINE:
            raise ServiceErr.ServiceAlreadyStartedEx()

        if self._state == Observatory.Service.ERROR:
            raise ServiceErr.ServiceInErrorStateEx()

        if self._state != Observatory.Service.OFFLINE:
            raise ServiceErr.ServiceIsTransitioningStatesEx()

        self._state = Observatory.Service.INITIALIZING 

    def _get_priorized_projects(self, projects):
        ''' 
            TODO some logic is needed?
        '''
        return projects

    def _load_projects_job(self):
        self._db_job = RecurrentJob(interval = timedelta(seconds=self.DB_INTERVAL_IN_SECONDS, execute=self._load_projects))
        self._db_job.start()

    def _load_projects(self):
        self._projects_list = self._db.getProjects()
    
    def _get_observing_mode(self):
        return self._observing_mode.getState()

    def _is_observe_available(self):
        return self._get_observing_mode == Observatory.Service.IDLE 
    
    def _make_it_happend_job(self):
        self._scheduling_job = RecurrentJob(interval = timedelta(seconds=self.SCHEDULING_INTERVAL_IN_SECONDS, execute=self._make_it_happend))
        self._scheduling_job.start()

    def _make_it_happend(self):
        projects = self._get_priorized_projects(self._project_list) 
        
        if self._is_observe_available() and projects:
            project = projects[0]
            self._observing_mode.observe(project)
            
