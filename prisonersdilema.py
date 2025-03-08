from strategy import Strategy
import random

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

# random = Strategy(
#     name='Random',
#     responses=None,
#     first_move= random.choice([1, 0]),
#     memory_size=1
# )

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
    friedman,
    tit_for_two_tats,
    joss,
    # random
]


def prisoners_dilemma(strat1, strat2, rounds=100):
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



    return score_1, score_2, strat1.history, strat2.history

def play_all_strategies(random_s):
    total = 0
    for strat in fixed_strategies:
        random_s.history = []
        score1, score2, s1_history, s2_history = prisoners_dilemma(random_s, strat)
        total += score1
    return total