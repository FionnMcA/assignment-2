import random

class Strategy():

    def __init__(self, name, first_move, responses, memory_size=1, hold_grudges= False, random_defection=0):
        self.name = name
        self.first_move = first_move # First move is either (1 = C, 0 = D)
        self.responses = responses
        self.history = []
        self.memory_size = memory_size
        self.hold_grudges = hold_grudges
        self.remain_defecting = False
        self.random_defection = random_defection


    def player_move(self):
        if len(self.history) < self.memory_size:
            return self.first_move


        if random.random() < self.random_defection: #If its a strategy that contains random defection
            return 0

        if self.remain_defecting: # If it holds grudges it will continue to only defect once it has been defected
            return 0

        last_move = tuple(self.history[-self.memory_size:])
        return self.responses[last_move]

    def update_history(self, opp_move):
        self.history.append(opp_move)
        if self.hold_grudges and opp_move == 0:
            self.remain_defecting = True


    def get_name(self):
        pass