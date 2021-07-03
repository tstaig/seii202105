class TelescopeState():
    def __init__(self):
        self.STATES = ['STOP', 'READY', 'BUSY']
        self.state = 'STOP'
    
    def get(self):
        return self.state
    
    def set(self, state):
        if state in self.STATES:
            self.state = state
        else:
            print(f'{state} state is not valid. Must be: STOP, READY or BUSY.')

# ts = TelescopeState()
# print(ts.get())
# ts.set('READY')
# print(ts.get())

# # must fail
# ts.set('etc')