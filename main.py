import random
from operators import crossover, mutation
from utils import init_population, select_parent
from prisonersdilema import play_all_strategies

GENERATIONS = 100
POPULATION_SIZE = 600
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8


def ga():
    population = init_population(POPULATION_SIZE)
    for _ in range(GENERATIONS):
        fitnesses = [play_all_strategies(pop) for pop in population] # GET geneome's score against the fixed strategies
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1 = select_parent(population, fitnesses)
            parent2 = select_parent(population, fitnesses)

            # Crossover
            if random.random() < CROSSOVER_RATE:
                offspring1, offspring2 = crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2

            # Mutation
            if random.random() < MUTATION_RATE:
                offspring1 = mutation(offspring1)
            if random.random() < MUTATION_RATE:
                offspring2 = mutation(offspring2)

            new_population.extend([offspring1, offspring2])

        best_index = fitnesses.index(max(fitnesses))
        best_in_pop = population[best_index]
        print(f"{best_in_pop.first_move}-{best_in_pop.responses}-{best_in_pop.hold_grudges}-{best_in_pop.random_defection}-{max(fitnesses)}")
        population = new_population

if __name__ == '__main__':
    ga()

