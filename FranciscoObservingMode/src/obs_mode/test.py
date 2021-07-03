from observing_mode import ObservingModeComponent

print('Testing happy path')
# initialize
obs = ObservingModeComponent()
# start
obs.startTelescope()
# observe
uid = 3
obs.observe(uid)
# stop
obs.stopTelescope()


print('Testing exceptions')
# initialize
obs = ObservingModeComponent()

print('should raise TelescopeAlreadyStoppedEx')
obs.stopTelescope()

# obs.startTelescope()
# print('should raise TelescopeAlreadyStartedEx')
# obs.startTelescope()
