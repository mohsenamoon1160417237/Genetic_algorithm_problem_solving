from GAFunctions import init_population, eval_fitness, pick_parents, gen_children
from GAConfig import population_size, parse_config, current_gen, maximum_gens
import csv

parse_config()
population = init_population(population_size)
fitnesses = []


def average(val):
    return sum(val) / len(val)


def find_best_candidate(fitnesses):
    fitnesses.sort(reverse=False)
    current_best = fitnesses[0][0]
    return current_best


while maximum_gens >= current_gen:
    with open('GAOutput.csv', 'a+', newline='') as GAOutput:
        csvOutput = csv.writer(GAOutput, delimiter=',')
        for pop in population:
            csvOutput.writerow(pop)
        csvOutput.writerow("")
    current_gen_fitnesses = eval_fitness(population)
    fitnesses.append(current_gen_fitnesses)
    parents = pick_parents(population)
    children = gen_children(parents)
    population = children
    print(
        f"Current Generation: {current_gen} - Population Fitness Average: {average(current_gen_fitnesses)} "
    )
    current_gen += 1

print(
    f"*** Best Fitness: {find_best_candidate(fitnesses)} -- Score: "
)
