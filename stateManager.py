class manager:
    def __init__(self, currentState):
        self.currentState = currentState

        self.VARCUTTING = 0
        self.CMCUTTING = 1
        self.cuttingType = self.VARCUTTING

    def change_state(self, state):
        self.currentState = state
        print("State changed to: " + state)