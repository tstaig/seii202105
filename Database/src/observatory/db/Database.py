import traceback
import Observatory
import Observatory__POA

from operator import attrgetter

from Acspy.Servants.ACSComponent import ACSComponent
from Acspy.Servants.ContainerServices import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle

import ServiceErrImpl
import DatabaseErrImpl

#------------------------------------------------------------------------------
class Database(Observatory__POA.Database, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._state = Observatory.Service.OFFLINE
        self._prjs = []
        prj1 = Observatory.Project(11, "Test", 10, Observatory.READY, 1)
        prj2 = Observatory.Project(12, "Test", 10, Observatory.READY, 1)
        self._prjs.append(prj1)
        self._prjs.append(prj2)

    #Component LifeCycle
    def execute(self):
        pass

    def cleanUp(self):
        if self._state == Observatory.Service.ONLINE or self._state == Observatory.Service.ERROR:
            self.stopService()
    #End Component LifeCycle

    #Service Interface
    def startService(self):
        if self._state == Observatory.Service.ONLINE:
            raise ServiceErrImpl.ServiceAlreadyStartedExImpl().getServiceAlreadyStartedEx()
        if self._state == Observatory.Service.ERROR:
            raise ServiceErrImpl.ServiceInErrorStateExImpl().getServiceInErrorStateEx()
        if self._state != Observatory.Service.OFFLINE:
            raise ServiceErrImpl.ServiceIsTransitioningStatesExImpl().getServiceIsTransitioningStatesEx()
        self._state = Observatory.Service.INITIALIZING
        self._state = Observatory.Service.ONLINE

    def stopService(self):
        if self._state == Observatory.Service.OFFLINE:
            raise ServiceErrImpl.ServiceAlreadyStoppedExImpl().getServiceAlreadyStoppedEx()
        if self._state != Observatory.Service.ONLINE and self._state != Observatory.Service.ERROR:
            raise ServiceErrImpl.ServiceIsTransitioningStatesExImpl().getServiceIsTransitioningStatesEx()
        self._state = Observatory.Service.STOPPING
        self._state = Observatory.Service.OFFLINE

    def getServiceState(self):
        return self._state
    #End Service Interface

    #Database Interface
    def addProject(self, project):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        prj = Observatory.Project(self._getUniqueID(), project.name, project.duration, Observatory.READY, project.rank)
        self._prjs.append(prj)
        print("Project (" + str(prj.uid) + ") was added")
    def getProject(self, uid):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        prj = [p for p in self._prjs if p.uid == uid]
        if len(prj) == 0:
            raise DatabaseErrImpl.ProjectDoesNotExistExImpl().getProjectDoesNotExistEx()
        return prj[0]
    def getProjects(self):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        return self._prjs
    def updateProject(self, project):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        prj = [p for p in self._prjs if p.uid == project.uid]
        if len(prj) == 0:
            raise DatabaseErrImpl.ProjectDoesNotExistExImpl().getProjectDoesNotExistEx()
        self._prjs = [project if p.uid == project.uid else p for p in self._prjs]
        print("Project (" + str(project.uid) + ") was updated")
    def removeProject(self, uid):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        prj = [p for p in self._prjs if p.uid == uid]
        if len(prj) == 0:
            raise DatabaseErrImpl.ProjectDoesNotExistExImpl().getProjectDoesNotExistEx()
        self._prjs = [p for p in self._prjs if p.uid != uid]
        print("Project (" + str(uid) + ") was removed")
    def clearAllProjects():
        self.prjs = []
    def forceChangeState(uid, state):
        if self._state != Observatory.Service.ONLINE:
            raise self._getServiceIsNotOnlineEx()
        prj = [p for p in self._prjs if p.uid == uid]
        if len(prj) == 0:
            raise DatabaseErrImpl.ProjectDoesNotExistExImpl().getProjectDoesNotExistEx()
        for p in self._prjs:
            if p.uid == uid:
                p.state = state
        print("Project (" + str(project.uid) + ") was updated")
    #End Database Interface

    #Misc Helper Methods
    def _getServiceIsNotOnlineEx(self):
        err = ServiceErrImpl.ServiceIsNotOnlineExImpl()
        err.setState(self._state)
        return err.getServiceIsNotOnlineEx()
    def _getUniqueID(self):
        if len(self._prjs) == 0:
            return 1
        return max(self._prjs, key=attrgetter('uid')).uid + 1

    #End Misc Helper Methods
