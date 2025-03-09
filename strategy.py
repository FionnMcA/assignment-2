import random

class Strategy():

    def __init__(self, name, first_move, responses, memory_size=1, hold_grudges= False, random_defection=0, random_strategy=False, fibonacci_defection=False, reverse_fibonacci=False):
        self.name = name
        self.first_move = first_move # First move is either (1 = C, 0 = D)
        self.responses = responses
        self.history = []
        self.memory_size = memory_size
        self.hold_grudges = hold_grudges
        self.remain_defecting = False
        self.random_defection = random_defection
        self.random_strategy = random_strategy
        self.fibonacci_defection = fibonacci_defection
        self.reverse_fibonacci = reverse_fibonacci
        self.fibonacci_numbers = self.gen_fibonacci_numbers()
        self.move_count = 0


    def gen_fibonacci_numbers(self):
        fib = {1, 2}
        a, b = 1, 2
        while b <= 100:
            a, b = b, a + b
            fib.add(b)
        return fib


    def player_move(self):
        self.move_count += 1

        if len(self.history) < self.memory_size:
            return self.first_move

        if self.fibonacci_defection and self.move_count in self.fibonacci_numbers:
            return 0

        if self.reverse_fibonacci and self.move_count in self.fibonacci_numbers:
            return 1

        if self.random_strategy:
            return random.choice([1, 0])

        if  self.responses is None:
            return random.choice([1, 0])

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