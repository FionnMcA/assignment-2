from strategy import Strategy
import random

# Define fixed strats
always_c = Strategy(
    name='Always Cooperate',
    first_move=1,
    responses={(1,): 1, (0,): 1},
    memory_size=1
)

always_d = Strategy(
    name='Always Defect',
    first_move=0,
    responses={(1,): 0, (0,): 0},
    memory_size=1
)

tit_for_tat = Strategy(
    name='Tit For Tat',
    first_move=1,
    responses={(1,): 1, (0,): 0},
    memory_size=1
)

suspicious_tit_for_tat = Strategy(
    name='Suspicious Tit For Tat',
    first_move=0,
    responses={(1,): 1, (0,): 0},
    memory_size=1
)

friedman = Strategy(
    name='Friedman',
    first_move=1,
    responses={(1,): 1, (0,): 0},
    memory_size=1,
    hold_grudges=True
)

tit_for_two_tats = Strategy(
    name='Tit For Two Tats',
    first_move=1,
    responses={(1,): 0, (0,): 1, (1, 1): 0, (1, 0): 1, (0, 1): 1, (0, 0): 0},
    memory_size=2
)


suspicious_for_two_tats = Strategy(
    name='Suspicious Tit For Two Tats',
    first_move=0,
    responses={(1,): 1, (0,): 1, (1,1): 1, (1,0): 1, (0,1): 1, (0,0): 0},
    memory_size=2
)


joss = Strategy(
    name='Joss',
    first_move=1,
    responses={(1,): 1, (0,): 0},
    memory_size=1,
    random_defection=0.1
)

random = Strategy(
    name='Random',
    responses=None,
    first_move= random.choice([1, 0]),
    memory_size=1,
    random_strategy = True
)

GA = Strategy(
    name='GA',
    first_move=1,
    responses={(1,): 1, (0,): 0, (1, 1): 1, (1, 0): 0, (0, 1): 1, (0, 0): 0},
    memory_size=2,
)

Fibonacci = Strategy(
    name='Fibonacci',
    first_move=0,
    responses={(1,): 1, (0,): 0},
    memory_size=1,
    fibonacci_defection=True
)

Reverse_Fibonacci = Strategy(
    name='Reverse Fibonacci',
    first_move=1,
    responses={(1,): 1, (0,): 0},
    memory_size=1,
    fibonacci_defection=True
)

def payoff_matrix(p1_move, p2_move):
    if p1_move and p2_move:
        return (3, 3)  # Both Cooperate
    elif p1_move and not p2_move:
        return (0, 5)  # P1 cooperates, P2 defects
    elif not p1_move and p2_move:
        return (5, 0)  # P1 defects, P2 cooperates
    else:
        return (1, 1)  # Both defect

fixed_strategies = [
    always_c,
    always_d,
    tit_for_tat,
    suspicious_tit_for_tat,
    friedman,
    tit_for_two_tats,
    suspicious_for_two_tats,
    joss,
    random,
    Fibonacci,
    Reverse_Fibonacci
]

def prisoners_dilemma(strat1, strat2, rounds=75):
    """
    Two strats play their moves in an IDP and it returns the score for each player
    """
    strat1_move = strat1.first_move
    strat2_move = strat2.first_move

    score_1 = 0
    score_2 = 0

    for _ in range(rounds):
        round_score_1, round_score_2 = payoff_matrix(strat1_move, strat2_move)
        score_1 += round_score_1
        score_2 += round_score_2

        strat1.update_history(strat2_move)
        strat2.update_history(strat1_move)

        strat1_move = strat1.player_move()
        strat2_move = strat2.player_move()

    return score_1, score_2


def play_all_strategies(random_s):
    """
    This plays the ga evolved strat against the fixed strats (this is the fitness function)
    """
    total = 0
    for strat in fixed_strategies:
        random_s.history = []
        score1, score2 = prisoners_dilemma(random_s, strat)
        total += score1
    return total


###
# Here is for when I got the evolved strategy and ran it in an axelrod RR tournament to see how it performed in the whole tournament
###

def clone_strategy(original):
    """
    Returns a new Strategy with the same parameters but a clean state.
    """
    new_responses = dict(original.responses) if original.responses else None

    return Strategy(
        name=original.name,
        first_move=original.first_move,
        responses=new_responses,
        memory_size=original.memory_size,
        hold_grudges=original.hold_grudges,
        random_defection=original.random_defection,
        random_strategy=original.random_strategy
    )


def run_axelrod_tournament(strategies, rounds=100):
    """
    Plays each strategy against every other exactly once.
    """
    # Initialize total scores for each strategy name
    scores = {s.name: 0 for s in strategies}

    n = len(strategies)
    for i in range(n):
        for j in range(i + 1, n):
            # To clear the history of the strategy
            s1 = clone_strategy(strategies[i])
            s2 = clone_strategy(strategies[j])

            # Play them
            score1, score2 = prisoners_dilemma(s1, s2, rounds)

            # Accumulated score
            scores[strategies[i].name] += score1
            scores[strategies[j].name] += score2

    return scores


if __name__ == "__main__":
    fixed_strategies = [
        always_c,
        always_d,
        tit_for_tat,
        suspicious_tit_for_tat,
        friedman,
        tit_for_two_tats,
        suspicious_for_two_tats,
        joss,
        random,
        Fibonacci,
        Reverse_Fibonacci,
        GA
    ]

    # Run the tournament
    results = run_axelrod_tournament(fixed_strategies, rounds=100)

    # Print out final scores
    print("\n[Axelrod Tournament Results]")
    for name, total_score in results.items():
        print(f"{name}: {total_score}")
