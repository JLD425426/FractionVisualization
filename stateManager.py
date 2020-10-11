class manager:
    def __init__(self, currentState):
        self.currentState = currentState

    def change_state(self, state):
        self.currentState = state
        print("State changed to: " + state)