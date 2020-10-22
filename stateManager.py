class manager:
    def __init__(self, currentState):
        self.currentState = currentState

        self.FRACTIONCUTTING = 0
        self.VARCUTTING = 1
        self.CMCUTTING = 2
        self.SHADING = 3
        self.cuttingType = self.FRACTIONCUTTING

    def change_state(self, state):
        self.currentState = state
        print("State changed to: " + state)