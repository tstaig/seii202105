from observing_mode import ObservingModeComponent

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