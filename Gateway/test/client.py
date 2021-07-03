import jsonrpcclient

prj = {"uid":1, "name":"Test", "duration": 10, "state":"READY", "rank":1}

#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'addProject', [prj]))
print(jsonrpcclient.request('http://localhost:5000/', 'getProject', [13]))
print(jsonrpcclient.request('http://localhost:5000/', 'getProjects'))
#prj["uid"] = 13
#prj["name"]="Test2"
#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'updateProject', [prj]))
#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'getProject', [13]))
#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'removeProject', [13]))
#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'getProjects'))
#print(jsonrpcclient.request('http://172.20.0.2:5000/', 'getTelescopeState'))
print(jsonrpcclient.request('http://localhost:5000/', 'getNextProjects', [5]))
