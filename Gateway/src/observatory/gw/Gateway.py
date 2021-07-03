import traceback
import Observatory
import Observatory__POA

from jsonrpcserver import methods
from observatory.gw.KThread import KThread
from Acspy.Servants.ACSComponent import ACSComponent
from jsonrpcserver.exceptions import JsonRpcServerError
from Acspy.Servants.ContainerServices import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle

import ServiceErr

#------------------------------------------------------------------------------
class Gateway(Observatory__POA.Gateway, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._state = Observatory.Service.OFFLINE
        self._rpc = None
        self._dbase = None
        self._omode = None
        self._sched = None
        methods.add(self._addProject, name="addProject")
        methods.add(self._getProject, name="getProject")
        methods.add(self._getProjects, name="getProjects")
        methods.add(self._updateProject, name="updateProject")
        methods.add(self._removeProject, name="removeProject")
        methods.add(self._getTelescopeState, name="getTelescopeState")
        methods.add(self._getNextProjects, name="getNextProjects")

    #Component LifeCycle
    def execute(self):
        if self._state == Observatory.Service.OFFLINE:
            self.startService()

    def cleanUp(self):
        if self._state == Observatory.Service.ONLINE or self._state == Observatory.Service.ERROR:
            self.stopService()
    #End Component LifeCycle

    #Service Interface
    def startService(self):
        if self._state == Observatory.Service.ONLINE:
            raise ServiceErr.ServiceAlreadyStartedEx()
        if self._state == Observatory.Service.ERROR:
            raise ServiceErr.ServiceInErrorStateEx()
        if self._state != Observatory.Service.OFFLINE:
            raise ServiceErr.ServiceIsTransitioningStatesEx()
        self._state = Observatory.Service.INITIALIZING
        try:
            self._dbase = self.getDefaultComponent("IDL:alma/Observatory/Database:1.0")
            self._omode = self.getDefaultComponent("IDL:alma/Observatory/ObservingMode:1.0")
            self._sched = self.getDefaultComponent("IDL:alma/Observatory/Scheduling:1.0")
            if self._dbase:
                if self._dbase.getServiceState() == Observatory.Service.OFFLINE: self._dbase.startService()
            if self._omode:
                if self._omode.getServiceState() == Observatory.Service.OFFLINE: self._omode.startService()
            if self._sched:
                if self._sched.getServiceState() == Observatory.Service.OFFLINE: self._sched.startService()
            self._rpc = KThread(target=self._startJsonRpcService)
            self._rpc.start()
        except:
            traceback.print_exc()
            self._logger.logWarning("Gateway: Problem retrieving components")
            self._state = Observatory.Service.ERROR
            return
        self._state = Observatory.Service.ONLINE

    def stopService(self):
        if self._state == Observatory.Service.OFFLINE:
            raise ServiceErr.ServiceAlreadyStoppedEx()
        if self._state != Observatory.Service.ONLINE and self._state != Observatory.Service.ERROR:
            raise ServiceErr.ServiceIsTransitioningStatesEx()
        self._state = Observatory.Service.STOPPING
        try:
            if self._rpc:
                self._rpc.kill()
                self._rpc.join()
            if self._sched:
                if self._sched.getServiceState() == Observatory.Service.ONLINE or self._sched.getServiceState() == Observatory.Service.ERROR: self._sched.stopService()
                self.releaseComponent(self._sched.name())
            if self._omode:
                if self._omode.getServiceState() == Observatory.Service.ONLINE or self._omode.getServiceState() == Observatory.Service.ERROR: self._omode.stopService()
                self.releaseComponent(self._omode.name())
            if self._dbase:
                if self._dbase.getServiceState() == Observatory.Service.ONLINE or self._dbase.getServiceState() == Observatory.Service.ERROR: self._dbase.stopService()
                self.releaseComponent(self._dbase.name())
        except:
            self._logger.logWarning("Gateway: Problem releasing components")
        self._rpc = None
        self._dbase = None
        self._omode = None
        self._sched = None
        self._state = Observatory.Service.OFFLINE

    def getServiceState(self):
        return self._state
    #End Service Interface

    #Gateway Interface
    #End Gateway Interface

    #JSON RPC Interface
    def _startJsonRpcService(self):
        methods.serve_forever()
    def _addProject(self, project):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        prj = self._fromJsonProject(project)
        prj.state = Observatory.READY
        self._dbase.addProject(prj)
        print("Project (" + str(project["uid"]) + ") was added")
    def _getProject(self, uid):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        return self._toJsonProject(self._dbase.getProject(uid))
    def _getProjects(self):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        return [self._toJsonProject(p) for p in self._dbase.getProjects()]
    def _updateProject(self, project):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        self._dbase.updateProject(self._fromJsonProject(project))
        print("Project (" + str(project["uid"]) + ") was updated")
    def _removeProject(self, uid):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        self._dbase.removeProject(uid)
        print("Project (" + str(uid) + ") was removed")
    def _getTelescopeState(self):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        return str(self._omode.getState())
    def _getNextProjects(self, num):
        if self._state != Observatory.Service.ONLINE:
            raise JsonRpcServerError(data="The Gateway service is in " + str (self._state) + " state.")
        return [self._toJsonProject(p) for p in self._sched.getNextProjects(num)]
    #End JSON RPC Interface

    def _toJsonProject(self, prj):
        return {"uid":prj.uid, "name":prj.name, "duration":prj.duration, "state":str(prj.state), "rank":prj.rank}
    def _fromJsonProject(self, prj):
        state = None
        for i in range (0, len(Observatory.ProjectState._items)): 
            print(str(prj["state"]), str(Observatory.ProjectState._item(i)))
            if str(Observatory.ProjectState._item(i)) == prj["state"]:
                state = Observatory.ProjectState._item(i)
        return Observatory.Project(prj["uid"], str(prj["name"]), prj["duration"], state, prj["rank"])
