import random
import matplotlib.pyplot as plt
from operators import crossover, mutation
from utils import init_population, select_parent
from prisonersdilema import play_all_strategies

GENERATIONS = 50
POPULATION_SIZE =75
ELITISM = True  # Keeps the best strategy from each generation
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.02

def ga():
    population = init_population(POPULATION_SIZE)
    best_overall_strategy = None
    best_overall_fitness = float('-inf')
    best_fitness_per_generation = []  # Track best fitness per generation

    for _ in range(GENERATIONS):
        # Evaluate fitness for each strategy in the population
        fitnesses = [play_all_strategies(individual) for individual in population]

        # Find the best strategy in this generation
        best_index = fitnesses.index(max(fitnesses))
        best_in_pop = population[best_index]
        best_fitness = fitnesses[best_index]

        # Store best fitness of this generation
        best_fitness_per_generation.append(best_fitness)

        # Update the best overall strategy if it's better
        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            best_overall_strategy = best_in_pop

        new_population = []

        if ELITISM:
            new_population.append(best_in_pop)  # Preserve the best strategy

        # Create new offspring via selection, crossover, and mutation
        while len(new_population) < POPULATION_SIZE:
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

        population = new_population[:POPULATION_SIZE]

    return best_overall_strategy, best_overall_fitness, best_fitness_per_generation


if __name__ == "__main__":

    for i in range(0,10):
        best_overall_strategy, best_overall_fitness, best_fitness_per_generation = ga()
        print(f"{i+1} - fitness: {best_overall_fitness} - first move: {best_overall_strategy.first_move} - responses: {best_overall_strategy.responses} - hold grudges: {best_overall_strategy.hold_grudges} - random defection: {best_overall_strategy.random_defection}")

    # TO PLOT FITNESS OVER TIME
    # best_strategy, best_fitness, fitness_history = ga()
    #
    # # Plot best fitness over generations
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(GENERATIONS), fitness_history, marker="o", linestyle="-", color="b", label="Best Fitness")
    # plt.xlabel("Generation")
    # plt.ylabel("Best Fitness")
    # plt.title("Evolution of Best Fitness Over Generations")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
