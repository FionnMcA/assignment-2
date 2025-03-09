import random
from strategy import Strategy

def mutation(strategy, mutation_rate=0.02):
    if random.random() < mutation_rate:
        new_first_move = 1 - strategy.first_move  # Flip from 0 to 1 or 1 t to 0
    else:
        new_first_move = strategy.first_move

    if random.random() < mutation_rate:
        new_hold_grudges = not strategy.hold_grudges
    else:
        new_hold_grudges = strategy.hold_grudges

    new_random_defection = strategy.random_defection
    if random.random() < mutation_rate:
        # Move up/down by 0.1
        step = random.choice([-0.1, 0.1])
        new_random_defection = min(max(0.0, new_random_defection + step), 1.0)

    new_responses = {}
    for key, old_val in strategy.responses.items():
        if random.random() < mutation_rate:
            # Flip from 0 to 1 or 1 to 0
            new_responses[key] = 1 - old_val
        else:
            new_responses[key] = old_val

    return Strategy(
        name="",
        first_move=new_first_move,
        responses=new_responses,
        memory_size=strategy.memory_size,
        hold_grudges=new_hold_grudges,
        random_defection=new_random_defection
    )

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
