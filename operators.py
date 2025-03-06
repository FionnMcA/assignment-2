import random
from strategy import Strategy

def mutation(strategy, mutation_rate=0.5):
    first_move = strategy.first_move if random.random() > mutation_rate else random.choice([0, 1])

    response_map = {
        key: val if random.random() > mutation_rate else random.choice([0, 1])
        for key, val in strategy.responses.items()
    }

    hold_grudges = strategy.hold_grudges if random.random() > mutation_rate else not strategy.hold_grudges

    random_defection = strategy.random_defection if random.random() > mutation_rate else random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    return Strategy(name="", first_move=first_move, responses=response_map, memory_size=2, hold_grudges=hold_grudges, random_defection=random_defection)

def crossover(parent1, parent2):
    off_1_first_move,off_2_first_move  = parent2.first_move, parent1.first_move

    off_1_hold_grudges = parent2.hold_grudges
    off_2_hold_grudges = parent1.hold_grudges

    off_1_random_defection, off_2_random_defection = parent1.random_defection, parent2.random_defection
    off_1_map = {key: random.choice([parent1.responses[key], parent2.responses[key]]) for key in parent1.responses}
    off_2_map = {key: random.choice([parent1.responses[key], parent2.responses[key]]) for key in parent1.responses}

    return (
        Strategy(name="", first_move=off_1_first_move, responses=off_1_map, memory_size=2, random_defection=off_1_random_defection, hold_grudges=off_1_hold_grudges),
        Strategy(name="", first_move=off_2_first_move, responses=off_2_map, memory_size=2, random_defection=off_2_random_defection, hold_grudges=off_2_hold_grudges)
    )
