class ActionProtocol():

    def __init__(self, 
                 target_id="",
                 state="",
                 action="",
                 reward=-1):
        
        self.target_id = target_id
        self.state = state
        self.action = action
        self.reward = reward
