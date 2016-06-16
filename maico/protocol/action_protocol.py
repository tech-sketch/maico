class ActionProtocol():

    def __init__(self, 
                 shop_id="",
                 target_id="",
                 state="",
                 action="",
                 reward=-1):
        
        self.shop_id = shop_id
        self.target_id = target_id
        self.state = state
        self.action = action
        self.reward = reward
